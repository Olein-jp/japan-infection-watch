const assert = require("node:assert/strict");
const { createHash } = require("node:crypto");
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

function build(target, base, ...flags) {
  execFileSync(python, ["-B", "-m", "fixtures.build_web_preview", target, "--base", base, ...flags], {
    cwd: repo, env: { ...process.env, PYTHONPATH: path.join(repo, "tests") }, stdio: ["ignore", "pipe", "pipe"],
  });
}

function verify(target, ...options) {
  const report = execFileSync(python, ["-B", "scripts/check_preview.py", target, ...options], {
    cwd: repo, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"],
  });
  return JSON.parse(report);
}

function switchLocalSite(workspace, target) {
  const next = path.join(workspace, "next");
  fs.symlinkSync(target, next);
  fs.renameSync(next, path.join(workspace, "active"));
}

async function preview(name, base) {
  const workspace = path.join(scratch, name);
  fs.mkdirSync(workspace);
  const target = path.join(workspace, "site");
  build(target, base);
  verify(target);
  switchLocalSite(workspace, target);
  const server = spawn(python, ["-B", "poc/pages/serve.py", workspace, "--base", base], { cwd: repo });
  servers.push(server);
  return await new Promise((resolve, reject) => {
    server.stdout.once("data", data => resolve({ url: data.toString().trim(), workspace, target }));
    server.once("error", reject);
    server.once("exit", code => reject(new Error(`HTTP サーバー終了 ${code}`)));
  });
}

async function servedVersion(page, home) {
  async function get(pathname, reference) {
    const response = await page.request.get(home + pathname, { maxRedirects: 0 });
    assert.equal(response.status(), 200);
    const bytes = await response.body();
    if (reference) {
      assert.equal(bytes.length, reference.bytes);
      assert.equal(createHash("sha256").update(bytes).digest("hex"), reference.sha256);
    }
    return JSON.parse(bytes);
  }

  const manifest = await get("data/manifest.json");
  const indexEntry = manifest.sources["sample-jihs-weekly"].region_indexes.jp;
  const index = await get("data/" + indexEntry.path, indexEntry);
  const latestEntry = index.diseases.influenza.latest;
  const latest = await get("data/" + latestEntry.path, latestEntry);
  assert.equal(index.release_id, manifest.release_id);
  assert.equal(latest.release_id, manifest.release_id);
  return { manifest, latest };
}

async function checkRecovery(page, project) {
  const { workspace, target } = project;
  const home = project.url + projectBase;
  const archived = path.join(workspace, "archive", "last-good");
  fs.mkdirSync(path.dirname(archived));
  fs.cpSync(target, archived, { recursive: true });
  const saved = verify(archived);
  assert.equal(saved.sha256, verify(target).sha256);
  const before = await servedVersion(page, home);
  const active = path.join(workspace, "active");

  function publishCandidate(candidate, ...options) {
    const report = verify(candidate, "--baseline", fs.realpathSync(active), ...options);
    if (report.change === "changed") switchLocalSite(workspace, candidate);
    return report;
  }

  const damaged = path.join(workspace, "damaged");
  fs.cpSync(archived, damaged, { recursive: true });
  const release = before.manifest.release_id;
  const shard = path.join(damaged, "data", "releases", release,
    "latest/sample-jihs-weekly/national/jp/influenza.json");
  const bytes = fs.readFileSync(shard);
  bytes[bytes.length - 1] = 0x20;
  fs.writeFileSync(shard, bytes);
  assert.throws(() => publishCandidate(damaged), error => error.status === 2 && error.stderr.includes("SHA-256"));
  assert.throws(() => publishCandidate(archived, "--max-bytes", "3"),
    error => error.status === 2 && error.stderr.includes("容量超過"));
  assert.throws(() => publishCandidate(archived, "--candidate-revision", "a".repeat(40),
    "--expected-revision", "b".repeat(40)), error => error.status === 2 && error.stderr.includes("古い候補"));
  assert.equal(publishCandidate(archived).change, "unchanged");
  assert.equal(fs.readlinkSync(active), target);
  assert.deepEqual(await servedVersion(page, home), before);

  const corrected = path.join(workspace, "corrected");
  build(corrected, projectBase, "--latest-count", "26");
  assert.equal(publishCandidate(corrected).change, "changed");
  const current = await servedVersion(page, home);
  assert.notEqual(current.manifest.release_id, release);
  assert.equal(current.latest.observations[0].value, 26);

  const restored = path.join(workspace, "restored");
  fs.cpSync(archived, restored, { recursive: true });
  assert.equal(verify(restored).sha256, saved.sha256);
  switchLocalSite(workspace, restored);
  assert.deepEqual(await servedVersion(page, home), before);
  assert.equal((await page.goto(home + "diseases/influenza/")).status(), 200);
  const nationwide = page.getByRole("row").filter({ has: page.getByRole("rowheader", { name: "全国", exact: true }) });
  assert.deepEqual(await nationwide.getByRole("cell").allTextContents(), ["24", "2.40"]);
  console.log(`旧版維持と復旧を確認 · ${saved.file_count}ファイル · SHA-256 ${saved.sha256}`);
}

async function check() {
  const project = await preview("project", projectBase);
  const root = await preview("root", "/");
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 320, height: 850 } });
    const origins = [project.url, root.url];
    const requests = [];
    const errors = [];
    page.on("request", request => requests.push(request.url()));
    page.on("pageerror", error => errors.push(error.message));
    await page.route("**/*", route => {
      const target = new URL(route.request().url()).origin;
      return origins.includes(target) ? route.continue() : route.abort();
    });

    const home = project.url + projectBase;
    assert.equal((await page.goto(home)).status(), 200);
    await page.keyboard.press("Tab");
    assert.equal(await page.locator(":focus").textContent(), "本文へ移動");
    await page.keyboard.press("Enter");
    assert.equal(new URL(page.url()).hash, "#main");
    assert.match(await page.locator(".provenance").textContent(), /2030年.*第5週/);
    assert.match(await page.locator(".notice").textContent(), /架空/);
    assert.ok(!requests.some(url => new URL(url).pathname.includes("/data/")));
    assert.equal(await page.locator("#regions").evaluate(el => el.compareDocumentPosition(document.querySelector("#diseases")) & Node.DOCUMENT_POSITION_FOLLOWING), 4);
    assert.match(await page.getByRole("link", { name: "日本学校保健会の感染症情報マップ" }).getAttribute("href"),
      /^https:\/\/www\.gakkohoken\.jp\//);
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
    const breadcrumbs = page.getByRole("navigation", { name: "パンくずリスト" });
    assert.equal(await breadcrumbs.getByRole("link", { name: "都道府県", exact: true }).getAttribute("href"), projectBase + "#regions");
    assert.equal(await breadcrumbs.locator('[aria-current="page"]').textContent(), "北海道");
    await page.getByRole("link", { name: "学級閉鎖・休校の情報を見る" }).click();
    assert.equal(new URL(page.url()).hash, "#school-closures");
    const school = page.getByRole("region", { name: "学級閉鎖・休校", exact: true });
    assert.match(await school.getByRole("link", { name: /日本学校保健会/ }).getAttribute("href"), /^https:\/\/www\.gakkohoken\.jp\//);
    assert.match(await school.getByRole("link", { name: /厚生労働省/ }).getAttribute("href"), /^https:\/\/www\.mhlw\.go\.jp\//);
    const municipalChartName = "市区町村別の学級閉鎖（インフルエンザ）";
    const municipalChart = await school.getByRole("link", { name: municipalChartName }).getAttribute("href");
    assert.match(municipalChart, /^https:\/\/public\.tableau\.com\/.*\/____16744492330710\/1\?/);
    await page.emulateMedia({ forcedColors: "active" });
    assert.equal(await page.evaluate(() => window.matchMedia("(forced-colors: active)").matches), true);
    const influenza = page.getByRole("row").filter({ has: page.getByRole("link", { name: "インフルエンザ", exact: true }) });
    assert.deepEqual(await influenza.getByRole("cell").allTextContents(), ["-", "空欄", "24", "2.40"]);
    await page.getByText("履歴を表示しました。", { exact: true }).waitFor();
    await page.locator(".history-output").getByRole("columnheader", { name: "医療機関1か所あたり（件）", exact: true }).waitFor();
    assert.equal(await page.locator(".history-output tbody tr").count(), 2);
    const comparison = page.locator(".history-comparison");
    const legend = comparison.locator(".trend-legend");
    assert.equal(await comparison.locator(".trend").count(), 1);
    assert.equal(await legend.getByRole("button").count(), 19);
    assert.equal(await comparison.locator(".trend-area path").count(), 18);
    assert.match(await legend.getByRole("button", { name: /インフルエンザ/ }).textContent(), /空欄$/);
    assert.match(await page.locator(".history-output tbody tr").first().textContent(), /2030-02-03/);
    const series = legend.getByRole("button", { name: /ＲＳウイルス感染症/ });
    await series.focus();
    await page.keyboard.press("Enter");
    assert.equal(await series.getAttribute("aria-pressed"), "true");
    assert.equal(await comparison.locator(".trend-area path.trend-muted").count(), 17);
    await page.keyboard.press("Enter");
    assert.equal(await series.getAttribute("aria-pressed"), "false");
    assert.equal(await comparison.locator(".trend-area path.trend-muted").count(), 0);
    assert.ok(requests.filter(url => url.includes("/history/")).every(url => url.includes("/prefecture/01/") && url.endsWith("/influenza.json")));
    const detailDisease = page.getByLabel("詳細表の疾患");
    assert.equal(await detailDisease.inputValue(), "influenza");
    await detailDisease.selectOption("rs-virus");
    await page.locator(".history-output").getByRole("heading", { name: /ＲＳウイルス感染症/ }).waitFor();
    assert.equal(await comparison.locator(".trend-area path").count(), 18);
    await detailDisease.selectOption("influenza");
    await page.locator(".history-output").getByRole("heading", { name: /インフルエンザ/ }).waitFor();
    assert.equal(await page.locator(".history").evaluate(el => el.compareDocumentPosition(document.querySelector(".provenance")) & Node.DOCUMENT_POSITION_FOLLOWING), 4);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 320);

    const previousRequestCount = requests.filter(url => url.includes("/history/")).length;
    const monthSelect = page.getByLabel("対象月");
    await monthSelect.selectOption("2030-01");
    await monthSelect.focus();
    const button = page.getByRole("button", { name: "週次履歴を表示" });
    await page.keyboard.press("Tab");
    assert.equal(await page.locator(":focus").textContent(), "週次履歴を表示");
    const [history] = await Promise.all([
      page.waitForResponse(response => response.url().includes("/history/")),
      page.keyboard.press("Enter"),
    ]);
    assert.match(history.url(), /\/prefecture\/01\/2030-01\/influenza\.json$/);
    assert.equal(history.status(), 200);
    await page.getByText("履歴を表示しました。", { exact: true }).waitFor();
    const week = page.locator(".history-output tbody tr");
    assert.match(await week.getByRole("rowheader").textContent(), /2030-01-07/);
    assert.deepEqual((await week.getByRole("cell").allTextContents()).slice(0, 2), ["-", "空欄"]);
    assert.match(await legend.textContent(), /2030-01-13終了/);
    assert.equal(await comparison.locator(".trend-area .trend-dot").count(), 18);
    assert.equal(requests.filter(url => url.includes("/history/")).length, previousRequestCount + 1);

    await page.route("**/history/**/2030-02/*.json", route => route.abort());
    await monthSelect.selectOption("");
    await button.click();
    await page.getByText(/履歴を読み込めませんでした/).waitFor();
    assert.match(await page.locator(".history-output").textContent(), /2030-01-07/);
    assert.match(await legend.textContent(), /2030-01-13終了/);
    assert.deepEqual(await influenza.getByRole("cell").allTextContents(), ["-", "空欄", "24", "2.40"]);
    await page.unroute("**/history/**/2030-02/*.json");
    await page.emulateMedia({ forcedColors: null });

    const disease = root.url + "/diseases/influenza/";
    assert.equal((await page.goto(disease.slice(0, -1))).status(), 200);
    assert.equal(page.url(), disease);
    assert.equal((await page.reload()).status(), 200);
    await page.getByRole("heading", { name: "インフルエンザ", exact: true }).waitFor();
    assert.equal(await page.locator("tbody tr").count(), 48);
    assert.ok(await page.locator(".table-scroll").evaluate(region => region.scrollWidth <= region.clientWidth));
    await page.getByRole("button", { name: "週次履歴を表示" }).click();
    await page.getByText("履歴を表示しました。", { exact: true }).waitFor();
    assert.match(await page.locator(".history-output tbody").textContent(), /2030-02-03.*2030-01-07/);
    assert.equal(await page.locator(".history-output tbody tr").count(), 2);
    assert.match(await page.locator(".trend-area path").getAttribute("d"), /^M[^M]+ M[^M]+$/);
    assert.equal(await page.locator(".trend-dot").first().evaluate(el => el.style.top), "100%");
    assert.match(await page.getByRole("link", { name: "6か月より前のデータは JIHS で見る" }).getAttribute("href"),
      /\/provisional\/sokuhou\.html$/);
    if (process.env.WEB_PREVIEW_SCREENSHOT) await page.screenshot({ path: process.env.WEB_PREVIEW_SCREENSHOT });
    assert.equal((await page.goto(home + "municipalities/21201/")).status(), 200);
    await page.getByText("このページに岐阜市の集計はありません。").waitFor();
    assert.match(await page.getByRole("link", { name: /岐阜市公式サイト/ }).getAttribute("href"), /^https:\/\/www\.city\.gifu\.lg\.jp\//);
    assert.equal(await page.getByRole("link", { name: municipalChartName }).getAttribute("href"), municipalChart);
    assert.equal(await page.getByRole("table").count(), 0);
    assert.equal((await page.goto(home + "municipalities/99999/")).status(), 404);
    await page.getByRole("link", { name: "全国のページへ戻る" }).click();
    assert.equal(page.url(), home);
    assert.equal((await page.goto(root.url + "/municipalities/99999/")).status(), 404);
    await page.getByRole("link", { name: "全国のページへ戻る" }).click();
    assert.equal(page.url(), root.url + "/");
    await checkRecovery(page, project);
    assert.deepEqual(errors, []);
    assert.ok(requests.every(url => origins.includes(new URL(url).origin)));
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
