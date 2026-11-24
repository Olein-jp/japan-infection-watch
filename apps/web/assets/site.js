const statuses = {
  blank: "空欄",
  dash: "原表ハイフン",
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
  table.append(element("caption", "週別の報告件数と定点当たり報告数"));
  const head = table.createTHead().insertRow();
  for (const name of ["対象期間", "報告件数（件）", "定点当たり（件／定点）", "原表作成日", "取得日時（架空）"]) {
    const cell = element("th", name);
    cell.scope = "col";
    head.append(cell);
  }
  const tbody = table.createTBody();
  const chart = element("div");
  chart.className = "trend";
  chart.setAttribute("aria-hidden", "true");
  chart.append(element("p", "定点当たり報告数の推移"));
  const reportedRates = [...weeks.values()].flatMap(week => {
    const rate = week.cells.sentinel_reports_per_site;
    return rate?.value_status === "reported" ? [Number(rate.value)] : [];
  });
  const scale = Math.max(1, ...reportedRates);

  for (const [end, week] of weeks) {
    const row = tbody.insertRow();
    const period = element("th", `${week.start}〜${end}`);
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
    const provenance = data.versions[week.version];
    row.append(element("td", provenance.source_created_on), element("td", provenance.retrieved_at));
    const rate = week.cells.sentinel_reports_per_site;
    const barRow = element("div");
    barRow.className = "trend-row";
    const track = element("span");
    track.className = "trend-track";
    const bar = element("span");
    const present = rate?.value_status === "reported";
    if (present) {
      bar.style.width = `${Number(rate.value) / scale * 100}%`;
      track.append(bar);
    }
    barRow.append(element("span", end), track, element("span", present ? rate.value : statuses[rate?.value_status] ?? "データなし"));
    chart.append(barRow);
  }
  const scroll = element("div");
  scroll.className = "table-scroll";
  scroll.tabIndex = 0;
  scroll.setAttribute("role", "region");
  scroll.setAttribute("aria-label", "週次履歴の表");
  scroll.append(table);
  const hint = element("p", "画面が狭い場合は表を横にスクロールできます。");
  hint.className = "table-hint";
  return [heading, chart, hint, scroll];
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
    const month = form.elements.month.value;
    const diseaseSelect = form.elements.disease;
    const disease = diseaseSelect ? diseaseSelect.value : form.dataset.disease;
    const caption = diseaseSelect ? `${diseaseSelect.selectedOptions[0].textContent} · ${month}` : month;
    button.disabled = true;
    status.textContent = "履歴を読み込んでいます。";
    try {
      const release = form.dataset.release;
      index ??= await readJson(new URL(form.dataset.index, window.location.origin), release);
      const reference = index.diseases[disease]?.history[month];
      if (!reference) {
        output.replaceChildren();
        status.textContent = "選択した月の履歴はありません。";
        return;
      }
      const data = await readJson(dataUrl(reference.path, dataBase), release);
      output.replaceChildren(...historyTable(data, caption));
      status.textContent = "履歴を表示しました。";
    } catch {
      status.textContent = "履歴を読み込めませんでした。再読み込みしてからもう一度お試しください。";
    } finally {
      button.disabled = false;
    }
  });
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
