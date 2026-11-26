"""F-001 の観測をローカルプレビュー用に分割する。"""

from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime
from hashlib import sha256
import json

from packages.data_model.observations import validate_batch
from packages.data_normalizer.jihs_weekly import (
    DATASET_ID, DISEASE_IDS, FIXTURE_SOURCE, LOCAL_DATASET_ID, METRICS, REGION_IDS, report_url,
)


REGIONS = {"jp": "全国", **{code: name for name, code in REGION_IDS.items() if code != "00"}}
DISEASES = {code: name for name, code in DISEASE_IDS.items()}
METRIC_IDS = tuple(metric for _, metric, _ in METRICS)
REGION_KEYS = {(code, "national" if code == "jp" else "prefecture") for code in REGIONS}
DATASET_KEYS = {(code, kind, disease, metric) for code, kind in REGION_KEYS
                for disease in DISEASES for metric in METRIC_IDS}
ATTRIBUTION = "架空データ（JIHS IDWR 週次定点速報 CSV の形式に基づく）"
LOCAL_ATTRIBUTION = "国立健康危機管理研究機構（JIHS）感染症情報提供サイト「IDWR速報データ」"
LOCAL_PROCESSING = "感染症動向ウォッチ（Japan Infection Watch）が速報 CSV の集計値を表示用に整形し、グラフと表を作成"
OFFICIAL_SOURCE = "https://id-info.jihs.go.jp/surveillance/idwr/"
OFFICIAL_ARCHIVE = "https://id-info.jihs.go.jp/surveillance/idwr/provisional/sokuhou.html"
SCHOOL_HEALTH_MAP = "https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping"
HISTORY_MONTHS = 6
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


def history_start(end, months=HISTORY_MONTHS):
    year, month_index = divmod(end.year * 12 + end.month - 1 - months, 12)
    month = month_index + 1
    return date(year, month, min(end.day, monthrange(year, month)[1]))


def prepare(batches, *, fictional=True):
    """各週の完全な F-001 出力を受け入れ、同じ週の競合は明示的に拒否する。"""
    by_week = {}
    dataset_id = DATASET_ID if fictional else LOCAL_DATASET_ID
    input_label = "F-001 の架空データ" if fictional else "ローカル閲覧用の JIHS 速報データ"
    for batch in batches:
        if batch.get("fictional") is not fictional or batch.get("public_candidates") != []:
            raise ValueError(f"{input_label}だけを指定してください")
        version, = batch["versions"]
        if (version["publication_status"] != "blocked" or version["dataset_id"] != dataset_id
                or version["edition_kind"] != "provisional"):
            raise ValueError(f"公開対象外の速報版が必要です（{input_label}）")
        expected_source = FIXTURE_SOURCE if fictional else report_url(
            version["reporting_year"], version["reporting_week"]
        )
        if version["source_url"] != expected_source:
            raise ValueError("対象週の出典が一致しません")
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
        raise ValueError(f"{input_label}を指定してください")

    newest = max(by_week)
    first = history_start(newest)
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
    version_fields = ("reporting_year", "reporting_week", "source_created_on", "retrieved_at")
    if not fictional:
        version_fields += ("source_url",)
    versions = {version["id"]: {field: version[field] for field in version_fields}
                for version, _ in (by_week[end] for end in weeks)}
    return latest, history, by_week[newest][0], versions


def write_distribution(root, release_id, generated_at, latest, history, version, versions, *,
                       fictional, release_candidate=False):
    prefix = f"releases/{release_id}"
    dataset_id = "jihs-weekly" if release_candidate else version["dataset_id"]
    indexes = {}
    provenance = {} if fictional else {"attribution": LOCAL_ATTRIBUTION, "processing": LOCAL_PROCESSING}

    def write(relative, content):
        path = root / "data" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = json_bytes(content)
        path.write_bytes(data)
        return {"path": relative, "bytes": len(data), "sha256": sha256(data).hexdigest()}

    for region in REGIONS:
        kind = "national" if region == "jp" else "prefecture"
        scope = f"{dataset_id}/{kind}/{region}"
        diseases = {}
        trend = {}
        for disease in DISEASES:
            current = list(latest[region, disease].values())
            months = {}
            for month, rows in history[region, disease].items():
                months[month] = write(f"{prefix}/history/{scope}/{month}/{disease}.json", {
                    "release_id": release_id, "observations": rows,
                    "versions": {key: versions[key] for key in sorted({row["version_id"] for row in rows})},
                    **provenance,
                })
            latest_provenance = {"versions": {version["id"]: versions[version["id"]]}, **provenance} if provenance else {}
            diseases[disease] = {
                "latest": write(f"{prefix}/latest/{scope}/{disease}.json", {
                    "release_id": release_id, "observations": current, **latest_provenance,
                }),
                "history": months,
            }
            if kind == "prefecture":
                trend[disease] = [
                    [row["period_end"], row["value_status"], row["value"]]
                    for rows in history[region, disease].values() for row in rows
                    if row["metric_id"] == "sentinel_reports_per_site"
                ]
        index = {"release_id": release_id, "diseases": diseases}
        if trend:
            index["trend"] = trend
        indexes[region] = write(f"{prefix}/index/{scope}.json", index)

    timestamp_field = "published_version_fetched_at" if fictional else "local_input_read_at"
    if release_candidate:
        timestamp_field = "input_read_at"
    write("manifest.json", {
        "schema_version": "0.1-draft", "release_id": release_id, "generated_at": generated_at,
        "fictional": fictional, "publication_status": "pending_review" if release_candidate else "blocked",
        "sources": {dataset_id: {
            "attribution": ATTRIBUTION,
            **provenance,
            "official_reference_url": OFFICIAL_SOURCE if fictional else version["source_url"],
            "latest_period_end": next(iter(latest["jp", next(iter(DISEASES))].values()))["period_end"],
            "source_created_on": version["source_created_on"],
            timestamp_field: version["retrieved_at"],
            "delivery_status": "unknown",
            "region_indexes": indexes,
        }},
    })
    return indexes
