"""架空データで R-15 の品質ルールを試す。"""

from datetime import date
from decimal import Decimal
import re


SERIES_FIELDS = (
    "dataset_id", "region_id", "region_kind", "disease_id", "coverage_id",
    "facility_group", "metric_id", "unit", "period_kind",
)
PERIOD_FIELDS = ("period_start", "period_end")
ROW_FIELDS = set(SERIES_FIELDS + PERIOD_FIELDS + (
    "version_id", "value", "value_status", "source_token", "denominator_status", "denominator",
))
UNITS = {
    "sentinel_report_count": "case",
    "sentinel_reports_per_site": "case_per_sentinel",
    "class_closure_facility_count": "facility",
}
MISSING_STATUSES = {
    "blank", "dash", "unknown_count", "not_reported", "suppressed", "not_applicable",
}


def series_key(row):
    return tuple(row[field] for field in SERIES_FIELDS)


def observation_key(row):
    return series_key(row) + tuple(row[field] for field in PERIOD_FIELDS)


def validate_observation(row):
    if row.keys() != ROW_FIELDS:
        raise ValueError("列変更")
    if any(not isinstance(row[field], str) or not row[field] for field in SERIES_FIELDS + ("version_id",)):
        raise ValueError("キーの欠落")
    if UNITS.get(row["metric_id"]) != row["unit"]:
        raise ValueError("指標と単位の不一致")

    dates = [row[field] for field in PERIOD_FIELDS]
    if any(not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value)
           for value in dates):
        raise ValueError("日付形式")
    start, end = map(date.fromisoformat, dates)
    if end < start:
        raise ValueError("日付逆転")
    if row["period_kind"] not in {"weekly", "season_to_date"}:
        raise ValueError("期間区分")
    if row["period_kind"] == "weekly" and (start.weekday() != 0 or (end - start).days != 6):
        raise ValueError("週次期間")

    value, status = row["value"], row["value_status"]
    rate = row["unit"] == "case_per_sentinel"
    if status == "reported":
        if rate:
            if not isinstance(value, str) or not re.fullmatch(r"[0-9]+\.[0-9]{2}", value):
                raise ValueError("定点当たりの表示精度")
        elif type(value) is not int or value < 0:
            raise ValueError("件数の形式")
    elif status not in MISSING_STATUSES or value is not None:
        raise ValueError("欠損値と状態の不一致")

    denominator, denominator_status = row["denominator"], row["denominator_status"]
    if rate and denominator_status == "known":
        if type(denominator) is not int or denominator <= 0:
            raise ValueError("定点数の形式")
    elif denominator is not None or denominator_status != ("not_provided" if rate else "not_applicable"):
        raise ValueError("分母と状態の不一致")


def validate_batch(rows, versions):
    version_by_id = {version["id"]: version for version in versions}
    if len(version_by_id) != len(versions):
        raise ValueError("版 ID の重複")
    for version in versions:
        previous_id = version["supersedes"]
        if previous_id is None:
            continue
        previous = version_by_id.get(previous_id)
        if (previous is None or previous["dataset_id"] != version["dataset_id"]
                or previous["publication_key"] != version["publication_key"]
                or previous["source_sha256"] == version["source_sha256"]):
            raise ValueError("訂正元の不一致")
        visited = {version["id"]}
        while previous_id in version_by_id:
            if previous_id in visited:
                raise ValueError("版の循環")
            visited.add(previous_id)
            previous_id = version_by_id[previous_id]["supersedes"]

    seen = set()
    for row in rows:
        validate_observation(row)
        version = version_by_id.get(row["version_id"])
        if version is None or version["dataset_id"] != row["dataset_id"]:
            raise ValueError("観測と版の不一致")
        key = (observation_key(row), row["version_id"])
        if key in seen:
            raise ValueError("同一版の観測の重複")
        seen.add(key)


def compare_revision(previous, current, versions):
    version_by_id = {version["id"]: version for version in versions}
    if (observation_key(previous) != observation_key(current)
            or version_by_id[current["version_id"]]["supersedes"] != previous["version_id"]):
        raise ValueError("訂正の比較条件が不一致")
    if previous["value_status"] == current["value_status"] == "reported":
        return Decimal(current["value"]) - Decimal(previous["value"])
    return None


def check_required_cells(rows, required_keys):
    reported_keys = {
        (observation_key(row), row["version_id"])
        for row in rows if row["value_status"] == "reported"
    }
    if not set(required_keys).issubset(reported_keys):
        raise ValueError("必須セルの欠落または異常欠損")


def reconcile_total(total, parts, expected_region_ids):
    # expected_region_ids は出典ごとに確認済みの排他的な内訳。
    expected = set(expected_region_ids)
    if not expected or total["unit"] == "case_per_sentinel":
        raise ValueError("検算対象外")
    if ({row["region_id"] for row in parts} != expected
            or len(parts) != len(expected) or total["region_id"] in expected):
        raise ValueError("内訳地域が不一致")
    same_fields = (
        "dataset_id", "version_id", "disease_id", "coverage_id",
        "facility_group", "metric_id", "unit", "period_kind",
    ) + PERIOD_FIELDS
    if any(tuple(row[field] for field in same_fields) != tuple(total[field] for field in same_fields)
           for row in parts):
        raise ValueError("内訳の比較条件が不一致")
    if any(row["value_status"] != "reported" for row in [total, *parts]):
        return "incomplete"
    if sum(row["value"] for row in parts) != total["value"]:
        raise ValueError("掲載計と内訳の集計不一致")
    return "matched"


def flag_weekly_jump(previous, current):
    if (series_key(previous) != series_key(current) or current["period_kind"] != "weekly"
            or (date.fromisoformat(current["period_start"])
                - date.fromisoformat(previous["period_start"])).days != 7):
        raise ValueError("急変検知の比較条件が不一致")
    if any(row["value_status"] != "reported" for row in (previous, current)):
        return "incomplete"
    # 例示の閾値。系列ごとの実運用閾値は別途検証する。
    before, after = Decimal(previous["value"]), Decimal(current["value"])
    return "review" if abs(after - before) >= 10 and max(before, after) >= 3 * min(before, after) else "ok"


def compare_transcriptions(expected, actual):
    if (observation_key(expected) != observation_key(actual)
            or expected["version_id"] != actual["version_id"]):
        raise ValueError("原表照合の比較条件が不一致")
    fields = ("source_token", "value", "value_status", "denominator", "denominator_status")
    if any(expected[field] != actual[field] for field in fields):
        raise ValueError("原表照合不一致")
