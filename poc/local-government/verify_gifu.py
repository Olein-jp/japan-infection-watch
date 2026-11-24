"""岐阜県のインフルエンザ週報 PDF と Excel の公開集計を照合する。"""

import argparse
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re

import pdfplumber
from pdfminer.pdfexceptions import PDFException
from pdfplumber.utils.exceptions import PdfminerException
import xlrd


HEALTH_CENTERS = ("岐阜市", "岐阜", "西濃", "関", "可茂", "東濃", "恵那", "飛騨")
REGION_COUNT = 1 + len(HEALTH_CENTERS)


def require_unique(matches, description):
    if len(matches) != 1:
        raise ValueError(f"{description}を一意に確認できません")
    return matches[0]


def read_weekly_report(pdf_path):
    with pdfplumber.open(pdf_path) as report:
        if len(report.pages) < 6:
            raise ValueError("週報の対象ページがありません")
        first_page = report.pages[0].extract_text() or ""
        reference_page = report.pages[5].extract_text() or ""

    year, latest_week = map(int, require_unique(re.findall(
        r"(?m)^岐阜県感染症発生動向調査週報（GIDWR） データ・グラフ編 ([0-9]{4})年第([0-9]+)週",
        first_page,
    ), "週報の対象年・週"))
    heading = (
        "◆ インフルエンザ ◆ 新型コロナウイルス感染症\n"
        "定点当たり報告数 定点当たり報告数\n"
        "保健所別 保健所別\n"
        "県全体 県全体\n"
        + " ".join(HEALTH_CENTERS + HEALTH_CENTERS) + "\n"
    )
    first_panel = require_unique(
        re.findall(re.escape(heading) + r"(.*?)\n推移", first_page, re.DOTALL),
        "インフルエンザの保健所別表",
    )
    weeks = tuple(range(latest_week - 2, latest_week + 1))
    rates = {}
    for week, row in zip(weeks, first_panel.splitlines(), strict=True):
        left_panel, separator, _ = row.partition(f" {week}週 ")
        label, *values = left_panel.split()
        if not separator or label != f"{week}週" or len(values) != REGION_COUNT:
            raise ValueError(f"第{week}週の列構成が想定と異なります")
        if not all(re.fullmatch(r"[0-9]+\.[0-9]{2}", value) for value in values):
            raise ValueError(f"第{week}週に非数値があります。原表で表記を確認してください")
        rates[week] = tuple(map(Decimal, values))

    if "保健所\n" not in reference_page or " ".join(HEALTH_CENTERS) not in reference_page:
        raise ValueError("週報の定点数表の地域を確認できません")
    denominator = tuple(map(int, require_unique(
        re.findall(rf"(?m)^ARI((?: [0-9]+){{{REGION_COUNT}}})$", reference_page), "ARI定点数"
    ).split()))
    if 0 in denominator or sum(denominator[1:]) != denominator[0]:
        raise ValueError("ARI定点数の地域と県計を検算できません")
    return year, latest_week, rates, denominator


def check_workbook(xls_path, year, latest_week, pdf_rates, denominator):
    with xlrd.open_workbook(str(xls_path), on_demand=True) as book:
        sheet = book.sheet_by_name("インフルエンザ")
        if (
            sheet.cell_value(2, 1) != "インフルエンザ（ARI定点）"
            or sheet.row_values(3, 1, 7) != ["年", "週 (週初日)", "", "岐阜県計", "", "保健所別"]
            or tuple(sheet.row_values(4, 6, 22)[::2]) != HEALTH_CENTERS
            or sheet.row_values(5, 4, 22) != ["報告数", "定点当"] * REGION_COUNT
        ):
            raise ValueError("Excel の疾患・地域・指標の見出しが想定と異なります")
        rows = list(sheet.get_rows())[6:]
        for week, expected_rates in pdf_rates.items():
            row = require_unique(
                [row for row in rows if (row[1].value, row[2].value) == (year, week)],
                f"Excel の第{week}週の行",
            )
            start = xlrd.xldate_as_datetime(row[3].value, book.datemode).date()
            if start != date.fromisocalendar(year, week, 1):
                raise ValueError(f"第{week}週の週初日が一致しません")
            cells = row[4:22]
            if any(cell.ctype != xlrd.XL_CELL_NUMBER or cell.value < 0 for cell in cells):
                raise ValueError(f"第{week}週に非数値または負数があります")
            counts = [cell.value for cell in cells[::2]]
            if not all(count.is_integer() for count in counts) or sum(counts[1:]) != counts[0]:
                raise ValueError(f"第{week}週の報告数の県計が一致しません")
            if tuple(Decimal(str(cell.value)) for cell in cells[1::2]) != expected_rates:
                raise ValueError(f"第{week}週の定点当たり報告数が一致しません")
            if week == latest_week:
                calculated = tuple(
                    (Decimal(int(count)) / sites).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    for count, sites in zip(counts, denominator, strict=True)
                )
                if calculated != expected_rates:
                    raise ValueError(f"第{week}週の定点数による検算が一致しません")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="県週報のデータ・グラフ編")
    parser.add_argument("xls", type=Path, help="県のインフルエンザ集計（旧 Excel 形式）")
    args = parser.parse_args()
    try:
        year, latest, rates, denominator = read_weekly_report(args.pdf)
        check_workbook(args.xls, year, latest, rates, denominator)
    except (OSError, ValueError, IndexError, PDFException, PdfminerException, xlrd.XLRDError) as error:
        parser.exit(2, f"照合エラー：{error}\n")
    print(f"{year}年の第{min(rates)}〜{latest}週で定点当たり報告数{len(rates) * REGION_COUNT}セルと"
          f"報告数3週の県計、第{latest}週の定点数による検算が一致しました。")


if __name__ == "__main__":
    main()
