"""公開されないローカル配布一式の生成と参照整合性を検証する。"""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from apps.web.build import build
from fixtures.build_web_preview import TIMESTAMP, preview_batches


class SiteBuildTest(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.output = Path(scratch.name) / "site"
        self.batches = preview_batches()

    def test_generates_pages_and_separates_the_municipality_guide(self):
        build(self.batches, self.output, base="/japan-infection-watch/", generated_at=TIMESTAMP)
        self.assertEqual(len(list(self.output.glob("prefectures/*/index.html"))), 47)
        self.assertEqual(len(list(self.output.glob("diseases/*/index.html"))), 19)
        home = (self.output / "index.html").read_text()
        for path in ("prefectures/21/", "diseases/influenza/", "municipalities/21201/", "sources/"):
            self.assertIn(f'href="/japan-infection-watch/{path}"', home)
        municipality = (self.output / "municipalities/21201/index.html").read_text()
        self.assertIn("このページに岐阜市の集計はありません。", municipality)
        self.assertIn("https://www.city.gifu.lg.jp/kenko/kansensyou/1004450/1004453.html", municipality)
        self.assertNotIn("<table>", municipality)
        self.assertFalse((self.output / "municipalities/99999").exists())
        self.assertIn("全国のページへ戻る", (self.output / "404.html").read_text())

    def test_all_indexes_and_monthly_files_have_matching_sizes_and_hashes(self):
        build(self.batches[::-1], self.output, base="/", generated_at=TIMESTAMP)
        data = self.output / "data"
        manifest = json.loads((data / "manifest.json").read_bytes())
        self.assertTrue(manifest["fictional"])
        self.assertEqual(manifest["publication_status"], "blocked")
        source, = manifest["sources"].values()
        self.assertEqual(source["latest_period_end"], "2030-02-03")
        self.assertEqual(len(source["region_indexes"]), 48)
        paths = set()

        def read(reference):
            path = reference["path"]
            self.assertNotIn(path, paths)
            paths.add(path)
            payload = (data / path).read_bytes()
            self.assertEqual(len(payload), reference["bytes"])
            self.assertEqual(sha256(payload).hexdigest(), reference["sha256"])
            payload = json.loads(payload)
            self.assertEqual(payload["release_id"], manifest["release_id"])
            return payload

        for region, reference in source["region_indexes"].items():
            self.assertIn("/index/", reference["path"])
            index = read(reference)
            for code, disease in index["diseases"].items():
                self.assertIn(f"/{region}/{code}.json", disease["latest"]["path"])
                current = read(disease["latest"])["observations"]
                self.assertEqual({row["period_end"] for row in current}, {"2030-02-03"})
                self.assertEqual(set(disease["history"]), {"2030-01", "2030-02"})
                for month, item in disease["history"].items():
                    self.assertIn(f"/{region}/{month}/{code}.json", item["path"])
                    history = read(item)
                    self.assertEqual({row["period_end"][:7] for row in history["observations"]}, {month})
                    self.assertNotIn("source_token", history["observations"][0])
        self.assertEqual(len(paths), 48 + 48 * 19 * 3)

    def test_refuses_duplicate_weeks_incomplete_rows_real_input_and_existing_output(self):
        for invalid_batch in (
            dict(self.batches[0], fictional=False),
            dict(self.batches[0], public_candidates=[{}]),
            dict(self.batches[0], observations=self.batches[0]["observations"][:-1]),
        ):
            with self.subTest(invalid_batch=list(invalid_batch)):
                with self.assertRaises(ValueError):
                    build([invalid_batch], self.output, base="/", generated_at=TIMESTAMP)
                self.assertFalse(self.output.exists())
        with self.assertRaisesRegex(ValueError, "同じ報告週"):
            build([self.batches[0]] * 2, self.output, base="/", generated_at=TIMESTAMP)
        with self.assertRaisesRegex(ValueError, "基準パス"):
            build(self.batches, self.output, base="//external.example/", generated_at=TIMESTAMP)
        blocked = deepcopy(self.batches[0])
        blocked["versions"][0]["publication_status"] = "allowed"
        with self.assertRaisesRegex(ValueError, "公開対象外"):
            build([blocked], self.output, base="/", generated_at=TIMESTAMP)
        self.output.mkdir()
        marker = self.output / "keep"
        marker.write_text("既存の版")
        with self.assertRaisesRegex(ValueError, "出力先が存在"):
            build(self.batches, self.output, base="/", generated_at=TIMESTAMP)
        self.assertEqual(marker.read_text(), "既存の版")


if __name__ == "__main__":
    unittest.main()
