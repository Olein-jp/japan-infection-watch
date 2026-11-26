"""架空の週次定点 CSV を開発用の共通観測 JSON に変換する。"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

from packages.data_model.observations import UNITS, validate_batch
from packages.data_normalizer.jihs_csv import AREAS, parse_weekly_csv


DATASET_ID = "sample-jihs-weekly"
LOCAL_DATASET_ID = "jihs-weekly-local"
FIXTURE_SOURCE = "https://example.invalid/jihs-weekly"
REGION_IDS = {name: f"{code:02}" for code, name in enumerate(AREAS)}
DISEASE_IDS = {
    "インフルエンザ": "influenza",
    "ＲＳウイルス感染症": "rs-virus",
    "咽頭結膜熱": "pharyngoconjunctival-fever",
    "Ａ群溶血性レンサ球菌咽頭炎": "group-a-streptococcal-pharyngitis",
    "感染性胃腸炎": "infectious-gastroenteritis",
    "水痘": "varicella",
    "手足口病": "hand-foot-and-mouth-disease",
    "伝染性紅斑": "erythema-infectiosum",
    "突発性発しん": "exanthema-subitum",
    "ヘルパンギーナ": "herpangina",
    "流行性耳下腺炎": "mumps",
    "急性出血性結膜炎": "acute-hemorrhagic-conjunctivitis",
    "流行性角結膜炎": "epidemic-keratoconjunctivitis",
    "細菌性髄膜炎": "bacterial-meningitis",
    "無菌性髄膜炎": "aseptic-meningitis",
    "マイコプラズマ肺炎": "mycoplasma-pneumonia",
    "クラミジア肺炎": "chlamydial-pneumonia",
    "感染性胃腸炎（ロタウイルス）": "rotavirus-gastroenteritis",
    "COVID-19": "covid-19",
}
METRICS = (
    ("report_count", "sentinel_report_count", "not_applicable"),
    ("reports_per_sentinel", "sentinel_reports_per_site", "not_provided"),
)


def normalize_fixture(raw: bytes, *, retrieved_at: datetime) -> dict:
    """明示的に架空入力として扱う。実資料の承認状態を引き受けない。"""
    return _normalize(raw, retrieved_at=retrieved_at, fictional=True)


def report_url(year: int, week: int) -> str:
    return f"https://id-info.jihs.go.jp/surveillance/idwr/provisional/{year}/{week:02d}/index.html"


def normalize_local(raw: bytes, *, retrieved_at: datetime) -> dict:
    """公式速報の CSV を、配布不可のローカル閲覧用観測に変換する。"""
    return _normalize(raw, retrieved_at=retrieved_at, fictional=False)


def _normalize(raw: bytes, *, retrieved_at: datetime, fictional: bool) -> dict:
    if retrieved_at.utcoffset() is None:
        raise ValueError("取得日時にタイムゾーンを指定してください")
    table = parse_weekly_csv(raw)
    records = table["records"]
    if {record["disease_label"] for record in records} != DISEASE_IDS.keys():
        raise ValueError("疾患見出しが検証済みの構成と異なります")

    year, week = table["reporting_year"], table["reporting_week"]
    dataset_id = DATASET_ID if fictional else LOCAL_DATASET_ID
    publication_key = f"{year}-W{week:02d}-provisional"
    digest = table["source_sha256"]
    version = {
        "id": f"{dataset_id}-{publication_key.lower()}-{digest}",
        "dataset_id": dataset_id,
        "publication_key": publication_key,
        "edition_kind": "provisional",
        "source_url": FIXTURE_SOURCE if fictional else report_url(year, week),
        "source_sha256": digest,
        "source_created_on": table["source_created_on"],
        "retrieved_at": retrieved_at.isoformat(),
        "reporting_year": year,
        "reporting_week": week,
        "supersedes": None,
        "publication_status": "blocked",
    }

    rows = []
    for record in records:
        region_code = REGION_IDS[record["area_label"]]
        common = {
            "dataset_id": dataset_id,
            "region_id": "jp" if region_code == "00" else region_code,
            "region_kind": record["area_level"],
            "disease_id": DISEASE_IDS[record["disease_label"]],
            "coverage_id": "sample-jihs-sentinel-sites" if fictional else "jihs-sentinel-sites",
            "facility_group": "all_in_scope",
            "period_kind": "weekly",
            "period_start": table["period_start"],
            "period_end": table["period_end"],
            "version_id": version["id"],
        }
        for source_field, metric, denominator_status in METRICS:
            cell = record[source_field]
            rows.append({
                **common,
                "metric_id": metric,
                "unit": UNITS[metric],
                "value": cell["value"],
                "value_status": "reported" if cell["status"] == "numeric" else cell["status"],
                "source_token": cell["source_token"],
                "denominator_status": denominator_status,
                "denominator": None,
            })

    validate_batch(rows, [version])
    # 内部の観測はローカル表示・検証用。本番の候補はこの入口から生成しない。
    return {"fictional": fictional, "versions": [version], "observations": rows, "public_candidates": []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="架空データだけを含む Shift_JIS CSV")
    parser.add_argument("--fixture", action="store_true", required=True, help="架空の入力であることを明示")
    parser.add_argument("--retrieved-at", required=True, help="実行記録用のタイムゾーン付き ISO 8601 日時")
    args = parser.parse_args()
    try:
        result = normalize_fixture(
            args.csv_file.read_bytes(), retrieved_at=datetime.fromisoformat(args.retrieved_at)
        )
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"正規化エラー：{error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, allow_nan=False)
    print()


if __name__ == "__main__":
    main()
