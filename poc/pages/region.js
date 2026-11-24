const container = document.querySelector("#data");
const region = container.dataset.region;
const manifestURL = new URL(container.dataset.manifest, location.href);
const status = document.querySelector("#status");
const historyButton = document.querySelector("#history-button");

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function text(tag, value) {
  const node = document.createElement(tag);
  node.textContent = value;
  return node;
}

function displayValue(row) {
  if (row.value_status !== "reported") return "データなし";
  const unit = row.unit === "case" ? "件" : "件／定点";
  return `${row.value} ${unit}`;
}

function draw(geojson, hasData) {
  const namespace = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(namespace, "svg");
  svg.setAttribute("viewBox", "-2 -2 89 30");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "架空の行政区域。選択地域の報告状況は凡例に表示。");
  for (const feature of geojson.features) {
    const shape = document.createElementNS(namespace, "polygon");
    shape.setAttribute("points", feature.geometry.coordinates[0].map(point => point.join(",")).join(" "));
    shape.setAttribute("stroke", "#335456");
    shape.setAttribute("fill", feature.id === region && hasData ? "#86b6a3" : "#e4e9e7");
    if (feature.id === region) shape.setAttribute("stroke-width", "2");
    svg.append(shape);
  }
  document.querySelector("#map").append(svg);
  document.querySelector("#legend").textContent = hasData ? "選択地域の状態　報告あり" : "選択地域の状態　データなし";
}

async function load() {
  const manifest = await json(manifestURL);
  const matches = manifest.files.filter(item => item.region_id === region);
  const latest = matches.find(item => item.kind === "latest");
  const map = manifest.files.find(item => item.kind === "map");
  const readEntry = entry => json(new URL(entry.path, manifestURL));
  const [current, boundaries] = await Promise.all([readEntry(latest), readEntry(map)]);
  if (current.release_id !== manifest.release_id) throw new Error("配布版の不一致");
  const table = document.querySelector("#latest");
  for (const row of current.observations) {
    const label = row.metric_id === "sentinel_report_count" ? "報告数" : "定点当たり報告数";
    const line = document.createElement("tr");
    line.append(text("th", label), text("td", displayValue(row)),
      text("td", `${row.period_start} ～ ${row.period_end}`));
    line.firstChild.scope = "row";
    table.append(line);
  }
  const source = manifest.sources[latest.dataset_id];
  const due = Date.parse(source.next_update_due_at);
  document.querySelector("#age").textContent = !Number.isFinite(due)
    ? "次回更新予定は未確認です。"
    : Date.now() > due ? "次回更新の予定時刻を過ぎています。" : "次回更新予定の範囲内です。";
  const freshness = document.querySelector("#freshness");
  for (const [label, value] of [
    ["対象期間の終了日", source.latest_period_end],
    ["提供元の更新", source.source_updated_on],
    ["最終取得成功", source.last_fetch_succeeded_at],
    ["表示中の版の取得", source.published_version_fetched_at],
    ["サイト生成", manifest.generated_at],
  ]) freshness.append(text("dt", label), text("dd", value));
  status.textContent = `配布版 ${manifest.release_id}`;
  document.querySelector("#source").textContent = `出典　${source.attribution}`;
  draw(boundaries, current.observations.some(row => row.value_status === "reported"));
  const history = matches.find(item => item.kind === "history" && item.year_month === source.latest_period_end.slice(0, 7));
  if (!history) return;
  historyButton.disabled = false;
  historyButton.addEventListener("click", async () => {
    historyButton.disabled = true;
    const list = document.querySelector("#history");
    list.replaceChildren();
    try {
      const payload = await readEntry(history);
      if (payload.release_id !== manifest.release_id) throw new Error("配布版の不一致");
      for (const row of payload.observations) list.append(text("li", `${row.period_end}　${displayValue(row)}`));
    } catch {
      list.replaceChildren(text("li", "履歴を読み込めませんでした。"));
      historyButton.disabled = false;
    }
  });
}

load().catch(() => { status.textContent = "データを読み込めませんでした。"; });
