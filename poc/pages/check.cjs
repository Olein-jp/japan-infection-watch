const assert = require("node:assert/strict");
const { execFileSync, spawn } = require("node:child_process");
const { existsSync, mkdtempSync, readFileSync, readlinkSync, rmSync } = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { chromium } = require("playwright");

const base = "/japan-infection-watch/";
const top = mkdtempSync(path.join(os.tmpdir(), "jiw-pages-check-"));
const python = process.env.PYTHON || "python3";
const workspace = path.join(top, "project");
const rootWorkspace = path.join(top, "root");

function build(target, release, mount, ...flags) {
  return execFileSync(python, [path.join(__dirname, "build.py"), target, release, "--base", mount, ...flags],
    { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
}

async function startServer(target, mount) {
  const process = spawn(python, ["-u", path.join(__dirname, "serve.py"), target, "--base", mount]);
  try {
    const url = await new Promise((resolve, reject) => {
      process.stdout.once("data", data => resolve(String(data).trim()));
      process.once("error", reject);
      process.once("exit", code => reject(new Error(`HTTP サーバー終了 ${code}`)));
    });
    return { process, url };
  } catch (error) {
    process.kill();
    throw error;
  }
}

async function test() {
  const builds = [];
  for (let n = 1; n <= 3; n += 1) builds.push(JSON.parse(build(workspace, `release-0${n}`, base)));
  console.log("build", JSON.stringify(builds));
  console.log("root build", build(rootWorkspace, "root-01", "/").trim());
  const servers = [];
  let browser;
  try {
    servers.push(await startServer(workspace, base));
    servers.push(await startServer(rootWorkspace, "/"));
    const [project, root] = servers;
    browser = await chromium.launch({ channel: "chrome", headless: true });
    console.log("Chrome", browser.version());
    const active = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2,
      isMobile: true, hasTouch: true, serviceWorkers: "block" });
    const page = await active.newPage();
    const requests = [];
    const errors = [];
    page.on("request", request => requests.push(request.url()));
    page.on("pageerror", error => errors.push(error.message));
    await page.route("**/*", route => {
      if (servers.some(server => route.request().url().startsWith(server.url + "/"))) return route.continue();
      return route.abort();
    });

    const regionURL = project.url + base + "regions/sample-a/";
    assert.equal((await page.goto(regionURL.slice(0, -1))).status(), 200);
    assert.equal(page.url(), regionURL);
    await page.getByText("配布版 release-03", { exact: true }).waitFor();
    assert.equal(await page.getByRole("heading", { level: 1 }).textContent(), "青葉県（架空）");
    assert.equal(await page.locator("#latest tr").count(), 2);
    assert.match(await page.locator("#latest").textContent(), /0.50 件／定点/);
    assert.ok(!requests.some(url => url.includes("/history/")));
    assert.ok(requests.some(url => url.includes("/latest/") && url.includes("/sample-a/")));
    assert.ok(!requests.some(url => url.includes("/latest/") && url.includes("/sample-b/")));
    assert.ok(requests.every(url => url.startsWith(project.url + base)));
    const mobile = await page.evaluate(() => {
      const entries = performance.getEntriesByType("resource");
      const navigation = performance.getEntriesByType("navigation")[0];
      return {
        viewport: window.innerWidth, width: document.documentElement.scrollWidth,
        resources: entries.length + 1,
        bodyBytes: navigation.encodedBodySize + entries.reduce((sum, entry) => sum + entry.encodedBodySize, 0),
        domContentLoadedMs: Math.round(navigation.domContentLoadedEventEnd),
      };
    });
    assert.equal(mobile.viewport, mobile.width);
    assert.equal(await page.locator("svg polygon").count(), 2);
    if (process.env.R17_SCREENSHOT) await page.screenshot({ path: process.env.R17_SCREENSHOT });
    console.log("mobile", JSON.stringify(mobile));

    const historyResponse = page.waitForResponse(response => response.url().includes("/history/"));
    await page.getByRole("button", { name: "対象月の履歴を表示" }).click();
    assert.equal((await historyResponse).status(), 200);
    await page.locator("#history li").first().waitFor();

    await page.clock.setFixedTime(new Date("2030-01-24T00:00:00+09:00"));
    await page.reload();
    await page.getByText("配布版 release-03", { exact: true }).waitFor();
    await page.getByText("次回更新の予定時刻を過ぎています。", { exact: true }).waitFor();
    await page.goto(project.url + base + "regions/sample-b/");
    await page.getByText("選択地域の状態　データなし", { exact: true }).waitFor();
    assert.match(await page.locator("#latest").textContent(), /データなし/);

    assert.equal((await page.goto(project.url + base + "regions/unknown/")).status(), 404);
    await page.getByRole("heading", { name: "ページが見つかりません" }).waitFor();
    await page.getByRole("link", { name: "トップへ戻る" }).click();
    await page.getByRole("heading", { name: "地域を選ぶ" }).waitFor();
    assert.equal(page.url(), project.url + base);
    assert.equal((await page.goto(root.url + "/regions/sample-a/")).status(), 200);
    await page.getByText("配布版 root-01", { exact: true }).waitFor();

    const pointer = readlinkSync(path.join(workspace, "active"));
    const manifest = readFileSync(path.join(workspace, "active/data/manifest.json"));
    assert.throws(() => build(workspace, "rejected", base, "--reject-candidate"),
      error => error.status === 2 && error.stderr.includes("ハッシュまたはサイズが不一致"));
    assert.equal(readlinkSync(path.join(workspace, "active")), pointer);
    assert.deepEqual(readFileSync(path.join(workspace, "active/data/manifest.json")), manifest);
    assert.ok(!existsSync(path.join(workspace, "archive/rejected")));
    await page.goto(regionURL);
    await page.getByText("配布版 release-03", { exact: true }).waitFor();
    assert.match(await page.locator("#latest").textContent(), /0.50 件／定点/);
    assert.deepEqual(errors, []);
    console.log("直リンク・再読込・末尾スラッシュ・404・ルート配置・遅延読込・欠損・旧版保持を確認");
  } finally {
    try { if (browser) await browser.close(); } finally {
      for (const server of servers) server.process.kill();
    }
  }
}

test().catch(error => {
  console.error(error);
  process.exitCode = 1;
}).finally(() => rmSync(top, { recursive: true, force: true }));
