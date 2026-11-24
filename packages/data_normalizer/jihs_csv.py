"""R-09 で確認した週次定点 CSV の共通パーサー。"""

import csv
import hashlib
import io
import re
from datetime import date


TITLE = "報告数・定点当り報告数、疾病・都道府県別"
AREAS = tuple("""
総数 北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 群馬県
埼玉県 千葉県 東京都 神奈川県 新潟県 富山県 石川県 福井県 山梨県 長野県
岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 和歌山県
鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 福岡県
佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県
""".split())
WEEK_LABEL = re.compile(
    r"([0-9]{4})年([0-9]{1,2})週\(([0-9]{1,2})月([0-9]{1,2})日"
    r"[〜～]([0-9]{1,2})月([0-9]{1,2})日\)"
)
CREATED_LABEL = re.compile(r"([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日作成")
COUNT = re.compile(r"[0-9]+")
RATE = re.compile(r"[0-9]+\.[0-9]{2}")
SPECIAL_VALUES = {"": "blank", "-": "dash"}


def observation(raw, pattern, location):
    if raw in SPECIAL_VALUES:
        return {"value": None, "status": SPECIAL_VALUES[raw], "source_token": raw}
    if not pattern.fullmatch(raw):
        raise ValueError(f"{location}：未対応の値 {raw!r}")
    value = int(raw) if pattern is COUNT else raw
    return {"value": value, "status": "numeric", "source_token": raw}


def parse_weekly_csv(raw):
    with io.StringIO(raw.decode("shift_jis"), newline="") as stream:
        rows = [row for row in csv.reader(stream, strict=True) if any(row)]
    if len(rows) != 4 + len(AREAS) or any(len(row) != 39 for row in rows):
        raise ValueError("CSV の行数または列数が対応する形式と異なります")

    title, metadata, headers, units, *data_rows = rows
    if title[0] != TITLE or any(title[1:]) or any(metadata[2:]):
        raise ValueError("週次定点速報の表題・メタデータを確認できません")
    week_label = WEEK_LABEL.fullmatch(metadata[0])
    created_label = CREATED_LABEL.fullmatch(metadata[1])
    if week_label is None or created_label is None:
        raise ValueError("対象週または作成日を確認できません")

    year, week, start_month, start_day, end_month, end_day = map(int, week_label.groups())
    start = date.fromisocalendar(year, week, 1)
    end = date.fromisocalendar(year, week, 7)
    if (start.month, start.day, end.month, end.day) != (start_month, start_day, end_month, end_day):
        raise ValueError("対象週の番号と期間が一致しません")
    created = date(*map(int, created_label.groups()))
    diseases = headers[1::2]
    if headers[0] or any(headers[2::2]) or not all(diseases) or len(set(diseases)) != 19:
        raise ValueError("疾患見出しに空欄、重複、または未対応の構造があります")
    if units != [""] + ["報告", "定当"] * len(diseases):
        raise ValueError("指標の見出しが対応する形式と異なります")
    if {row[0] for row in data_rows} != set(AREAS):
        raise ValueError("全国と47都道府県を重複なく確認できません")

    records = []
    for area, *values in data_rows:
        area_level = "national" if area == "総数" else "prefecture"
        for index, disease in enumerate(diseases):
            count, rate = values[2 * index:2 * index + 2]
            records.append({
                "area_level": area_level,
                "area_label": area,
                "disease_label": disease,
                "report_count": observation(count, COUNT, f"{area}・{disease}・報告"),
                "reports_per_sentinel": observation(rate, RATE, f"{area}・{disease}・定当"),
            })

    return {
        "source_stage": "provisional",
        "source_created_on": created.isoformat(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "reporting_year": year,
        "reporting_week": week,
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "records": records,
    }
