const statuses = {
  blank: "空欄",
  dash: "-",
  unknown_count: "計数不明",
  not_reported: "未報告",
  suppressed: "秘匿",
  not_applicable: "対象外",
};
const metrics = ["sentinel_report_count", "sentinel_reports_per_site"];
const trendColors = [
  "#007267", "#b6470c", "#235fa7", "#962f61", "#59601a", "#64439a", "#9b3440",
  "#13778b", "#8d480f", "#394b9f", "#aa3d77", "#486816", "#755185", "#ae2633",
  "#21635c", "#92610e", "#38577e", "#814771", "#38704b",
];
const trendDashes = ["none", "7 4", "2 4"];

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

function historyChart(series, comparison = false) {
  const chart = element("div");
  chart.className = "trend";
  chart.append(element("p", "報告を担当する医療機関1か所あたりの報告数（件）"));
  const ends = [...new Set(series.flatMap(({ points }) => points.map(point => point.end)))].sort();
  const values = series.flatMap(({ points }) => points.filter(point => point.status === "reported")
    .map(point => Number(point.value)));
  const latest = ends.at(-1);
  const layers = new Map();
  if (!values.length) {
    chart.append(element("p", "選択した期間に表示できる報告数はありません。"));
  } else {
    chart.append(historyPlot(series, ends, values, layers, comparison));
  }
  if (comparison && latest) chart.append(historyLegend(series, latest, layers));
  return chart;
}

function historyPlot(series, ends, values, layers, comparison) {
  const max = Math.max(1, Math.ceil(Math.max(...values)));
  const dayNumber = end => Date.parse(end) / 86_400_000;
  const first = dayNumber(ends[0]);
  const last = dayNumber(ends.at(-1));
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
  area.append(svg);
  for (const { code, color, dash, points } of series) {
    const line = document.createElementNS(svgName, "path");
    const dots = element("div");
    dots.className = "trend-points";
    if (color) {
      line.style.stroke = color;
      dots.style.setProperty("--series-color", color);
    }
    if (dash) line.style.strokeDasharray = dash;
    let segments = "";
    let previousDay = null;
    const reported = points.filter(point => point.status === "reported");
    for (const [i, point] of reported.entries()) {
      const day = dayNumber(point.end);
      const x = first === last ? 50 : (day - first) / (last - first) * 100;
      const y = (1 - Number(point.value) / max) * 100;
      const connects = previousDay !== null && day - previousDay === 7;
      segments += `${connects ? "L" : "M"}${x} ${y} `;
      previousDay = day;
      const next = reported[i + 1];
      if (comparison && (connects || (next && dayNumber(next.end) - day === 7))) continue;
      const dot = element("span");
      dot.className = "trend-dot";
      dot.style.left = `${x}%`;
      dot.style.top = `${y}%`;
      dots.append(dot);
    }
    if (!segments) continue;
    line.setAttribute("d", segments.trim());
    line.setAttribute("vector-effect", "non-scaling-stroke");
    svg.append(line);
    area.append(dots);
    layers.set(code, [line, dots]);
  }
  const dates = element("div");
  dates.className = "trend-dates";
  dates.append(element("span", ends[0]));
  if (first !== last) dates.append(element("span", ends.at(-1)));
  plot.append(labels, area, dates);
  return plot;
}

function historyLegend(series, latest, layers) {
  const legend = element("div");
  legend.className = "trend-legend";
  legend.append(element("p", `表示期間の最新週（${latest}終了）の値。疾患名を選ぶと線を強調できます。`));
  const list = element("ul");
  const entries = series.map(item => ({ ...item, latest: item.points.find(point => point.end === latest) }));
  const latestRate = item => item.latest?.status === "reported" ? Number(item.latest.value) : -1;
  entries.sort((a, b) => latestRate(b) - latestRate(a));
  const buttons = new Map();
  let selected = null;
  for (const { code, name, color, dash, latest: point } of entries) {
    const row = element("li");
    const button = element("button");
    button.type = "button";
    button.disabled = !layers.has(code);
    button.setAttribute("aria-pressed", "false");
    const swatch = element("span");
    swatch.className = "trend-swatch";
    swatch.style.color = color;
    swatch.style.borderTopStyle = dash === "none" ? "solid" : dash === "7 4" ? "dashed" : "dotted";
    swatch.setAttribute("aria-hidden", "true");
    const value = point?.status === "reported" ? point.value : statuses[point?.status] ?? "データなし";
    button.append(swatch, element("span", name), element("strong", value));
    buttons.set(code, button);
    button.addEventListener("click", () => {
      selected = selected === code ? null : code;
      for (const [key, item] of buttons) {
        item.setAttribute("aria-pressed", String(key === selected));
      }
      for (const [key, [line, dots]] of layers) {
        line.classList.toggle("trend-muted", selected !== null && key !== selected);
        dots.classList.toggle("trend-muted", selected !== null && key !== selected);
        if (key === selected) {
          line.parentNode.append(line);
          dots.parentNode.append(dots);
        }
      }
    });
    row.append(button);
    list.append(row);
  }
  legend.append(list, element("p", "疾患によって報告する医療機関の種類や範囲が異なります。数値は疾患ごとの定点報告の目安です。"));
  return legend;
}

function historyTable(data, caption, includeChart) {
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
  for (const [end, week] of [...weeks].reverse()) {
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
  const content = [heading, hint, scroll, note];
  if (includeChart) {
    const points = [...weeks].map(([end, week]) => {
      const rate = week.cells.sentinel_reports_per_site;
      return { end, status: rate?.value_status, value: rate?.value };
    });
    content.splice(1, 0, historyChart([{ points }]));
  }
  return content;
}

const form = document.querySelector(".history-form");
if (form) {
  form.hidden = false;
  const output = document.querySelector(".history-output");
  const status = document.querySelector(".history-status");
  const comparison = document.querySelector(".history-comparison");
  const diseaseSelect = document.querySelector("#history-disease");
  const button = form.querySelector("button");
  const dataBase = new URL(form.dataset.base, window.location.origin);
  let index;
  let shownMonth;

  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (button.disabled) return;
    const month = form.elements.month.value;
    const disease = diseaseSelect ? diseaseSelect.value : form.dataset.disease;
    const period = month || "収録期間すべて";
    const caption = diseaseSelect ? `${diseaseSelect.selectedOptions[0].textContent} · ${period}` : period;
    button.disabled = true;
    if (diseaseSelect) diseaseSelect.disabled = true;
    status.textContent = "履歴を読み込んでいます。";
    try {
      const release = form.dataset.release;
      index ??= await readJson(new URL(form.dataset.index, window.location.origin), release);
      const history = index.diseases[disease]?.history ?? {};
      const months = (month ? [month] : Object.keys(history).sort()).filter(key => history[key]);
      if (!months.length) {
        output.replaceChildren();
        comparison?.replaceChildren();
        shownMonth = undefined;
        status.textContent = "選択した月の履歴はありません。";
        return;
      }
      const shards = await Promise.all(months.map(key => readJson(dataUrl(history[key].path, dataBase), release)));
      const data = {
        observations: shards.flatMap(shard => shard.observations),
        versions: Object.assign({}, ...shards.map(shard => shard.versions)),
      };
      if (comparison && index.trend && shownMonth !== month) {
        const series = Array.from(diseaseSelect.options, (option, i) => ({
          code: option.value,
          name: option.textContent,
          color: trendColors[i % trendColors.length],
          dash: trendDashes[i % trendDashes.length],
          points: index.trend[option.value]
            .filter(([end]) => !month || end.startsWith(month))
            .map(([end, status, value]) => ({ end, status, value })),
        }));
        comparison.replaceChildren(historyChart(series, true));
        shownMonth = month;
      }
      output.replaceChildren(...historyTable(data, caption, !index.trend));
      if (diseaseSelect) diseaseSelect.parentElement.hidden = false;
      status.textContent = "履歴を表示しました。";
    } catch {
      status.textContent = "履歴を読み込めませんでした。再読み込みしてからもう一度お試しください。";
    } finally {
      button.disabled = false;
      if (diseaseSelect) diseaseSelect.disabled = false;
    }
  });
  if (diseaseSelect) {
    diseaseSelect.addEventListener("change", () => form.requestSubmit());
    form.requestSubmit();
  }
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
