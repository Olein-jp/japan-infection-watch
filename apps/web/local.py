"""手元にある JIHS 週次定点速報 CSV を、この Mac だけで閲覧する。"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from apps.web.build import build
from packages.data_normalizer.jihs_weekly import normalize_local
from poc.pages.serve import serve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs="+", type=Path, help="JIHS の公式速報 CSV（各週1ファイル）")
    parser.add_argument("--school-report", action="append", type=Path, default=[],
                        help="厚労省の学校休業 PDF から抽出した JSON（複数指定可）")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--port", default=8765, type=int)
    destination.add_argument("--output", type=Path, help="検証用に書き出す新規ディレクトリ（配布不可）")
    args = parser.parse_args()
    if args.output and args.school_report:
        parser.error("--output の出力対象は JIHS 週次定点速報のみです")
    try:
        timestamp = datetime.now().astimezone()
        batches = [normalize_local(path.read_bytes(), retrieved_at=timestamp) for path in args.csv_files]
        reports = [json.loads(path.read_text(encoding="utf-8")) for path in args.school_report]
        if args.output:
            build(batches, args.output, base="/japan-infection-watch/", generated_at=timestamp.isoformat(),
                  local_only=True)
            return
        with TemporaryDirectory(prefix="jiw-local-") as directory:
            site = Path(directory) / "site"
            build(batches, site, base="/", generated_at=timestamp.isoformat(), local_only=True,
                  closure_reports=reports)
            serve(site, base="/", port=args.port)
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, TypeError, KeyError, csv.Error) as error:
        parser.exit(2, f"ローカル閲覧を開始できません：{error}\n")


if __name__ == "__main__":
    main()
