"""架空の2週分を正規化し、指定先に静的プレビューを生成する。"""

import argparse
from datetime import datetime
from pathlib import Path

from apps.web.build import build
from packages.data_normalizer.jihs_weekly import normalize_fixture
from fixtures.jihs_weekly import csv_bytes, fixture_table


TIMESTAMP = "2030-02-05T13:00:00+09:00"


def preview_batches(latest_count=24):
    february = fixture_table()
    february[1][:2] = ["2030年5週(1月28日〜2月3日)", "2030年2月4日作成"]
    february[4][1:3] = [str(latest_count), "2.40"]
    return [
        normalize_fixture(csv_bytes(fixture_table()), retrieved_at=datetime.fromisoformat("2030-01-16T09:00:00+09:00")),
        normalize_fixture(csv_bytes(february), retrieved_at=datetime.fromisoformat("2030-02-05T09:00:00+09:00")),
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--base", default="/japan-infection-watch/")
    parser.add_argument("--generated-at", default=TIMESTAMP)
    parser.add_argument("--latest-count", type=int, default=24, help="架空の全国インフルエンザ報告件数")
    args = parser.parse_args()
    build(preview_batches(args.latest_count), args.output, base=args.base, generated_at=args.generated_at)
