"""F-001 の架空観測からローカル確認用の静的サイトを生成する。"""

import argparse
from datetime import datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory

from apps.web.preview_data import (
    ATTRIBUTION, DISEASES, METRIC_IDS, MUNICIPALITIES, OFFICIAL_SOURCE, REGIONS,
    json_bytes, parse_timestamp, prepare, write_distribution,
)


SITE = "感染症動向ウォッチ"
STATUS = {
    "blank": "空欄", "dash": "原表ハイフン", "unknown_count": "計数不明",
    "not_reported": "未報告", "suppressed": "秘匿", "not_applicable": "対象外",
}
METRIC_HEADERS = "<th scope=\"col\">報告件数（件）</th><th scope=\"col\">定点当たり（件／定点）</th>"


def layout(base, title, content, *, wide_title=False):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {SITE}</title>
<link rel="stylesheet" href="{base}assets/site.css">
<script type="module" src="{base}assets/site.js"></script>
</head>
<body>
<a href="#main" class="skip">本文へ移動</a>
<header class="masthead"><div class="shell masthead-inner">
<a class="brand" href="{base}">{SITE}</a>
<nav aria-label="主要メニュー"><a href="{base}#regions">地域</a><a href="{base}#diseases">疾患</a><a href="{base}sources/">出典</a></nav>
</div></header>
<div class="notice"><div class="shell">開発プレビュー · 画面内の数値は架空です</div></div>
<main id="main" class="shell" tabindex="-1">
<header class="page-title{' hero' if wide_title else ''}"><h1>{escape(title)}</h1></header>
{content}
</main>
<footer class="shell footer"><a href="{base}sources/">出典とデータの見方</a></footer>
</body>
</html>
"""


def table(caption, first_column, entries, *, extra=""):
    hint = '<p class="table-hint">画面が狭い場合は表を横にスクロールできます。</p>' if extra else ""
    return (hint + f'<div class="table-scroll" tabindex="0" role="region" aria-label="{escape(caption)}">'
            f'<table><caption>{escape(caption)}</caption><thead><tr><th scope="col">{first_column}</th>'
            f'{METRIC_HEADERS}{extra}</tr></thead><tbody>{"".join(entries)}</tbody></table></div>')


def values(cells):
    result = []
    for metric in METRIC_IDS:
        cell = cells.get(metric)
        if cell is None:
            label = "データなし"
        elif cell["value_status"] == "reported":
            result.append(f'<td class="number">{escape(str(cell["value"]))}</td>')
            continue
        else:
            label = STATUS[cell["value_status"]]
        result.append(f'<td class="missing">{label}</td>')
    return "".join(result)


def data_note(version, latest, timestamp):
    sample = latest["jp", next(iter(DISEASES))][METRIC_IDS[0]]
    return f"""<dl class="provenance">
<div><dt>対象週</dt><dd>{version["reporting_year"]}年第{version["reporting_week"]}週（{sample["period_start"]}〜{sample["period_end"]}）</dd></div>
<div><dt>資料区分</dt><dd>週次定点・速報形式</dd></div>
<div><dt>原表の作成日</dt><dd>{escape(version["source_created_on"])}</dd></div>
<div><dt>表示版の取得日時（架空）</dt><dd>{escape(version["retrieved_at"])}</dd></div>
<div><dt>サイト生成日時</dt><dd>{escape(timestamp)}</dd></div>
<div><dt>出典</dt><dd>{ATTRIBUTION} · <a href="{OFFICIAL_SOURCE}">公式 IDWR</a></dd></div>
</dl>"""


def history_form(base, index, release, months, disease=None):
    disease_input = ""
    if disease is None:
        options = "".join(f'<option value="{code}">{escape(name)}</option>' for code, name in DISEASES.items())
        disease_input = f'<label>疾患<select name="disease">{options}</select></label>'
    month_options = "".join(f'<option>{month}</option>' for month in sorted(months, reverse=True))
    return f"""<section aria-labelledby="history-heading" class="panel history">
<h2 id="history-heading">週次の履歴</h2>
<form class="history-form" data-index="{base}data/{index["path"]}" data-release="{release}"
      data-base="{base}data/" data-disease="{disease or ''}" hidden>
{disease_input}
<label>対象月<select name="month">{month_options}</select></label>
<button type="submit">週次履歴を表示</button>
</form>
<p class="history-status" role="status"></p><div class="history-output"></div>
<noscript>履歴の読み込みには JavaScript が必要です。最新の集計は上の表で確認できます。</noscript>
</section>"""


def pages(root, base, release, timestamp, latest, history, version, indexes):
    def emit(target, title, content, *, hero=False):
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(layout(base, title, content, wide_title=hero), encoding="utf-8")

    note = data_note(version, latest, timestamp)
    entries = []
    for disease, label in DISEASES.items():
        link = f'<a href="{base}diseases/{disease}/">{escape(label)}</a>'
        entries.append(f'<tr><th scope="row">{link}</th>{values(latest["jp", disease])}</tr>')
    national = table("全国の週次集計", "疾患", entries)
    links = "".join(f'<li><a href="{base}prefectures/{code}/">{name}</a></li>' for code, name in REGIONS.items() if code != "jp")
    emit("index.html", "全国の感染症動向", f"""
{note}
<section id="diseases" class="panel"><h2>疾患別の最新値</h2>{national}</section>
<section id="regions" class="panel"><h2>都道府県を選ぶ</h2>
<label class="region-filter" hidden>都道府県名で絞り込む<input type="search" autocomplete="off"></label>
<p class="region-status" role="status"></p><ul class="region-list">{links}</ul></section>
<section class="panel"><h2>市区町村の公式案内</h2><a href="{base}municipalities/21201/">岐阜市の公式案内</a></section>
""", hero=True)

    for code, name in REGIONS.items():
        if code == "jp":
            continue
        rows = []
        for disease, label in DISEASES.items():
            link = f'<a href="{base}diseases/{disease}/">{escape(label)}</a>'
            rows.append(f'<tr><th scope="row">{link}</th>{values(latest[code, disease])}{values(latest["jp", disease])}</tr>')
        cols = '<th scope="col">全国の報告件数（件）</th><th scope="col">全国の定点当たり（件／定点）</th>'
        local = table(f"{name}と全国の最新値（同じ対象週）", "疾患", rows, extra=cols)
        months = {month for disease in DISEASES for month in history[code, disease]}
        guide = f'<p><a href="{base}municipalities/21201/">岐阜市の公式案内</a></p>' if code == "21" else ""
        emit(f"prefectures/{code}/index.html", name,
             f'{note}<section class="panel"><h2>週次の最新値</h2>{local}{guide}</section>'
             + history_form(base, indexes[code], release, months))

    for disease, label in DISEASES.items():
        rows = []
        for code, name in REGIONS.items():
            link = name if code == "jp" else f'<a href="{base}prefectures/{code}/">{name}</a>'
            rows.append(f'<tr><th scope="row">{link}</th>{values(latest[code, disease])}</tr>')
        comparison = table("同じ対象週の全国・都道府県の比較", "地域", rows)
        emit(f"diseases/{disease}/index.html", label,
             f'{note}<section class="panel"><h2>全国と都道府県の最新値</h2>{comparison}</section>'
             + history_form(base, indexes["jp"], release, history["jp", disease], disease))

    for code, (name, pref, label, url) in MUNICIPALITIES.items():
        emit(f"municipalities/{code}/index.html", name, f"""
<section class="panel"><h2>市の公式案内</h2>
<p>このページに{name}の集計はありません。</p>
<ul><li><a href="{url}">{name}公式サイト「{label}」</a></li>
<li><a href="{base}prefectures/{pref}/">{REGIONS[pref]}の週次集計（都道府県単位）</a></li></ul></section>
""")

    emit("sources/index.html", "出典とデータの見方", f"""
<section class="panel"><h2>情報源</h2><p>{ATTRIBUTION}。</p>
<p><a href="{OFFICIAL_SOURCE}">国立健康危機管理研究機構の感染症発生動向調査週報（IDWR）</a></p>
<p><a href="{base}municipalities/21201/">岐阜市の公式案内</a></p></section>
<section class="panel"><h2>指標と欠損</h2><p>報告件数は定点からの報告の件数です。定点当たり報告数は出典の表示精度のまま掲載します。
定点数が提供されていない場合は逆算しません。</p>
<p>数値の 0 と、空欄や原表のハイフンは分けて表示します。ハイフンの意味は原表の定義が得られるまで未確認とします。</p></section>
""")
    emit("404.html", "ページが見つかりません",
         f'<section class="panel"><p><a href="{base}">全国のページへ戻る</a></p></section>')


def build(inputs, output, *, base, generated_at):
    if not re.fullmatch(r"/(?:[a-zA-Z0-9][a-zA-Z0-9_-]*/)*", base):
        raise ValueError("基準パスは / で始まり / で終わるサイト内のパスを指定してください")
    if output.exists() or output.is_symlink():
        raise ValueError("出力先が存在します。新しいディレクトリを指定してください")
    timestamp = parse_timestamp(generated_at).isoformat()
    latest, history, version, versions = prepare(inputs)
    # 同じ日時で再生成した場合にも、異なるデータを同じ版として扱わない。
    release = "preview-" + sha256(json_bytes([timestamp, inputs])).hexdigest()[:20]
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as scratch:
        candidate = Path(scratch) / "site"
        shutil.copytree(Path(__file__).parent / "assets", candidate / "assets")
        indexes = write_distribution(candidate, release, timestamp, latest, history, version, versions)
        pages(candidate, base, release, timestamp, latest, history, version, indexes)
        candidate.rename(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="F-001 が出力した架空観測 JSON（各週1ファイル）")
    parser.add_argument("--output", type=Path, required=True, help="新規の出力ディレクトリ")
    parser.add_argument("--base", default="/japan-infection-watch/")
    parser.add_argument("--generated-at", default=datetime.now().astimezone().isoformat(timespec="seconds"))
    args = parser.parse_args()
    try:
        inputs = [json.loads(path.read_text(encoding="utf-8")) for path in args.inputs]
        build(inputs, args.output, base=args.base, generated_at=args.generated_at)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f"静的生成エラー：{error}\n")


if __name__ == "__main__":
    main()
