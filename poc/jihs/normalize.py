"""JIHS の週次定点速報 CSV をローカルで正規化する。"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from packages.data_normalizer.jihs_csv import parse_weekly_csv


def normalize(raw, source_url, retrieved_at):
    result = parse_weekly_csv(raw)
    year, week = result["reporting_year"], result["reporting_week"]
    expected_url = (
        "https://id-info.jihs.go.jp/surveillance/idwr/provisional/"
        f"{year}/{week:02d}/{year}-{week:02d}-teiten.csv"
    )
    if source_url != expected_url:
        raise ValueError("配布 URL と CSV 内の対象週が一致しません")
    for record in result["records"]:
        del record["report_count"]["source_token"]
        del record["reports_per_sentinel"]["source_token"]
    return {
        "source_url": source_url,
        "source_stage": result.pop("source_stage"),
        "source_created_on": result.pop("source_created_on"),
        "retrieved_at": retrieved_at.isoformat(),
        **result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="ダウンロードした公式 CSV")
    parser.add_argument("--source-url", required=True, help="ダウンロード元の公式 CSV URL")
    parser.add_argument("--retrieved-at", required=True, help="取得日時（タイムゾーン付き ISO 8601）")
    args = parser.parse_args()
    try:
        retrieved_at = datetime.fromisoformat(args.retrieved_at)
        if retrieved_at.utcoffset() is None:
            raise ValueError("取得日時にタイムゾーンを指定してください")
        result = normalize(args.csv_file.read_bytes(), args.source_url, retrieved_at)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"正規化エラー：{error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
