"""F-001 と F-002 の確認に使う架空の週次 CSV。"""

import csv
import io

from packages.data_normalizer.jihs_csv import AREAS, TITLE
from packages.data_normalizer.jihs_weekly import DISEASE_IDS


def fixture_table():
    headers = [""] + [label for name in DISEASE_IDS for label in (name, "")]
    units = [""] + ["報告", "定当"] * 19
    table = [
        [TITLE] + [""] * 38,
        ["2030年2週(1月7日〜1月13日)", "2030年1月15日作成"] + [""] * 37,
        headers,
        units,
    ]
    table.extend([area] + ["000", "0.00"] * 19 for area in AREAS)
    table[5][1:3] = ["-", ""]
    table[6][1:3] = ["", "-"]
    table[7][1:3] = ["12", "1.70"]
    return table


def csv_bytes(table):
    stream = io.StringIO(newline="")
    csv.writer(stream).writerows(table)
    return stream.getvalue().encode("shift_jis")
