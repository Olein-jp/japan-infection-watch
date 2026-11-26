"""O-001 で照合した JIHS 第45・46週から公開承認前の候補を生成する。"""

import argparse
import csv
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from apps.web.build import build
from packages.data_normalizer.jihs_weekly import normalize_local


REVIEWED_INPUTS = {
    "3bcbdddab4f6267db777e3b44cbddc00be9e2782d5872f5260ad81fd00957410": (2026, 45),
    "ae5642911f0c702ba2ab4035fb3ca6e7516f4f9cd4799e78bed51908fac6e310": (2026, 46),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs=len(REVIEWED_INPUTS), type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Git 管理外の新規ディレクトリ")
    parser.add_argument("--generated-at", required=True, help="候補の生成日時（タイムゾーンを含む ISO 8601）")
    args = parser.parse_args()

    try:
        timestamp = datetime.fromisoformat(args.generated_at)
        batches = {}
        for path in args.csv_files:
            raw = path.read_bytes()
            week = REVIEWED_INPUTS.get(sha256(raw).hexdigest())
            if week is None or week in batches:
                raise ValueError(f"照合済み原本と一致しないか同じ週が重複しています: {path.name}")
            batch = normalize_local(raw, retrieved_at=timestamp)
            version, = batch["versions"]
            if (version["reporting_year"], version["reporting_week"]) != week:
                raise ValueError(f"原本の対象週が一致しません: {path.name}")
            batches[week] = batch

        build([batches[week] for week in sorted(batches)], args.output, base="/japan-infection-watch/",
              generated_at=timestamp.isoformat(), release_candidate=True)
    except (OSError, KeyError, ValueError, TypeError, csv.Error) as error:
        parser.exit(2, f"公開候補を生成できません：{error}\n")


if __name__ == "__main__":
    main()
