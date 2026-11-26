"""照合済みの JIHS 週次定点 CSV から公開承認前の候補を生成する。"""

import argparse
import csv
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from apps.web.build import build
from packages.data_normalizer.jihs_weekly import normalize_local
from scripts.jihs_release_inputs import DEFAULT_INPUTS, load_reviewed_inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs="+", type=Path)
    parser.add_argument("--reviewed-inputs", type=Path, default=DEFAULT_INPUTS, help="照合済みの対象週と原本ハッシュ")
    parser.add_argument("--output", required=True, type=Path, help="Git 管理外の新規ディレクトリ")
    parser.add_argument("--generated-at", required=True, help="候補の生成日時（タイムゾーンを含む ISO 8601）")
    args = parser.parse_args()

    try:
        timestamp = datetime.fromisoformat(args.generated_at)
        reviewed = load_reviewed_inputs(args.reviewed_inputs)
        if len(args.csv_files) != len(reviewed):
            raise ValueError("入力ファイル数が照合済みの対象週数と一致しません")
        by_hash = {digest: week for week, digest in reviewed.items()}
        batches = {}
        for path in args.csv_files:
            raw = path.read_bytes()
            week = by_hash.get(sha256(raw).hexdigest())
            if week is None or week in batches:
                raise ValueError(f"照合済み原本と一致しないか同じ週が重複しています: {path.name}")
            batch = normalize_local(raw, retrieved_at=timestamp)
            version, = batch["versions"]
            if f'{version["reporting_year"]:04d}-W{version["reporting_week"]:02d}' != week:
                raise ValueError(f"原本の対象週が一致しません: {path.name}")
            batches[week] = batch

        build([batches[week] for week in sorted(batches)], args.output, base="/japan-infection-watch/",
              generated_at=timestamp.isoformat(), release_candidate=True)
    except (OSError, KeyError, ValueError, TypeError, csv.Error) as error:
        parser.exit(2, f"公開候補を生成できません：{error}\n")


if __name__ == "__main__":
    main()
