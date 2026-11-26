const statuses = {
  blank: "空欄",
  dash: "-",
  unknown_count: "計数不明",
  not_reported: "未報告",
  suppressed: "秘匿",
  not_applicable: "対象外",
};
const metrics = ["sentinel_report_count", "sentinel_reports_per_site"];

function element(tag, text) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}

function dataUrl(relative, base) {
  if (typeof relative !== "string" || !relative.startsWith("releases/")) {
    throw new Error("データのパスが不正です");
  }
  const path = new URL(relative, base);
  if (path.origin !== base.origin || !path.pathname.startsWith(base.pathname + "releases/")) {
    throw new Error("サイト内のデータを指定してください");
  }
  return path;
}

async function readJson(url, release) {
  const response = await fetch(url);
  if (!response.ok) throw new Error("データを取得できません");
  const data = await response.json();
  if (data.release_id !== release) throw new Error("配布版が一致しません");
  return data;
}

function historyChart(weeks) {
  const chart = element("div");
  chart.className = "trend";
  chart.append(element("p", "報告を担当する医療機関1か所あたりの報告数（件）"));
  const points = [...weeks].map(([end, week]) => {
    const rate = week.cells.sentinel_reports_per_site;
    return { end, value: rate?.value_status === "reported" ? Number(rate.value) : null };
  });
  const values = points.flatMap(point => point.value === null ? [] : [point.value]);
  if (!values.length) {
    chart.append(element("p", "選択した期間に表示できる報告数はありません。"));
    return chart;
  }

  const max = Math.max(1, Math.ceil(Math.max(...values)));
  const days = points.map(point => Date.parse(point.end) / 86_400_000);
  const first = days[0];
  const last = days[days.length - 1];
  const plot = element("div");
  plot.className = "trend-plot";
  plot.setAttribute("aria-hidden", "true");
  const labels = element("div");
  labels.className = "trend-axis";
  labels.append(element("span", max), element("span", max / 2), element("span", "0"));
  const area = element("div");
  area.className = "trend-area";
  const svgName = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgName, "svg");
  svg.setAttribute("viewBox", "0 0 100 100");
  svg.setAttribute("preserveAspectRatio", "none");
  const line = document.createElementNS(svgName, "path");
  let segments = "";
  let previousDay = null;
  for (const [index, point] of points.entries()) {
    if (point.value === null) {
      previousDay = null;
      continue;
    }
    const day = days[index];
    const x = first === last ? 50 : (day - first) / (last - first) * 100;
    const y = (1 - point.value / max) * 100;
    segments += `${previousDay !== null && day - previousDay === 7 ? "L" : "M"}${x} ${y} `;
    previousDay = day;
    const dot = element("span");
    dot.className = "trend-dot";
    dot.style.left = `${x}%`;
    dot.style.top = `${y}%`;
    area.append(dot);
  }
  line.setAttribute("d", segments.trim());
  line.setAttribute("vector-effect", "non-scaling-stroke");
  svg.append(line);
  area.prepend(svg);
  const dates = element("div");
  dates.className = "trend-dates";
  dates.append(element("span", points[0].end));
  if (first !== last) dates.append(element("span", points[points.length - 1].end));
  plot.append(labels, area, dates);
  chart.append(plot);
  return chart;
}

function historyTable(data, caption) {
  const weeks = new Map();
  for (const row of data.observations) {
    if (!weeks.has(row.period_end)) {
      weeks.set(row.period_end, { start: row.period_start, version: row.version_id, cells: {} });
    }
    weeks.get(row.period_end).cells[row.metric_id] = row;
  }
  const heading = element("h3", caption);
  const table = element("table");
  table.append(element("caption", "週別の報告件数と医療機関1か所あたりの報告数"));
  const head = table.createTHead().insertRow();
  const readLabel = Object.values(data.versions).some(version => version.source_url)
    ? "CSV の読み込み日時" : "取得日時（架空）";
  for (const name of ["対象期間", "報告件数（件）", "医療機関1か所あたり（件）", "原表作成日", readLabel]) {
    const cell = element("th", name);
    cell.scope = "col";
    head.append(cell);
  }
  const tbody = table.createTBody();
  for (const [end, week] of weeks) {
    const row = tbody.insertRow();
    const provenance = data.versions[week.version];
    const period = element("th");
    const periodLabel = `${week.start}〜${end}`;
    if (provenance.source_url) {
      const source = element("a", periodLabel);
      source.href = provenance.source_url;
      source.setAttribute("aria-label", `${periodLabel} の JIHS IDWR 速報（出典）`);
      period.append(source);
    } else {
      period.textContent = periodLabel;
    }
    period.scope = "row";
    row.append(period);
    for (const metric of metrics) {
      const cell = week.cells[metric];
      const number = cell?.value_status === "reported";
      const display = number ? cell.value : statuses[cell?.value_status] ?? "データなし";
      const item = element("td", display);
      item.className = number ? "number" : "missing";
      row.append(item);
    }
    row.append(element("td", provenance.source_created_on), element("td", provenance.retrieved_at));
  }
  const scroll = element("div");
  scroll.className = "table-scroll history-table";
  scroll.tabIndex = 0;
  scroll.setAttribute("role", "region");
  scroll.setAttribute("aria-label", "週次履歴の表");
  scroll.append(table);
  const hint = element("p", "画面が狭い場合は表を横にスクロールできます。");
  hint.className = "table-hint";
  const note = element("p", "- は原表の表記です。報告数の 0 とは区別しています。");
  note.className = "table-note";
  return [heading, historyChart(weeks), hint, scroll, note];
}

const form = document.querySelector(".history-form");
if (form) {
  form.hidden = false;
  const output = document.querySelector(".history-output");
  const status = document.querySelector(".history-status");
  const button = form.querySelector("button");
  const dataBase = new URL(form.dataset.base, window.location.origin);
  let index;

  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (button.disabled) return;
    const month = form.elements.month.value;
    const diseaseSelect = form.elements.disease;
    const disease = diseaseSelect ? diseaseSelect.value : form.dataset.disease;
    const period = month || "収録期間すべて";
    const caption = diseaseSelect ? `${diseaseSelect.selectedOptions[0].textContent} · ${period}` : period;
    button.disabled = true;
    status.textContent = "履歴を読み込んでいます。";
    try {
      const release = form.dataset.release;
      index ??= await readJson(new URL(form.dataset.index, window.location.origin), release);
      const history = index.diseases[disease]?.history ?? {};
      const months = (month ? [month] : Object.keys(history).sort()).filter(key => history[key]);
      if (!months.length) {
        output.replaceChildren();
        status.textContent = "選択した月の履歴はありません。";
        return;
      }
      const shards = await Promise.all(months.map(key => readJson(dataUrl(history[key].path, dataBase), release)));
      const data = {
        observations: shards.flatMap(shard => shard.observations),
        versions: Object.assign({}, ...shards.map(shard => shard.versions)),
      };
      output.replaceChildren(...historyTable(data, caption));
      status.textContent = "履歴を表示しました。";
    } catch {
      status.textContent = "履歴を読み込めませんでした。再読み込みしてからもう一度お試しください。";
    } finally {
      button.disabled = false;
    }
  });
  if (form.elements.disease) form.requestSubmit();
}

const filter = document.querySelector(".region-filter");
if (filter) {
  filter.hidden = false;
  const input = filter.querySelector("input");
  const items = document.querySelectorAll(".region-list li");
  const status = document.querySelector(".region-status");
  input.addEventListener("input", () => {
    const query = input.value.trim();
    let shown = 0;
    for (const item of items) {
      item.hidden = !item.textContent.includes(query);
      if (!item.hidden) shown += 1;
    }
    status.textContent = query ? `${shown}件の都道府県` : "";
  });
}
