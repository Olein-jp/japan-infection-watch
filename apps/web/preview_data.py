"""F-001 の観測をローカルプレビュー用に分割する。"""

from collections import defaultdict
from datetime import date, datetime, timedelta
from hashlib import sha256
import json

from packages.data_model.observations import validate_batch
from packages.data_normalizer.jihs_weekly import DATASET_ID, DISEASE_IDS, METRICS, REGION_IDS


REGIONS = {"jp": "全国", **{code: name for name, code in REGION_IDS.items() if code != "00"}}
DISEASES = {code: name for name, code in DISEASE_IDS.items()}
METRIC_IDS = tuple(metric for _, metric, _ in METRICS)
REGION_KEYS = {(code, "national" if code == "jp" else "prefecture") for code in REGIONS}
DATASET_KEYS = {(code, kind, disease, metric) for code, kind in REGION_KEYS
                for disease in DISEASES for metric in METRIC_IDS}
ATTRIBUTION = "架空データ（JIHS IDWR 週次定点速報 CSV の形式に基づく）"
OFFICIAL_SOURCE = "https://id-info.jihs.go.jp/surveillance/idwr/"
MUNICIPALITIES = {
    "21201": ("岐阜市", "21", "インフルエンザについて", "https://www.city.gifu.lg.jp/kenko/kansensyou/1004450/1004453.html"),
}


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def parse_timestamp(value):
    timestamp = datetime.fromisoformat(value)
    if timestamp.utcoffset() is None:
        raise ValueError("日時にタイムゾーンを指定してください")
    return timestamp


def prepare(batches):
    """各週の完全な F-001 出力を受け入れ、同じ週の競合は明示的に拒否する。"""
    by_week = {}
    for batch in batches:
        if batch.get("fictional") is not True or batch.get("public_candidates") != []:
            raise ValueError("F-001 の架空データだけを指定してください")
        version, = batch["versions"]
        if (version["publication_status"] != "blocked" or version["dataset_id"] != DATASET_ID
                or version["edition_kind"] != "provisional"):
            raise ValueError("公開対象外の架空の速報版が必要です")
        if version["source_url"] != "https://example.invalid/jihs-weekly":
            raise ValueError("架空の出典が必要です")
        parse_timestamp(version["retrieved_at"])
        date.fromisoformat(version["source_created_on"])
        rows = batch["observations"]
        validate_batch(rows, [version])
        end = date.fromisocalendar(version["reporting_year"], version["reporting_week"], 7)
        if (len(rows) != len(DATASET_KEYS)
                or {(row["region_id"], row["region_kind"], row["disease_id"], row["metric_id"])
                    for row in rows} != DATASET_KEYS
                or any(row["period_kind"] != "weekly" or row["period_end"] != end.isoformat()
                       for row in rows)):
            raise ValueError("対象週・地域・疾患・指標が F-001 の出力範囲と一致しません")
        if end in by_week:
            raise ValueError("同じ報告週に複数の入力があります。採用版を1つ指定してください")
        by_week[end] = (version, rows)
    if not by_week:
        raise ValueError("架空の週次入力を指定してください")

    newest = max(by_week)
    first = newest - timedelta(weeks=51)
    weeks = sorted(end for end in by_week if end >= first)
    history = defaultdict(lambda: defaultdict(list))
    latest = {}
    for end in weeks:
        _, rows = by_week[end]
        for row in rows:
            key = (row["region_id"], row["disease_id"])
            cell = {field: row[field] for field in (
                "period_start", "period_end", "metric_id", "unit", "value", "value_status", "version_id",
            )}
            history[key][end.isoformat()[:7]].append(cell)
            if end == newest:
                latest.setdefault(key, {})[row["metric_id"]] = cell
    versions = {by_week[end][0]["id"]: {
        "reporting_year": by_week[end][0]["reporting_year"],
        "reporting_week": by_week[end][0]["reporting_week"],
        "source_created_on": by_week[end][0]["source_created_on"],
        "retrieved_at": by_week[end][0]["retrieved_at"],
    } for end in weeks}
    return latest, history, by_week[newest][0], versions


def write_distribution(root, release_id, generated_at, latest, history, version, versions):
    prefix = f"releases/{release_id}"
    indexes = {}

    def write(relative, content):
        path = root / "data" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = json_bytes(content)
        path.write_bytes(data)
        return {"path": relative, "bytes": len(data), "sha256": sha256(data).hexdigest()}

    for region in REGIONS:
        kind = "national" if region == "jp" else "prefecture"
        scope = f"{DATASET_ID}/{kind}/{region}"
        diseases = {}
        for disease in DISEASES:
            current = list(latest[region, disease].values())
            months = {}
            for month, rows in history[region, disease].items():
                months[month] = write(f"{prefix}/history/{scope}/{month}/{disease}.json", {
                    "release_id": release_id, "observations": rows,
                    "versions": {key: versions[key] for key in sorted({row["version_id"] for row in rows})},
                })
            diseases[disease] = {
                "latest": write(f"{prefix}/latest/{scope}/{disease}.json", {
                    "release_id": release_id, "observations": current,
                }),
                "history": months,
            }
        indexes[region] = write(f"{prefix}/index/{scope}.json", {"release_id": release_id, "diseases": diseases})

    write("manifest.json", {
        "schema_version": "0.1-draft", "release_id": release_id, "generated_at": generated_at,
        "fictional": True, "publication_status": "blocked",
        "sources": {DATASET_ID: {
            "attribution": ATTRIBUTION, "official_reference_url": OFFICIAL_SOURCE,
            "latest_period_end": next(iter(latest["jp", next(iter(DISEASES))].values()))["period_end"],
            "source_created_on": version["source_created_on"],
            "published_version_fetched_at": version["retrieved_at"],
            "delivery_status": "unknown",
            "region_indexes": indexes,
        }},
    })
    return indexes
