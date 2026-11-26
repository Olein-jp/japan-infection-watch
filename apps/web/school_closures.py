"""厚労省の週次 PDF から抽出した学校休業の集計をローカルで表示する。"""

from datetime import date
from html import escape
import re

from apps.web.preview_data import REGIONS, history_start


METRICS = (
    ("schools_with_class_closures", "学級閉鎖"),
    ("schools_with_grade_closures", "学年閉鎖"),
    ("school_closures", "休校"),
)
MISSING = {"blank": "空欄", "unknown_count": "計数不明"}


def prepare(reports):
    names = set(REGIONS.values()) - {"全国"}
    weeks = {}
    for report in reports:
        start = date.fromisoformat(report["weekly_start"])
        end = date.fromisoformat(report["weekly_end"])
        year, week, _ = end.isocalendar()
        if ((year, week) != (report["reporting_year"], report["reporting_week"])
                or start != date.fromisocalendar(year, week, 1)
                or end != date.fromisocalendar(year, week, 7)
                or end in weeks):
            raise ValueError("学校休業の報告週が不正か、同じ週の報告が重複しています")
        url = report["source_url"]
        page = report["regional_page"]
        if (not re.fullmatch(r"https://www\.mhlw\.go\.jp/content/[0-9]+\.pdf", url)
                or type(page) is not int or page < 1):
            raise ValueError("学校休業の出典が厚生労働省の PDF と一致しません")
        regions = {}
        for row in report["regional_rows"]:
            if row["area_level"] != "prefecture_reporting_area":
                continue
            name = row["area_label"]
            if name in regions:
                raise ValueError("学校休業の都道府県報告区分が重複しています")
            cells = tuple(row["weekly"][key] for key, _ in METRICS)
            for cell in cells:
                value = cell["value"]
                status = cell["status"]
                if not ((status == "numeric" and type(value) is int and value >= 0)
                        or (status in MISSING and value is None)):
                    raise ValueError("学校休業の施設数または欠損区分が不正です")
            regions[name] = cells
        if regions.keys() != names:
            raise ValueError("学校休業の都道府県報告区分が揃っていません")
        weeks[end] = (start, end, week, f"{url}#page={page}", regions)
    if not weeks:
        return []
    first = history_start(max(weeks))
    return [weeks[end] for end in sorted(weeks) if end >= first]


def chart(reports, name):
    if not reports:
        return ""
    scale = max(1, *(cell["value"] or 0 for _, _, _, _, regions in reports for cell in regions[name]))
    weeks = []
    for start, end, week, source, regions in reports:
        lines = []
        for (_, label), cell in zip(METRICS, regions[name], strict=True):
            value = cell["value"]
            if value is None:
                bar, text = "", MISSING[cell["status"]]
            else:
                bar = f'<span style="width:{value / scale:.2%}"></span>'
                text = f"{value:,}施設"
            lines.append(f'<dt>{label}</dt><dd><span class="closure-track" aria-hidden="true">{bar}</span>{text}</dd>')
        weeks.append(
            f'<div class="closure-week"><h3>{end.isocalendar().year}年第{week}週（{start:%m/%d}〜{end:%m/%d}）</h3>'
            f'<dl>{"".join(lines)}</dl><p><a href="{escape(source, quote=True)}">第{week}週の原表（PDF）</a></p></div>'
        )
    return (
        f'<p>インフルエンザ様疾患による措置を実施した施設数（{escape(name)}の報告区分）。'
        '厚生労働省の週次集計を表示用に整形しています。</p>'
        f'<div class="closure-chart">{"".join(weeks)}</div>'
        '<p class="table-note">原表で別掲の市はこの集計に加えていません。</p>'
    )
