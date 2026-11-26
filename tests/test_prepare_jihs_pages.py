"""架空の週次速報で Pages 配布前の照合を試験する。"""

from datetime import date, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory
import unittest

from apps.web.build import build
from fixtures.jihs_weekly import csv_bytes, fixture_table
from packages.data_normalizer.jihs_weekly import normalize_local
from scripts.check_preview import verify_bundle
from scripts.jihs_release_inputs import load_reviewed_inputs
from scripts.prepare_jihs_pages import prepare


class PrepareJihsPagesTest(unittest.TestCase):
    def test_writes_only_the_approved_weeks_and_hashes(self):
        timestamp = "2026-11-26T11:02:41+09:00"
        batches = []
        reviewed = {}
        for week, start, end, creation in ((45, 2, 8, 11), (46, 9, 15, 18)):
            table = fixture_table()
            table[1][:2] = [f"2026年{week}週(11月{start}日〜11月{end}日)", f"2026年11月{creation}日作成"]
            raw = csv_bytes(table)
            reviewed[f"2026-W{week}"] = sha256(raw).hexdigest()
            batches.append(normalize_local(raw, retrieved_at=datetime.fromisoformat(timestamp)))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "reviewed.json"
            config.write_text(json.dumps(reviewed))
            site = root / "candidate"
            archive_path = root / "candidate.tar"
            output = root / "pages"
            build(batches, site, base="/japan-infection-watch/", generated_at=timestamp, release_candidate=True)
            candidate_hash = verify_bundle(site, release_candidate=True)["sha256"]
            with tarfile.open(archive_path, "w") as archive:
                archive.add(site, arcname=".")

            report = prepare(archive_path, output, candidate_sha256=candidate_hash, reviewed_inputs=config)
            self.assertFalse(output.exists())
            with self.assertRaisesRegex(ValueError, "候補一式の SHA-256"):
                prepare(archive_path, output, candidate_sha256="0" * 64, reviewed_inputs=config)
            with self.assertRaisesRegex(ValueError, "Pages 配布用一式の SHA-256"):
                prepare(archive_path, output, candidate_sha256=candidate_hash,
                        pages_sha256=candidate_hash, reviewed_inputs=config)
            self.assertFalse(output.exists())
            prepare(archive_path, output, candidate_sha256=candidate_hash,
                    pages_sha256=report["sha256"], reviewed_inputs=config)
            self.assertEqual(verify_bundle(output, published_jihs=True), report)
            manifest = json.loads((output / "data/manifest.json").read_bytes())
            self.assertEqual(manifest["publication_status"], "published")
            self.assertNotEqual(report["sha256"], candidate_hash)

            single_week = root / "one-week"
            build(batches[1:], single_week, base="/japan-infection-watch/", generated_at=timestamp,
                  release_candidate=True)
            with tarfile.open(archive_path, "w") as archive:
                archive.add(single_week, arcname=".")
            with self.assertRaisesRegex(ValueError, "履歴の対象週"):
                prepare(archive_path, root / "rejected", candidate_sha256=candidate_hash, reviewed_inputs=config)
            self.assertFalse((root / "rejected").exists())

    def test_preserves_a_reviewed_half_year_through_the_build_and_publish_pipeline(self):
        timestamp = "2026-11-26T11:02:41+09:00"
        with TemporaryDirectory() as directory:
            root = Path(directory)
            files = []
            reviewed = {}
            for week in range(20, 47):
                end = date.fromisocalendar(2026, week, 7)
                start = end - timedelta(days=6)
                created = end + timedelta(days=3)
                table = fixture_table()
                table[1][:2] = [
                    f"2026年{week}週({start.month}月{start.day}日〜{end.month}月{end.day}日)",
                    f"2026年{created.month}月{created.day}日作成",
                ]
                raw = csv_bytes(table)
                path = root / f"2026-{week}-teiten.csv"
                path.write_bytes(raw)
                files.append(path)
                reviewed[f"2026-W{week}"] = sha256(raw).hexdigest()

            config = root / "reviewed.json"
            config.write_text(json.dumps(reviewed))
            site = root / "candidate"
            command = [sys.executable, "-B", "-m", "scripts.build_release_candidate",
                       "--generated-at", timestamp, "--output", str(site), "--reviewed-inputs", str(config)]
            failed = subprocess.run(command + [str(path) for path in files[:-1]], capture_output=True, text=True)
            self.assertEqual(failed.returncode, 2)
            self.assertIn("対象週数", failed.stderr)
            self.assertFalse(site.exists())
            subprocess.run(command + [str(path) for path in reversed(files)], check=True)
            candidate_hash = verify_bundle(site, release_candidate=True)["sha256"]
            archive_path = root / "candidate.tar"
            with tarfile.open(archive_path, "w") as archive:
                archive.add(site, arcname=".")
            output = root / "pages"
            report = prepare(archive_path, output, candidate_sha256=candidate_hash, reviewed_inputs=config)
            prepare(archive_path, output, candidate_sha256=candidate_hash,
                    pages_sha256=report["sha256"], reviewed_inputs=config)
            self.assertEqual(report["file_count"], 7417)
            covered = (output / "prefectures/21/index.html").read_text()
            self.assertIn("<time>2026-05-11</time>〜<time>2026-11-15</time>", covered)

            config.write_text(json.dumps({"2026-W19": "0" * 64, **reviewed}))
            with self.assertRaisesRegex(ValueError, "直近6か月"):
                load_reviewed_inputs(config)
