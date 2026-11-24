"""R-15 の品質ルールを架空データで検証する。"""

from datetime import date, timedelta
import json
from pathlib import Path
import unittest

from verify_rules import (
    check_required_cells, compare_revision, compare_transcriptions, flag_weekly_jump,
    observation_key, reconcile_total, validate_batch, validate_observation,
)


class DraftRulesTest(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).resolve().parents[2] / "tests/fixtures/r15-observations.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertTrue(data["fictional"])
        self.rows = data["observations"]
        self.versions = data["versions"]
        (self.zero, self.corrected, self.rounded_zero, self.corrected_rate, self.dash,
         self.prefecture, self.city, self.total, self.cumulative) = self.rows

    def test_valid_batch_preserves_zero_dash_and_distinct_periods(self):
        validate_batch(self.rows, self.versions)
        self.assertEqual(self.zero["value"], 0)
        self.assertEqual(self.rounded_zero["value"], "0.00")
        self.assertIsNone(self.rounded_zero["denominator"])
        self.assertIsNone(self.dash["value"])
        self.assertNotEqual(observation_key(self.total), observation_key(self.cumulative))

    def test_missing_states_cannot_carry_numbers(self):
        for status in ("blank", "dash", "unknown_count", "not_reported", "suppressed", "not_applicable"):
            with self.subTest(status=status):
                validate_observation(dict(self.zero, value_status=status, value=None))
                with self.assertRaisesRegex(ValueError, "欠損値と状態の不一致"):
                    validate_observation(dict(self.zero, value_status=status))

    def test_explicit_zero_cannot_be_null(self):
        with self.assertRaisesRegex(ValueError, "件数の形式"):
            validate_observation(dict(self.zero, value=None))

    def test_unknown_denominator_cannot_be_inferred(self):
        with self.assertRaisesRegex(ValueError, "分母と状態の不一致"):
            validate_observation(dict(self.rounded_zero, denominator=4))

    def test_decimal_precision_and_unit(self):
        with self.assertRaisesRegex(ValueError, "表示精度"):
            validate_observation(dict(self.rounded_zero, value="0.0"))
        with self.assertRaisesRegex(ValueError, "指標と単位"):
            validate_observation(dict(self.zero, unit="facility"))

    def test_duplicate_in_same_version_fails(self):
        with self.assertRaisesRegex(ValueError, "同一版の観測の重複"):
            validate_batch([*self.rows, dict(self.zero, value=5)], self.versions)

    def test_correction_is_compared_without_overwriting_previous_version(self):
        validate_batch(self.rows, self.versions)
        self.assertEqual(compare_revision(self.zero, self.corrected, self.versions), 2)
        self.assertEqual(str(compare_revision(self.rounded_zero, self.corrected_rate, self.versions)), "0.50")
        self.assertEqual(self.zero["value"], 0)
        with self.assertRaisesRegex(ValueError, "訂正の比較条件"):
            compare_revision(self.dash, self.corrected, self.versions)

    def test_correction_cannot_cross_sources_or_publications(self):
        for field, value in (("supersedes", "closures-a"), ("publication_key", "2030-W03-provisional")):
            with self.subTest(field=field):
                versions = [self.versions[0], dict(self.versions[1], **{field: value}), self.versions[2]]
                with self.assertRaisesRegex(ValueError, "訂正元"):
                    validate_batch(self.rows, versions)

    def test_version_cycle_fails(self):
        versions = [dict(self.versions[0], supersedes="sentinel-b"), *self.versions[1:]]
        with self.assertRaisesRegex(ValueError, "版の循環"):
            validate_batch(self.rows, versions)

    def test_original_transcription_must_match_even_if_numeric_values_are_equivalent(self):
        compare_transcriptions(self.rounded_zero, self.rounded_zero.copy())
        with self.assertRaisesRegex(ValueError, "原表照合不一致"):
            compare_transcriptions(self.rounded_zero, dict(self.rounded_zero, source_token="0"))

    def test_missing_required_cell_is_abnormal_but_unrequired_dash_is_allowed(self):
        keys = [(observation_key(self.zero), self.zero["version_id"])]
        check_required_cells(self.rows, keys)
        for rows in (self.rows[1:], [dict(self.zero, value_status="blank", value=None)]):
            with self.assertRaisesRegex(ValueError, "異常欠損"):
                check_required_cells(rows, keys)

    def test_renamed_column_and_inverted_date(self):
        changed = self.zero.copy()
        changed["amount"] = changed.pop("value")
        with self.assertRaisesRegex(ValueError, "列変更"):
            validate_observation(changed)
        with self.assertRaisesRegex(ValueError, "日付逆転"):
            validate_observation(dict(self.zero, period_end="2030-01-06"))

    def test_reconciliation_requires_expected_regions_and_version(self):
        parts = [self.prefecture, self.city]
        ids = [row["region_id"] for row in parts]
        self.assertEqual(reconcile_total(self.total, parts, ids), "matched")
        with self.assertRaisesRegex(ValueError, "内訳地域"):
            reconcile_total(self.total, parts[:1], ids)
        with self.assertRaisesRegex(ValueError, "比較条件"):
            reconcile_total(self.total, [parts[0], dict(parts[1], version_id="old")], ids)
        with self.assertRaisesRegex(ValueError, "比較条件"):
            reconcile_total(self.cumulative, parts, ids)

    def test_total_difference_is_error_and_unknown_is_incomplete(self):
        parts = [self.prefecture, self.city]
        ids = [row["region_id"] for row in parts]
        with self.assertRaisesRegex(ValueError, "集計不一致"):
            reconcile_total(dict(self.total, value=7), parts, ids)
        unknown = dict(self.city, value_status="unknown_count", value=None)
        self.assertEqual(reconcile_total(self.total, [self.prefecture, unknown], ids), "incomplete")
        self.assertIsNone(unknown["value"])

    def test_jump_is_review_and_missing_is_not_zero(self):
        next_week = {
            field: (date.fromisoformat(self.corrected[field]) + timedelta(days=7)).isoformat()
            for field in ("period_start", "period_end")
        }
        self.assertEqual(flag_weekly_jump(self.corrected, dict(self.corrected, value=15, **next_week)), "review")
        self.assertEqual(flag_weekly_jump(self.corrected, dict(self.corrected, value=4, **next_week)), "ok")
        missing = dict(self.corrected, value=None, value_status="not_reported", **next_week)
        self.assertEqual(flag_weekly_jump(self.corrected, missing), "incomplete")
        with self.assertRaisesRegex(ValueError, "比較条件"):
            flag_weekly_jump(self.corrected, dict(missing, coverage_id="different"))


if __name__ == "__main__":
    unittest.main()
