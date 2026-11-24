"""厚労省のインフルエンザ様疾患発生報告から当報の集計を抽出する。"""

import argparse
import hashlib
import io
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

import pdfplumber
from pdfminer.pdfexceptions import PDFException
from pdfplumber.utils.exceptions import PdfminerException


REPORT_TITLE = r"インフルエンザ様疾患発生報告\(第([0-9]+)報\)"
TREND_TITLE = "インフルエンザ様疾患発生報告における施設数の推移"
BREAKDOWN_TITLE = r"休業施設数施設別内訳\(第([0-9]+)報\)合計:([0-9,]+)施設"
ERA_DATE = r"R([0-9]+)\.([0-9]+)\.([0-9]+)"
METRICS = {
    "facilities": "施設数",
    "school_closures": "休校数",
    "schools_with_grade_closures": "学年閉鎖学校数",
    "schools_with_class_closures": "学級閉鎖学校数",
    "enrolled": "在籍者数",
    "patients": "患者数",
    "absent_among_patients": "うち欠席者数",
}
FACILITY_TYPES = ("保育所", "幼稚園", "小学校", "中学校", "高等学校", "その他")
TREND_HEADER = ("", "報告週", "報告期間", "休校", "学年閉鎖", "学級閉鎖", "施設数合計")
TREND_KEYS = (
    "school_closures", "schools_with_grade_closures",
    "schools_with_class_closures", "facilities",
)


def compact(text):
    return "".join(unicodedata.normalize("NFKC", text or "").split())


def require_match(pattern, text, description):
    matches = list(re.finditer(pattern, text))
    if len(matches) != 1:
        raise ValueError(f"{description}を一意に確認できません")
    return matches[0]


def reiwa_date(groups):
    year, month, day = map(int, groups)
    if year < 1:
        raise ValueError("令和の日付の年が不正です")
    return date(year + 2018, month, day)


def quantity(cell):
    if cell is None:
        raise ValueError("数値欄の罫線またはセルを確認できません")
    value = unicodedata.normalize("NFKC", cell).strip()
    if value == "...":
        return {"value": None, "status": "unknown_count"}
    if value == "":
        return {"value": None, "status": "blank"}
    if not re.fullmatch(r"(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)", value):
        raise ValueError(f"対応していない数値表記：{cell!r}")
    return {"value": int(value.replace(",", "")), "status": "numeric"}


def verify_sum(parts, total, description):
    if None in parts or total is None:
        return "incomplete"
    if sum(parts) != total:
        raise ValueError(f"{description}が掲載計と一致しません")
    return "matched"


def find_table(page, header):
    tables = [
        table for table in page.extract_tables()
        if table and tuple(map(compact, table[0])) == header
    ]
    if len(tables) != 1:
        raise ValueError(f"PDF {page.page_number}ページで想定の表を一意に確認できません")
    return tables[0]


def regional_rows(table):
    periods = ("", "") + ("今週", "累計") * len(METRICS) + ("",)
    if len(table) != 71 or any(len(row) != len(periods) for row in table):
        raise ValueError("地域表の行数または列数が想定と異なります")
    if tuple(map(compact, table[1])) != periods:
        raise ValueError("地域表の今週・累計の列が想定と異なります")
    if [compact(row[0]) for row in table[-2:]] != ["計", "昨年同期"]:
        raise ValueError("掲載計または昨年同期の位置が想定と異なります")

    rows = []
    for cells in table[2:-1]:
        left, right = map(compact, cells[:2])
        if right:
            if left not in ("", "別掲") or not right.endswith("市"):
                raise ValueError(f"別掲市の表示が想定と異なります：{cells[:2]!r}")
            level, area = "designated_city", right
        elif left == "計":
            level, area = "national", left
        elif left == "北海道" or left.endswith(("都", "府", "県")):
            level, area = "prefecture_reporting_area", left
        else:
            raise ValueError(f"地域表示が想定と異なります：{cells[:2]!r}")

        first_onset = compact(cells[-1])
        if first_onset not in ("", "..."):
            onset = reiwa_date(require_match(
                r"^" + ERA_DATE + r"$", first_onset, "初発年月日"
            ).groups()).isoformat()
        else:
            onset = None
        rows.append({
            "area_level": level,
            "area_label": area,
            "weekly": dict(zip(METRICS, map(quantity, cells[2:-1:2]), strict=True)),
            "cumulative": dict(zip(METRICS, map(quantity, cells[3:-1:2]), strict=True)),
            "first_onset_on": onset,
            "first_onset_status": (
                "date" if onset else {"": "blank", "...": "unknown_count"}[first_onset]
            ),
        })

    expected_levels = ["prefecture_reporting_area"] * 47 + ["designated_city"] * 20 + ["national"]
    if ([row["area_level"] for row in rows] != expected_levels
            or len({row["area_label"] for row in rows}) != len(rows)
            or [compact(row[0]) for row in table[49:69] if compact(row[0])] != ["別掲"]):
        raise ValueError("都道府県47行と別掲市20行の構成を確認できません")
    return rows


def extract(raw, source_url):
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        report_pages = []
        trend_pages = []
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            headings = [compact(line) for line in page_text.splitlines()]
            if any(re.fullmatch(REPORT_TITLE, line) for line in headings):
                report_pages.append((page, compact(page_text)))
            if TREND_TITLE in headings:
                trend_pages.append((page, compact(page_text)))
        if len(report_pages) != 1 or len(trend_pages) != 1:
            raise ValueError("地域表と施設種別のページを一意に特定できません")
        report_page, report_text = report_pages[0]
        trend_page, trend_text = trend_pages[0]

        number = int(require_match(REPORT_TITLE, report_text, "報番号")[1])
        published = reiwa_date(require_match(
            r"令和([0-9]+)年([0-9]+)月([0-9]+)日", report_text, "発表日"
        ).groups())
        week = int(require_match(r"\(第([0-9]+)週\)", report_text, "報告週")[1])
        weekly_dates = require_match("今週" + ERA_DATE + "-" + ERA_DATE, report_text, "今週の期間")
        cumulative_dates = require_match("累計" + ERA_DATE + "-" + ERA_DATE, report_text, "累計の期間")
        start = reiwa_date(weekly_dates.groups()[:3])
        end = reiwa_date(weekly_dates.groups()[3:])
        cumulative_start = reiwa_date(cumulative_dates.groups()[:3])
        cumulative_end = reiwa_date(cumulative_dates.groups()[3:])
        if ((end - start).days != 6 or (start.isocalendar().week, start.weekday()) != (week, 0)
                or cumulative_start > start or cumulative_end != end or published <= end):
            raise ValueError("発表日、報告週、今週と累計の期間の関係が想定と異なります")

        header = ("", "") + tuple(cell for label in METRICS.values() for cell in (label, "")) + ("初発年月日",)
        rows = regional_rows(find_table(report_page, header))
        national = rows[-1]
        comparisons = {
            period: {
                key: verify_sum(
                    [row[period][key]["value"] for row in rows[:-1]],
                    national[period][key]["value"], f"{period}の地域別{label}の合計",
                )
                for key, label in METRICS.items()
            }
            for period in ("weekly", "cumulative")
        }

        trend_table = find_table(trend_page, TREND_HEADER)
        candidates = [row for row in trend_table[1:] if compact(row[0]) == f"第{number}報"]
        if len(candidates) != 1 or len(candidates[0]) != len(TREND_HEADER):
            raise ValueError("推移表で当報の行を一意に確認できません")
        _, trend_week, trend_period, *trend_values = candidates[0]
        trend_dates = require_match(
            "^" + ERA_DATE + "~" + ERA_DATE + "$", compact(trend_period), "推移表の報告期間"
        )
        if (compact(trend_week) != f"第{week}週" or reiwa_date(trend_dates.groups()[:3]) != start
                or reiwa_date(trend_dates.groups()[3:]) != end):
            raise ValueError("推移表の対象週が地域表と一致しません")
        if list(map(quantity, trend_values)) != [national["weekly"][key] for key in TREND_KEYS]:
            raise ValueError("推移表の当報の値が地域表の今週全国計と一致しません")

        breakdown = require_match(BREAKDOWN_TITLE, trend_text, "施設種別の表題")
        breakdown_total = quantity(breakdown[2])["value"]
        if int(breakdown[1]) != number or breakdown_total != national["weekly"]["facilities"]["value"]:
            raise ValueError("施設種別の表題が当報の週次全国計と一致しません")
        facility_table = find_table(trend_page, ("", *FACILITY_TYPES))
        if len(facility_table) != 2 or compact(facility_table[1][0]) != "施設数":
            raise ValueError("施設種別内訳の行が想定と異なります")
        facilities = dict(zip(FACILITY_TYPES, map(quantity, facility_table[1][1:]), strict=True))
        facility_check = verify_sum(
            [cell["value"] for cell in facilities.values()], breakdown_total, "施設種別の合計",
        )

        return {
            "source_url": source_url,
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "published_on": published.isoformat(),
            "report_number": number,
            "reporting_year": start.isocalendar().year,
            "reporting_week": week,
            "weekly_start": start.isoformat(),
            "weekly_end": end.isoformat(),
            "cumulative_start": cumulative_start.isoformat(),
            "cumulative_end": cumulative_end.isoformat(),
            "regional_page": report_page.page_number,
            "facility_page": trend_page.page_number,
            "regional_rows": rows,
            "national_weekly_facilities_by_type": facilities,
            "checks": {"regional_sum": comparisons, "facility_sum": facility_check},
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="厚労省の公式配布 PDF")
    parser.add_argument("--source-url", required=True, help="PDF の配布 URL")
    args = parser.parse_args()
    try:
        url = urlsplit(args.source_url)
        if (url.scheme, url.netloc) != ("https", "www.mhlw.go.jp") or not url.path.endswith(".pdf"):
            raise ValueError("厚労省の公式 PDF URL を指定してください")
        result = extract(args.pdf.read_bytes(), args.source_url)
    except (OSError, ValueError, PDFException, PdfminerException) as error:
        parser.exit(2, f"抽出エラー：{error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
