"""架空の週次速報で Pages 配布前の照合を試験する。"""

from datetime import datetime
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory
import unittest

from apps.web.build import build
from fixtures.jihs_weekly import csv_bytes, fixture_table
from packages.data_normalizer.jihs_weekly import normalize_local
from scripts.check_preview import verify_bundle
from scripts.prepare_jihs_pages import prepare


class PrepareJihsPagesTest(unittest.TestCase):
    def test_writes_only_the_approved_weeks_and_hashes(self):
        timestamp = "2026-11-26T11:02:41+09:00"
        batches = []
        for week, start, end, creation in ((45, 2, 8, 11), (46, 9, 15, 18)):
            table = fixture_table()
            table[1][:2] = [f"2026年{week}週(11月{start}日〜11月{end}日)", f"2026年11月{creation}日作成"]
            batches.append(normalize_local(csv_bytes(table), retrieved_at=datetime.fromisoformat(timestamp)))

        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "candidate"
            archive_path = root / "candidate.tar"
            output = root / "pages"
            build(batches, site, base="/japan-infection-watch/", generated_at=timestamp, release_candidate=True)
            candidate_hash = verify_bundle(site, release_candidate=True)["sha256"]
            with tarfile.open(archive_path, "w") as archive:
                archive.add(site, arcname=".")

            report = prepare(archive_path, output, candidate_sha256=candidate_hash)
            self.assertFalse(output.exists())
            with self.assertRaisesRegex(ValueError, "候補一式の SHA-256"):
                prepare(archive_path, output, candidate_sha256="0" * 64)
            with self.assertRaisesRegex(ValueError, "Pages 配布用一式の SHA-256"):
                prepare(archive_path, output, candidate_sha256=candidate_hash, pages_sha256=candidate_hash)
            self.assertFalse(output.exists())
            prepare(archive_path, output, candidate_sha256=candidate_hash, pages_sha256=report["sha256"])
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
                prepare(archive_path, root / "rejected", candidate_sha256=candidate_hash)
            self.assertFalse((root / "rejected").exists())
