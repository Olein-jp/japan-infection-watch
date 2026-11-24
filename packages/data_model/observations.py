"""観測行と原本版の検証。"""

from datetime import date
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
