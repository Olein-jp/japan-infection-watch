"""架空データで R-15 の品質ルールを試す。"""

from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from packages.data_model.observations import (
    PERIOD_FIELDS, observation_key, series_key, validate_batch, validate_observation,
)


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
