"""ハッシュを照合した第45・46週の候補から Pages 配布用一式を作る。"""

import argparse
from datetime import date
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

from apps.web.preview_data import json_bytes
from scripts.build_release_candidate import REVIEWED_INPUTS
from scripts.check_preview import MAX_BYTES, SHA256, verify_bundle


PERIOD_ENDS = {date.fromisocalendar(year, week, 7).isoformat() for year, week in REVIEWED_INPUTS.values()}


def extract_candidate(archive_path, destination):
    total = 0
    with tarfile.open(archive_path, "r:") as archive:
        for member in archive:
            if not (member.isfile() or member.isdir()):
                raise ValueError("候補アーカイブには通常ファイルとディレクトリだけを含めてください")
            total += member.size
            if total > MAX_BYTES:
                raise ValueError("候補アーカイブの展開サイズが上限を超えました")
            archive.extract(member, destination, filter="data")


def prepare(archive, output, *, candidate_sha256, pages_sha256=None):
    if output.exists() or output.is_symlink():
        raise ValueError("指定先が存在します。新規ディレクトリを指定してください")
    if not SHA256.fullmatch(candidate_sha256) or (pages_sha256 is not None and not SHA256.fullmatch(pages_sha256)):
        raise ValueError("照合する SHA-256 を64桁の小文字の16進数で指定してください")
    with TemporaryDirectory(dir=output.parent) as work:
        site = Path(work) / "site"
        site.mkdir()
        extract_candidate(archive, site)
        candidate = verify_bundle(site, release_candidate=True, expected_period_ends=PERIOD_ENDS)
        if candidate["sha256"] != candidate_sha256:
            raise ValueError("候補一式の SHA-256 が承認対象と一致しません")

        path = site / "data/manifest.json"
        manifest = json.loads(path.read_bytes())
        manifest["publication_status"] = "published"
        path.write_bytes(json_bytes(manifest))
        pages = verify_bundle(site, published_jihs=True, expected_period_ends=PERIOD_ENDS)
        if pages_sha256 is not None:
            if pages["sha256"] != pages_sha256:
                raise ValueError("Pages 配布用一式の SHA-256 が承認対象と一致しません")
            site.rename(output)
        return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="候補 artifact の artifact.tar")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--pages-sha256", help="一致した配布版だけを書き出す。省略時はハッシュの算出のみ")
    args = parser.parse_args()
    try:
        report = prepare(args.archive, args.output, candidate_sha256=args.candidate_sha256,
                         pages_sha256=args.pages_sha256)
    except (OSError, tarfile.TarError, ValueError, KeyError, AttributeError, TypeError) as error:
        parser.exit(2, f"Pages 配布用一式を準備できません：{error}\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
