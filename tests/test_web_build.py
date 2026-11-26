"""公開されないローカル配布一式の生成と参照整合性を検証する。"""

from copy import deepcopy
from datetime import date, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from apps.web.build import JIHS_PROVISIONAL, MHLW_SCHOOL_REPORTS, build
from apps.web.preview_data import REGIONS, history_start
from fixtures.build_web_preview import TIMESTAMP, preview_batches
from fixtures.jihs_weekly import csv_bytes, fixture_table
from packages.data_normalizer.jihs_weekly import normalize_fixture, normalize_local
from scripts.check_preview import verify_bundle


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
        self.assertIn(f'href="{MHLW_SCHOOL_REPORTS}"', home)
        for code in REGIONS.keys() - {"jp"}:
            with self.subTest(prefecture=code):
                region = (self.output / f"prefectures/{code}/index.html").read_text()
                school = region.split('id="school-closures"', 1)[1].split("</section>", 1)[0]
                self.assertIn(f'href="{MHLW_SCHOOL_REPORTS}"', school)
                self.assertIn("医療機関1か所あたり（件）", region)
                self.assertNotIn("定点当たり（件／定点）", region)
        municipality = (self.output / "municipalities/21201/index.html").read_text()
        self.assertIn("このページに岐阜市の集計はありません。", municipality)
        self.assertIn("https://www.city.gifu.lg.jp/kenko/kansensyou/1004450/1004453.html", municipality)
        self.assertNotIn("<table>", municipality)
        self.assertFalse((self.output / "municipalities/99999").exists())
        self.assertIn("全国のページへ戻る", (self.output / "404.html").read_text())
        fallback = Path(__file__).resolve().parents[1] / "apps/web/official_links/index.html"
        self.assertIn(f'href="{MHLW_SCHOOL_REPORTS}"', fallback.read_text())
        for path in [*self.output.rglob("*.html"), fallback]:
            with self.subTest(page=path):
                page = path.read_text()
                self.assertNotIn("gakkohoken.jp", page)
                self.assertNotIn("jssh.absence.information.mapping.service", page)

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

    def test_release_candidate_requires_provenance_and_stays_out_of_preview_modes(self):
        batch = normalize_local(csv_bytes(fixture_table()), retrieved_at=datetime.fromisoformat(TIMESTAMP))
        build([batch], self.output, base="/japan-infection-watch/", generated_at=TIMESTAMP,
              release_candidate=True)
        self.assertGreater(verify_bundle(self.output, release_candidate=True)["file_count"], 0)
        for options in ({}, {"local_jihs": True}):
            with self.assertRaisesRegex(ValueError, "配布版 ID"):
                verify_bundle(self.output, **options)

        home = self.output / "index.html"
        html = home.read_text()
        self.assertNotIn("自分用・ローカル閲覧", html)
        self.assertIn(JIHS_PROVISIONAL, html)
        home.write_text(html.replace(JIHS_PROVISIONAL, ""))
        with self.assertRaisesRegex(ValueError, "訂正される可能性の表示"):
            verify_bundle(self.output, release_candidate=True)

    def test_rolling_six_months_includes_boundary_and_omits_earlier_rows(self):
        self.assertEqual(history_start(date(2028, 8, 31)), date(2028, 2, 29))
        self.assertEqual(history_start(date(2029, 8, 31)), date(2029, 2, 28))
        self.assertEqual(history_start(date(2030, 2, 3)), date(2029, 8, 3))
        batches = []
        for end in (date(2030, 3, 31), date(2029, 9, 23), date(2029, 9, 30), date(2029, 8, 26)):
            start = end - timedelta(days=6)
            created = end + timedelta(days=1)
            year, week, _ = end.isocalendar()
            table = fixture_table()
            table[1][:2] = [f"{year}年{week}週({start.month}月{start.day}日〜{end.month}月{end.day}日)",
                            f"{created.year}年{created.month}月{created.day}日作成"]
            batches.append(normalize_fixture(csv_bytes(table), retrieved_at=datetime.fromisoformat(
                f"{created}T09:00:00+09:00")))

        build(batches, self.output, base="/", generated_at="2030-04-02T09:00:00+09:00")
        data = self.output / "data"
        manifest = json.loads((data / "manifest.json").read_text())
        source, = manifest["sources"].values()
        index = json.loads((data / source["region_indexes"]["jp"]["path"]).read_text())
        history = index["diseases"]["influenza"]["history"]
        self.assertEqual(set(history), {"2029-09", "2030-03"})
        september = json.loads((data / history["2029-09"]["path"]).read_text())
        self.assertEqual({row["period_end"] for row in september["observations"]}, {"2029-09-30"})
        self.assertEqual(set(september["versions"]), {batches[2]["versions"][0]["id"]})
        html = (self.output / "diseases/influenza/index.html").read_text()
        self.assertIn("<time>2029-09-24</time>〜<time>2030-03-31</time>", html)

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

    def test_local_csv_mode_stays_separate_from_preview_and_publication(self):
        batch = normalize_local(csv_bytes(fixture_table()), retrieved_at=datetime.fromisoformat(TIMESTAMP))
        school_report = {
            "reporting_year": 2030, "reporting_week": 2,
            "weekly_start": "2030-01-07", "weekly_end": "2030-01-13",
            "source_url": "https://www.mhlw.go.jp/content/123456.pdf", "regional_page": 4,
            "regional_rows": [
                {"area_level": "prefecture_reporting_area", "area_label": name, "weekly": {
                    "schools_with_class_closures": {"value": 2, "status": "numeric"},
                    "schools_with_grade_closures": {"value": 0, "status": "numeric"},
                    "school_closures": {"value": None, "status": "unknown_count"},
                }} for code, name in REGIONS.items() if code != "jp"
            ] + [{"area_level": "designated_city", "area_label": "横浜市"}],
        }
        with self.assertRaisesRegex(ValueError, "架空データだけ"):
            build([batch], self.output, base="/", generated_at=TIMESTAMP)
        with self.assertRaisesRegex(ValueError, "ローカル閲覧用"):
            build(self.batches, self.output, base="/", generated_at=TIMESTAMP, local_only=True)
        with self.assertRaisesRegex(ValueError, "ローカル閲覧専用"):
            build(self.batches, self.output, base="/", generated_at=TIMESTAMP, closure_reports=[school_report])

        build([batch], self.output, base="/", generated_at=TIMESTAMP, local_only=True,
              closure_reports=[school_report])
        manifest = json.loads((self.output / "data/manifest.json").read_text())
        self.assertFalse(manifest["fictional"])
        self.assertEqual(manifest["publication_status"], "blocked")
        self.assertTrue(manifest["release_id"].startswith("local-"))
        with self.assertRaises(ValueError):
            verify_bundle(self.output)
        verification = verify_bundle(self.output, local_jihs=True)
        self.assertEqual(verification["latest_period_end"], "2030-01-13")
        html = (self.output / "index.html").read_text()
        self.assertIn("自分用・ローカル閲覧", html)
        self.assertIn("<dt>出典</dt>", html)
        self.assertIn("<dt>編集・加工</dt>", html)
        self.assertIn("https://id-info.jihs.go.jp/surveillance/idwr/provisional/2030/02/index.html", html)
        regional = (self.output / "prefectures/14/index.html").read_text()
        self.assertIn("https://www.mhlw.go.jp/content/123456.pdf#page=4", regional)
        self.assertIn('style="width:100.00%"></span></span>2施設', regional)
        self.assertIn('style="width:0.00%"></span></span>0施設', regional)
        self.assertIn('aria-hidden="true"></span>計数不明', regional)
        (self.output / "index.html").write_text(html.replace("<dt>編集・加工</dt>", "<dt>説明</dt>"))
        with self.assertRaisesRegex(ValueError, "出典または編集・加工"):
            verify_bundle(self.output, local_jihs=True)


if __name__ == "__main__":
    unittest.main()
