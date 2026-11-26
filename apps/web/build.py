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
    ATTRIBUTION, DISEASES, HISTORY_MONTHS, LOCAL_ATTRIBUTION, LOCAL_PROCESSING, METRIC_IDS, MUNICIPALITIES,
    OFFICIAL_ARCHIVE, OFFICIAL_SOURCE, REGIONS, SCHOOL_HEALTH_MAP,
    json_bytes, parse_timestamp, prepare, write_distribution,
)
from apps.web import school_closures


SITE = "感染症動向ウォッチ"
JIHS_PROVISIONAL = "JIHS の速報値は、後日の週報・年報で訂正されることがあります。"
STATUS = {
    "blank": "空欄", "dash": "-", "unknown_count": "計数不明",
    "not_reported": "未報告", "suppressed": "秘匿", "not_applicable": "対象外",
}
METRIC_HEADERS = "<th scope=\"col\">報告件数（件）</th><th scope=\"col\">医療機関1か所あたり（件）</th>"
MUNICIPAL_CLOSURES = ("https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/"
                      "viz/____16744492330710/1?%E7%96%BE%E6%82%A3%E3%83%BB%E7%97%87%E7%8A%B6%E3%81%AE%E5%8C%BA%E5%88%86=3")
MHLW_SCHOOL_REPORTS = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/kenkou/kekkaku-kansenshou01/houdou.html"
GAP_NOTE = '<p class="table-note"><span class="missing">-</span> は原表の表記です。報告数の 0 とは区別しています。</p>'


def layout(base, title, content, *, notice, asset_versions, wide_title=False, trail=None):
    breadcrumbs = ""
    if trail is not None:
        links = "".join(f'<li><a href="{base}{path}">{escape(label)}</a></li>'
                        for path, label in (("", "トップ"), *trail))
        breadcrumbs = (f'<nav class="breadcrumbs" aria-label="パンくずリスト">'
                       f'<ol>{links}<li aria-current="page">{escape(title)}</li></ol></nav>')
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {SITE}</title>
<link rel="stylesheet" href="{base}assets/site.css?v={asset_versions["site.css"]}">
<script type="module" src="{base}assets/site.js?v={asset_versions["site.js"]}"></script>
</head>
<body>
<a href="#main" class="skip">本文へ移動</a>
<header class="masthead"><div class="shell masthead-inner">
<a class="brand" href="{base}">{SITE}</a>
<nav aria-label="主要メニュー"><a href="{base}#regions">地域</a><a href="{base}#diseases">疾患</a><a href="{base}sources/">出典</a></nav>
</div></header>
<div class="notice"><div class="shell">{notice}</div></div>
<main id="main" class="shell" tabindex="-1">
{breadcrumbs}
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
            f'{METRIC_HEADERS}{extra}</tr></thead><tbody>{"".join(entries)}</tbody></table></div>{GAP_NOTE}')


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


def data_note(version, latest, timestamp, *, real_data, release_candidate):
    sample = latest["jp", next(iter(DISEASES))][METRIC_IDS[0]]
    attribution = LOCAL_ATTRIBUTION if real_data else ATTRIBUTION
    source = version["source_url"] if real_data else OFFICIAL_SOURCE
    date_label = "CSV の読み込み日時" if real_data else "表示版の取得日時（架空）"
    edition = "週次・速報値" if real_data else "週次・速報形式"
    processing = f"<div><dt>編集・加工</dt><dd>{LOCAL_PROCESSING}。</dd></div>" if real_data else ""
    correction = f'<p class="table-note">{JIHS_PROVISIONAL}</p>' if release_candidate else ""
    return f"""<dl class="provenance">
<div><dt>対象週</dt><dd>{version["reporting_year"]}年第{version["reporting_week"]}週（{sample["period_start"]}〜{sample["period_end"]}）</dd></div>
<div><dt>資料区分</dt><dd>{edition}</dd></div>
<div><dt>原表の作成日</dt><dd>{escape(version["source_created_on"])}</dd></div>
<div><dt>{date_label}</dt><dd>{escape(version["retrieved_at"])}</dd></div>
<div><dt>サイト生成日時</dt><dd>{escape(timestamp)}</dd></div>
<div><dt>出典</dt><dd>{attribution} · <a href="{source}">公式 IDWR</a></dd></div>
{processing}
</dl>{correction}"""


def history_form(base, index, release, months, covered_period, disease=None, *, real_data):
    disease_input = ""
    if disease is None:
        options = "".join(
            f'<option value="{code}"{" selected" if code == "influenza" else ""}>{escape(name)}</option>'
            for code, name in DISEASES.items()
        )
        disease_input = (f'<div class="history-field history-detail" hidden><label for="history-disease">詳細表の疾患</label>'
                         f'<select id="history-disease">{options}</select></div>')
    comparison = '<div class="history-comparison"></div>' if disease is None else ""
    month_options = "".join(f'<option>{month}</option>' for month in sorted(months, reverse=True))
    archive_label = ("JIHS の速報一覧でほかの報告週を見る" if real_data
                     else f"{HISTORY_MONTHS}か月より前のデータは JIHS で見る")
    return f"""<section aria-labelledby="history-heading" class="panel history">
<h2 id="history-heading">週次の推移</h2>
<p>収録期間 <time>{covered_period[0]}</time>〜<time>{covered_period[1]}</time></p>
<form class="history-form" data-index="{base}data/{index["path"]}" data-release="{release}"
      data-base="{base}data/" data-disease="{disease or ''}" hidden>
<div class="history-field"><label for="history-month">対象月</label>
<select id="history-month" name="month"><option value="">収録期間すべて（最長{HISTORY_MONTHS}か月）</option>{month_options}</select></div>
<button type="submit">週次履歴を表示</button>
</form>
<p class="history-status" role="status"></p>
{comparison}{disease_input}<div class="history-output"></div>
<noscript>推移の表示には JavaScript が必要です。このページの表で最新の集計を確認できます。</noscript>
<p><a href="{OFFICIAL_ARCHIVE}">{archive_label}</a></p>
</section>"""


def pages(root, base, release, timestamp, latest, history, version, indexes, *,
          local_only, release_candidate, closure_reports):
    real_data = local_only or release_candidate
    asset_versions = {name: sha256((root / "assets" / name).read_bytes()).hexdigest()[:12]
                      for name in ("site.css", "site.js")}
    notice = "開発プレビュー · 画面内の数値は架空です"
    if local_only:
        notice = "自分用・ローカル閲覧 · JIHS の速報値"
    if release_candidate:
        notice = "JIHS の週次定点速報"

    def emit(target, title, content, *, hero=False, trail=()):
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(layout(base, title, content, notice=notice, asset_versions=asset_versions, wide_title=hero,
                               trail=None if target == "index.html" else trail), encoding="utf-8")

    note = data_note(version, latest, timestamp, real_data=real_data, release_candidate=release_candidate)
    attribution = LOCAL_ATTRIBUTION if real_data else ATTRIBUTION
    processing = f"<p>編集・加工　{LOCAL_PROCESSING}。</p>" if real_data else ""
    sample_key = ("jp", next(iter(DISEASES)))
    first_row = next(iter(history[sample_key].values()))[0]
    covered_period = (first_row["period_start"], latest[sample_key][METRIC_IDS[0]]["period_end"])
    school_map = f'<a href="{SCHOOL_HEALTH_MAP}">日本学校保健会の感染症情報マップ</a>'
    school_municipal = f'<a href="{MUNICIPAL_CLOSURES}">市区町村別の学級閉鎖（インフルエンザ）</a>'
    school_reports = f'<a href="{MHLW_SCHOOL_REPORTS}">厚生労働省のインフルエンザ様疾患発生報告</a>'
    municipal_guides = {
        code: f'<a href="{base}municipalities/{code}/">{escape(name)}の公式案内</a>'
        for code, (name, _, _, _) in MUNICIPALITIES.items()
    }
    all_municipal_guides = "".join(f"<li>{link}</li>" for link in municipal_guides.values())
    municipal_closure_guide = (
        f'<p>{school_municipal}。日本学校保健会の公式グラフで自治体を選べます。</p>'
    )
    school_links = f"""
{municipal_closure_guide}
<ul>
<li>{school_map}で、ほかの疾患の学級閉鎖なども確認できます。</li>
<li>{school_reports}で、インフルエンザ様疾患による学級閉鎖・学年閉鎖・休校を実施した施設数を週ごとに確認できます。</li>
</ul>"""
    entries = []
    for disease, label in DISEASES.items():
        link = f'<a href="{base}diseases/{disease}/">{escape(label)}</a>'
        entries.append(f'<tr><th scope="row">{link}</th>{values(latest["jp", disease])}</tr>')
    national = table("全国の週次集計", "疾患", entries)
    links = "".join(f'<li><a href="{base}prefectures/{code}/">{name}</a></li>' for code, name in REGIONS.items() if code != "jp")
    emit("index.html", "全国の感染症動向", f"""
<section id="regions" class="panel"><h2>都道府県を選ぶ</h2>
{municipal_closure_guide}
<label class="region-filter" hidden>都道府県名で絞り込む<input type="search" autocomplete="off"></label>
<p class="region-status" role="status"></p><ul class="region-list">{links}</ul></section>
{note}
<section id="diseases" class="panel"><h2>疾患別の最新値</h2>{national}</section>
<section class="panel"><h2>学校・市区町村の公式案内</h2>
<ul><li>{school_map}</li>{all_municipal_guides}</ul></section>
""", hero=True)

    for code, name in REGIONS.items():
        if code == "jp":
            continue
        rows = []
        for disease, label in DISEASES.items():
            link = f'<a href="{base}diseases/{disease}/">{escape(label)}</a>'
            rows.append(f'<tr><th scope="row">{link}</th>{values(latest[code, disease])}{values(latest["jp", disease])}</tr>')
        cols = '<th scope="col">全国の報告件数（件）</th><th scope="col">全国の医療機関1か所あたり（件）</th>'
        local = table(f"{name}と全国の最新値（同じ対象週）", "疾患", rows, extra=cols)
        months = {month for disease in DISEASES for month in history[code, disease]}
        guides = "".join(
            f"<p>{municipal_guides[municipality]}</p>"
            for municipality, (_, prefecture, _, _) in MUNICIPALITIES.items()
            if prefecture == code
        )
        closures = f"""
<section class="panel" id="school-closures" aria-labelledby="school-closures-heading">
<h2 id="school-closures-heading">学級閉鎖・休校</h2>
{school_closures.chart(closure_reports, name)}
{school_links}
</section>"""
        emit(f"prefectures/{code}/index.html", name,
             '<p><a href="#school-closures">学級閉鎖・休校の情報を見る</a></p>'
             + history_form(base, indexes[code], release, months, covered_period, real_data=real_data)
             + closures
             + f'{note}<section class="panel"><h2>週次の最新値</h2>{local}{guides}</section>',
             trail=(("#regions", "都道府県"),))

    for disease, label in DISEASES.items():
        rows = []
        for code, name in REGIONS.items():
            link = name if code == "jp" else f'<a href="{base}prefectures/{code}/">{name}</a>'
            rows.append(f'<tr><th scope="row">{link}</th>{values(latest[code, disease])}</tr>')
        comparison = table("同じ対象週の全国・都道府県の比較", "地域", rows)
        emit(f"diseases/{disease}/index.html", label,
             f'{note}<section class="panel"><h2>全国と都道府県の最新値</h2>{comparison}</section>'
             + history_form(base, indexes["jp"], release, history["jp", disease], covered_period, disease,
                            real_data=real_data),
             trail=(("#diseases", "疾患"),))

    for code, (name, pref, label, url) in MUNICIPALITIES.items():
        emit(f"municipalities/{code}/index.html", name, f"""
<section class="panel"><h2>市の公式案内</h2>
{municipal_closure_guide}
<p>このページに{name}の集計はありません。</p>
<ul><li><a href="{url}">{name}公式サイト「{label}」</a></li>
<li><a href="{base}prefectures/{pref}/">{REGIONS[pref]}の週次集計（都道府県単位）</a></li></ul></section>
""", trail=(("#regions", "都道府県"), (f"prefectures/{pref}/", REGIONS[pref])))

    emit("sources/index.html", "出典とデータの見方", f"""
<section class="panel"><h2>情報源</h2><p>{attribution}。</p>
{processing}
<p><a href="{OFFICIAL_SOURCE}">国立健康危機管理研究機構の感染症発生動向調査週報（IDWR）</a></p>
<p>{school_map}</p>
<p>{school_reports}</p>
{municipal_closure_guide}
<ul>{all_municipal_guides}</ul></section>
<section class="panel"><h2>指標と欠損</h2><p>報告件数は、週ごとの報告を担当する医療機関からの報告の合計です。
「医療機関1か所あたり」は、報告を担当する医療機関（定点）1か所あたりの報告数です。出典にある「定点当たり報告数」を同じ精度で掲載しています。</p>
<p>数値の 0、空欄、原表にハイフンがある場合の「-」は区別します。</p></section>
""")
    emit("404.html", "ページが見つかりません",
         f'<section class="panel"><p><a href="{base}">全国のページへ戻る</a></p></section>')


def build(inputs, output, *, base, generated_at, local_only=False, release_candidate=False, closure_reports=()):
    if not re.fullmatch(r"/(?:[a-zA-Z0-9][a-zA-Z0-9_-]*/)*", base):
        raise ValueError("基準パスは / で始まり / で終わるサイト内のパスを指定してください")
    if output.exists() or output.is_symlink():
        raise ValueError("出力先が存在します。新しいディレクトリを指定してください")
    if local_only and release_candidate:
        raise ValueError("ローカル閲覧版と公開候補版は同時に指定できません")
    if closure_reports and not local_only:
        raise ValueError("学校休業の実集計はローカル閲覧専用です")
    timestamp = parse_timestamp(generated_at).isoformat()
    fictional = not (local_only or release_candidate)
    latest, history, version, versions = prepare(inputs, fictional=fictional)
    school_weeks = school_closures.prepare(closure_reports)
    # 同じ日時で再生成した場合にも、異なるデータを同じ版として扱わない。
    prefix = "candidate-" if release_candidate else ("local-" if local_only else "preview-")
    release = prefix + sha256(
        json_bytes([timestamp, HISTORY_MONTHS, inputs, *closure_reports])
    ).hexdigest()[:20]
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as scratch:
        candidate = Path(scratch) / "site"
        shutil.copytree(Path(__file__).parent / "assets", candidate / "assets")
        indexes = write_distribution(candidate, release, timestamp, latest, history, version, versions,
                                     fictional=fictional, release_candidate=release_candidate)
        pages(candidate, base, release, timestamp, latest, history, version, indexes, local_only=local_only,
              release_candidate=release_candidate, closure_reports=school_weeks)
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
