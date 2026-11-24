const assert = require("node:assert/strict");
const { execFileSync, spawn } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { chromium } = require("playwright");

const repo = path.resolve(__dirname, "..");
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "jiw-web-check-"));
const python = process.env.PYTHON || "python3";
const projectBase = "/japan-infection-watch/";
const servers = [];

async function preview(name, base) {
  const workspace = path.join(scratch, name);
  fs.mkdirSync(workspace);
  const target = path.join(workspace, "site");
  execFileSync(python, ["-B", "-m", "fixtures.build_web_preview", target, "--base", base], {
    cwd: repo, env: { ...process.env, PYTHONPATH: path.join(repo, "tests") },
  });
  fs.symlinkSync(target, path.join(workspace, "active"));
  const server = spawn(python, ["-B", "poc/pages/serve.py", workspace, "--base", base], { cwd: repo });
  servers.push(server);
  return await new Promise((resolve, reject) => {
    server.stdout.once("data", data => resolve(data.toString().trim()));
    server.once("error", reject);
    server.once("exit", code => reject(new Error(`HTTP サーバー終了 ${code}`)));
  });
}

async function check() {
  const project = await preview("project", projectBase);
  const root = await preview("root", "/");
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 320, height: 850 } });
    const requests = [];
    const errors = [];
    page.on("request", request => requests.push(request.url()));
    page.on("pageerror", error => errors.push(error.message));
    await page.route("**/*", route => {
      const target = new URL(route.request().url()).origin;
      return [project, root].includes(target) ? route.continue() : route.abort();
    });

    const home = project + projectBase;
    assert.equal((await page.goto(home)).status(), 200);
    await page.keyboard.press("Tab");
    assert.equal(await page.locator(":focus").textContent(), "本文へ移動");
    await page.keyboard.press("Enter");
    assert.equal(new URL(page.url()).hash, "#main");
    assert.match(await page.locator(".provenance").textContent(), /2030年.*第5週/);
    assert.match(await page.locator(".notice").textContent(), /架空/);
    assert.ok(!requests.some(url => new URL(url).pathname.includes("/data/")));
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 320);
    await page.getByRole("searchbox", { name: "都道府県名で絞り込む" }).fill("北海道");
    assert.equal(await page.locator(".region-status").textContent(), "1件の都道府県");
    await page.getByRole("link", { name: "北海道", exact: true }).click();
    const pref = home + "prefectures/01/";
    assert.equal(page.url(), pref);
    assert.equal((await page.goto(pref.slice(0, -1))).status(), 200);
    assert.equal(page.url(), pref);
    assert.equal((await page.reload()).status(), 200);
    await page.getByRole("heading", { name: "北海道", exact: true }).waitFor();
    const influenza = page.getByRole("row").filter({ has: page.getByRole("link", { name: "インフルエンザ", exact: true }) });
    assert.match(await influenza.textContent(), /原表ハイフン.*空欄.*24.*2.40/);
    assert.ok(!requests.some(url => url.includes("/history/") || url.includes("/index/sample-jihs")));
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 320);

    const whenHistory = page.waitForResponse(response => response.url().includes("/history/"));
    await page.getByLabel("対象月").selectOption("2030-01");
    const button = page.getByRole("button", { name: "週次履歴を表示" });
    await button.focus();
    await page.keyboard.press("Enter");
    const history = await whenHistory;
    assert.match(history.url(), /\/prefecture\/01\/2030-01\/influenza\.json$/);
    assert.equal(history.status(), 200);
    await page.getByText("履歴を表示しました。", { exact: true }).waitFor();
    assert.match(await page.locator(".history-output").textContent(), /2030-01-07.*原表ハイフン.*空欄/);
    assert.equal(requests.filter(url => url.includes("/history/")).length, 1);

    await page.route("**/history/**", route => route.abort());
    await page.getByLabel("対象月").selectOption("2030-02");
    await button.click();
    await page.getByText(/履歴を読み込めませんでした/).waitFor();
    assert.match(await page.locator(".history-output").textContent(), /2030-01-07/);
    assert.match(await influenza.textContent(), /原表ハイフン.*空欄.*24.*2.40/);
    await page.unroute("**/history/**");

    const disease = root + "/diseases/influenza/";
    assert.equal((await page.goto(disease)).status(), 200);
    await page.getByRole("heading", { name: "インフルエンザ", exact: true }).waitFor();
    assert.equal(await page.locator("tbody tr").count(), 48);
    assert.ok(await page.locator(".table-scroll").evaluate(region => region.scrollWidth <= region.clientWidth));
    const nationalHistory = page.waitForResponse(response => response.url().includes("/history/"));
    await page.getByRole("button", { name: "週次履歴を表示" }).click();
    assert.match((await nationalHistory).url(), /\/national\/jp\/2030-02\/influenza\.json$/);
    await page.getByText("履歴を表示しました。", { exact: true }).waitFor();
    if (process.env.WEB_PREVIEW_SCREENSHOT) await page.screenshot({ path: process.env.WEB_PREVIEW_SCREENSHOT });
    assert.equal((await page.goto(home + "municipalities/21201/")).status(), 200);
    await page.getByText("このページに岐阜市の集計はありません。").waitFor();
    assert.match(await page.getByRole("link", { name: /岐阜市公式サイト/ }).getAttribute("href"), /^https:\/\/www\.city\.gifu\.lg\.jp\//);
    assert.equal(await page.getByRole("table").count(), 0);
    assert.equal((await page.goto(home + "municipalities/99999/")).status(), 404);
    await page.getByRole("link", { name: "全国のページへ戻る" }).click();
    assert.equal(page.url(), home);
    assert.deepEqual(errors, []);
    assert.ok(requests.every(url => [project, root].includes(new URL(url).origin)));
    console.log(`Chrome ${browser.version()} · 320px・キーボード・直リンク・再読込・404・履歴の遅延読込と失敗時の表示を確認`);
  } finally {
    await browser.close();
  }
}

check().catch(error => {
  console.error(error);
  process.exitCode = 1;
}).finally(() => {
  for (const server of servers) server.kill();
  fs.rmSync(scratch, { recursive: true, force: true });
});
