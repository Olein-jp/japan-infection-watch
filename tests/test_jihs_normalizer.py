"""F-001 の入力検査と共通観測への変換を架空の CSV で確認する。"""

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from fixtures.jihs_weekly import csv_bytes, fixture_table
from packages.data_model.observations import validate_batch
from packages.data_normalizer.jihs_weekly import DISEASE_IDS, normalize_fixture


REPO = Path(__file__).resolve().parents[1]
RETRIEVED_AT = datetime.fromisoformat("2030-01-16T09:00:00+09:00")
POC_URL = "https://id-info.jihs.go.jp/surveillance/idwr/provisional/2030/02/2030-02-teiten.csv"


class JihsNormalizerTest(unittest.TestCase):
    def normalize(self, table):
        return normalize_fixture(csv_bytes(table), retrieved_at=RETRIEVED_AT)

    def test_valid_weekly_batch_preserves_source_and_common_keys(self):
        raw = csv_bytes(fixture_table())
        batch = normalize_fixture(raw, retrieved_at=RETRIEVED_AT)
        rows = batch["observations"]
        version, = batch["versions"]
        validate_batch(rows, [version])
        self.assertEqual(len(rows), 1824)
        self.assertEqual({row["region_kind"] for row in rows}, {"national", "prefecture"})
        self.assertEqual({row["region_id"] for row in rows}, {"jp", *(f"{code:02}" for code in range(1, 48))})
        self.assertEqual({row["disease_id"] for row in rows}, set(DISEASE_IDS.values()))
        self.assertEqual({row["version_id"] for row in rows}, {version["id"]})
        self.assertEqual({(row["period_start"], row["period_end"]) for row in rows}, {
            ("2030-01-07", "2030-01-13"),
        })
        self.assertEqual((version["reporting_year"], version["reporting_week"]), (2030, 2))
        self.assertEqual(version["source_sha256"], sha256(raw).hexdigest())
        self.assertEqual(version["source_created_on"], "2030-01-15")
        self.assertEqual(version["retrieved_at"], RETRIEVED_AT.isoformat())
        self.assertIsNone(version["supersedes"])

    def test_distinguishes_values_and_does_not_infer_denominator(self):
        rows = [row for row in self.normalize(fixture_table())["observations"]
                if row["disease_id"] == "influenza"]
        selected = {
            (row["region_id"], row["metric_id"]): (
                row["unit"], row["value_status"], row["value"], row["source_token"],
                row["denominator_status"],
            )
            for row in rows
        }
        count = "sentinel_report_count"
        rate = "sentinel_reports_per_site"
        self.assertEqual(selected["jp", count], ("case", "reported", 0, "000", "not_applicable"))
        self.assertEqual(selected["jp", rate], ("case_per_sentinel", "reported", "0.00", "0.00", "not_provided"))
        self.assertEqual(selected["01", count], ("case", "dash", None, "-", "not_applicable"))
        self.assertEqual(selected["01", rate], ("case_per_sentinel", "blank", None, "", "not_provided"))
        self.assertEqual(selected["02", count], ("case", "blank", None, "", "not_applicable"))
        self.assertEqual(selected["02", rate], ("case_per_sentinel", "dash", None, "-", "not_provided"))
        self.assertEqual(selected["03", rate], ("case_per_sentinel", "reported", "1.70", "1.70", "not_provided"))
        self.assertTrue(all(row["denominator"] is None for row in rows))

    def test_rejects_duplicate_regions_duplicate_titles_and_column_changes(self):
        for row, column, value, error in (
            (5, 0, "総数", "全国と47都道府県"),
            (2, 3, "インフルエンザ", "疾患見出し"),
            (2, 1, "未確認の疾患", "疾患見出し"),
            (3, 2, "別の指標", "指標の見出し"),
            (4, 0, "未確認の地域", "全国と47都道府県"),
        ):
            with self.subTest(row=row, column=column):
                table = fixture_table()
                table[row][column] = value
                with self.assertRaisesRegex(ValueError, error):
                    self.normalize(table)
        table = fixture_table()
        table[4].pop()
        with self.assertRaisesRegex(ValueError, "列数"):
            self.normalize(table)

    def test_rejects_inconsistent_week_and_unsupported_cell_value(self):
        table = fixture_table()
        table[1][0] = "2030年2週(1月6日〜1月12日)"
        with self.assertRaisesRegex(ValueError, "番号と期間"):
            self.normalize(table)
        table = fixture_table()
        table[4][2] = "0.0"
        with self.assertRaisesRegex(ValueError, "未対応の値"):
            self.normalize(table)

    def test_retrieval_time_does_not_create_another_source_version(self):
        table = fixture_table()
        raw = csv_bytes(table)
        original = self.normalize(table)["versions"][0]
        refetch = normalize_fixture(raw, retrieved_at=RETRIEVED_AT.replace(hour=10))["versions"][0]
        self.assertEqual(original["id"], refetch["id"])
        table[4][1] = "123"
        changed = self.normalize(table)["versions"][0]
        self.assertEqual(original["publication_key"], changed["publication_key"])
        self.assertNotEqual(original["id"], changed["id"])
        self.assertIsNone(changed["supersedes"])

    def test_cli_requires_fixture_mode_and_never_emits_public_candidates(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "weekly.csv"
            path.write_bytes(csv_bytes(fixture_table()))
            command = [
                sys.executable, "-B", "-m", "packages.data_normalizer.jihs_weekly", str(path),
                "--retrieved-at", RETRIEVED_AT.isoformat(),
            ]
            denied = subprocess.run(command, cwd=REPO, capture_output=True, check=False)
            self.assertEqual(denied.returncode, 2)
            self.assertEqual(denied.stdout, b"")
            allowed = subprocess.run([*command, "--fixture"], cwd=REPO, capture_output=True, check=True)
            result = json.loads(allowed.stdout)
            self.assertTrue(result["fictional"])
            self.assertEqual(result["public_candidates"], [])
            self.assertEqual(result["versions"][0]["publication_status"], "blocked")
            command[-1] = "2030-01-16T09:00:00"
            bad_time = subprocess.run([*command, "--fixture"], cwd=REPO, capture_output=True, check=False)
            self.assertEqual(bad_time.returncode, 2)
            self.assertEqual(bad_time.stdout, b"")
            path.write_bytes(b"invalid")
            malformed = subprocess.run(
                [*command[:-1], RETRIEVED_AT.isoformat(), "--fixture"],
                cwd=REPO, capture_output=True, check=False,
            )
            self.assertEqual(malformed.returncode, 2)
            self.assertEqual(malformed.stdout, b"")

    def test_legacy_poc_output_shape_is_preserved(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "weekly.csv"
            path.write_bytes(csv_bytes(fixture_table()))
            proc = subprocess.run([
                sys.executable, "-B", str(REPO / "poc/jihs/normalize.py"), str(path),
                "--source-url", POC_URL, "--retrieved-at", RETRIEVED_AT.isoformat(),
            ], cwd=folder, capture_output=True, check=True)
        result = json.loads(proc.stdout)
        self.assertEqual(len(result["records"]), 912)
        self.assertEqual(result["source_url"], POC_URL)
        self.assertEqual(result["records"][0]["report_count"], {"value": 0, "status": "numeric"})
        self.assertEqual(result["records"][0]["reports_per_sentinel"], {"value": "0.00", "status": "numeric"})


if __name__ == "__main__":
    unittest.main()
