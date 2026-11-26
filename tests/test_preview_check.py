"""検証用成果物の容量・配布範囲・変更・旧版判定を再現する。"""

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from apps.web.build import build
from fixtures.build_web_preview import TIMESTAMP, preview_batches
from scripts.check_preview import evaluate


class PreviewCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scratch = TemporaryDirectory()
        cls.addClassCleanup(scratch.cleanup)
        cls.root = Path(scratch.name)
        cls.batches = preview_batches()
        cls.baseline = cls.root / "baseline"
        build(cls.batches, cls.baseline, base="/japan-infection-watch/", generated_at=TIMESTAMP)

    def setUp(self):
        scratch = TemporaryDirectory(dir=self.root)
        self.addCleanup(scratch.cleanup)
        self.candidate = Path(scratch.name) / "candidate"

    def test_first_preview_and_regeneration_without_content_change(self):
        initial = evaluate(self.baseline)
        refreshed = deepcopy(self.batches)
        refreshed[1]["versions"][0]["retrieved_at"] = "2030-02-05T11:00:00+09:00"
        build(refreshed, self.candidate, base="/japan-infection-watch/", generated_at="2030-02-05T14:00:00+09:00")
        result = evaluate(self.candidate, baseline=self.baseline)
        self.assertEqual(initial["change"], "no_baseline")
        self.assertEqual(result["change"], "unchanged")
        self.assertNotEqual(result["sha256"], initial["sha256"])
        self.assertEqual(result["content_sha256"], initial["content_sha256"])
        self.assertEqual(result["file_count"], 2857)
        self.assertFalse(result["publication_allowed"])

    def test_detects_asset_changes_and_observation_changes(self):
        shutil.copytree(self.baseline, self.candidate)
        asset = self.candidate / "assets/site.css"
        asset.write_bytes(asset.read_bytes() + b"\nmain { color: black; }\n")
        self.assertEqual(evaluate(self.candidate, baseline=self.baseline)["change"], "changed")
        observations = deepcopy(self.batches)
        observations[1]["observations"][0]["value"] = 25
        updated = self.candidate.parent / "updated"
        build(observations, updated, base="/japan-infection-watch/", generated_at=TIMESTAMP)
        result = evaluate(updated, baseline=self.baseline)
        self.assertEqual(result["change"], "changed")
        self.assertFalse(result["publication_allowed"])

    def test_refuses_corruption_even_with_the_same_size(self):
        shutil.copytree(self.baseline, self.candidate)
        target = next(self.candidate.glob("data/releases/*/latest/*/national/jp/influenza.json"))
        raw = target.read_bytes()
        changed = raw.replace(b'24', b'34', 1)
        self.assertEqual(len(changed), len(raw))
        self.assertNotEqual(changed, raw)
        target.write_bytes(changed)
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            evaluate(self.candidate)

    def test_refuses_extra_files_links_and_over_budget(self):
        shutil.copytree(self.baseline, self.candidate)
        for kind in ("extra", "symlink", "hardlink"):
            file = self.candidate / "unexpected"
            source = self.candidate / "assets/site.css"
            with self.subTest(kind=kind):
                if kind == "symlink":
                    file.symlink_to(source)
                elif kind == "hardlink":
                    os.link(source, file)
                else:
                    file.write_text("範囲外")
                with self.assertRaisesRegex(ValueError, "配布範囲|ハードリンク"):
                    evaluate(self.candidate)
                file.unlink()
        with self.assertRaisesRegex(ValueError, "容量超過"):
            evaluate(self.candidate, limit=3)

    def test_refuses_a_stale_revision_or_an_older_week(self):
        with self.assertRaisesRegex(ValueError, "Git リビジョン"):
            evaluate(self.baseline, candidate_revision="a" * 40, expected_revision="b" * 40)
        build(self.batches[:1], self.candidate, base="/japan-infection-watch/", generated_at=TIMESTAMP)
        with self.assertRaisesRegex(ValueError, "集計対象週が比較元より前"):
            evaluate(self.candidate, baseline=self.baseline)

    def test_only_accepts_the_expected_bundle_hash(self):
        expected = evaluate(self.baseline)["sha256"]
        self.assertEqual(evaluate(self.baseline, expected_sha256=expected)["sha256"], expected)
        with self.assertRaisesRegex(ValueError, "64桁"):
            evaluate(self.baseline, expected_sha256="")
        with self.assertRaisesRegex(ValueError, "照合済みの値"):
            evaluate(self.baseline, expected_sha256="0" * 64)

    def test_refuses_nonpreview_and_internal_fields(self):
        shutil.copytree(self.baseline, self.candidate)
        path = self.candidate / "data/manifest.json"
        original = json.loads(path.read_bytes())
        path.write_text(json.dumps(dict(original, fictional=False)))
        with self.assertRaisesRegex(ValueError, "架空プレビュー"):
            evaluate(self.candidate)
        path.write_text(json.dumps(dict(original, internal_notes="配布外")))
        with self.assertRaisesRegex(ValueError, "配布対象の項目"):
            evaluate(self.candidate)


if __name__ == "__main__":
    unittest.main()
