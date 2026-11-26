"""週次の静的配布を架空データで計測する。"""

from argparse import ArgumentParser
from collections import defaultdict
from datetime import date, datetime, timedelta
from gzip import compress
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
from tempfile import TemporaryDirectory

from apps.web.build import build
from apps.web.preview_data import DATASET_ID, HISTORY_MONTHS, history_start, json_bytes
from fixtures.jihs_weekly import csv_bytes, fixture_table
from packages.data_normalizer.jihs_weekly import normalize_fixture
from scripts.check_preview import verify_bundle


END = date(2030, 2, 3)
GENERATED = "2030-02-06T09:00:00+09:00"


def sample(weeks):
    batches = []
    for offset in reversed(range(weeks)):
        end = END - timedelta(weeks=offset)
        start = end - timedelta(days=6)
        created = end + timedelta(days=2)
        year, week, _ = end.isocalendar()
        table = fixture_table()
        table[1][:2] = [
            f"{year}年{week}週({start.month}月{start.day}日〜{end.month}月{end.day}日)",
            f"{created.year}年{created.month}月{created.day}日作成",
        ]
        for region, row in enumerate(table[4:]):
            for column in range(1, len(row), 2):
                number = (region * 103 + column * 17 + offset * 71) % 1913
                row[column:column + 2] = (
                    [str(number), f"{number / 47:.2f}"] if number % 89 else ["-", ""]
                )
        retrieved = datetime.fromisoformat(f"{created}T18:00:00+09:00")
        batches.append(normalize_fixture(csv_bytes(table), retrieved_at=retrieved))
    return batches


def measurements(payloads):
    return {name: {"median": round(median(values)), "max": max(values)} for name, values in payloads.items()}


def compare(root):
    data = root / "data"
    paths = [path for path in root.rglob("*") if path.is_file()]
    original_bytes = sum(path.stat().st_size for path in paths)
    total = original_bytes
    size = len(paths)
    maximum = max(path.stat().st_size for path in paths)
    manifest_body = (data / "manifest.json").read_bytes()
    manifest = json.loads(manifest_body)
    release = manifest["release_id"]
    current_payloads = defaultdict(list)
    grouped_payloads = defaultdict(list)
    months = set()
    index_bytes = []
    grouped_index_bytes = []
    grouped_indexes = {}
    for region, entry in manifest["sources"][DATASET_ID]["region_indexes"].items():
        index_body = (data / entry["path"]).read_bytes()
        current_index = json.loads(index_body)
        history = defaultdict(dict)
        versions = defaultdict(dict)
        grouped_size_by_month = {}
        grouped_gzip_by_month = {}
        grouped_references = {}
        compressed_index = len(compress(index_body, mtime=0))

        for disease, ref in current_index["diseases"].items():
            for month, shard in ref["history"].items():
                raw = (data / shard["path"]).read_bytes()
                decoded = json.loads(raw)
                history[month][disease] = decoded["observations"]
                versions[month].update(decoded["versions"])
                current_payloads["history_raw"].append(len(raw))
                current_payloads["first_raw"].append(len(index_body) + len(raw))
                current_payloads["history_gzip"].append(len(compress(raw, mtime=0)))
                current_payloads["first_gzip"].append(compressed_index + current_payloads["history_gzip"][-1])
                size -= 1
                total -= len(raw)
        for month, observations in sorted(history.items()):
            months.add(month)
            body = json_bytes({"release_id": release, "observations_by_disease": observations, "versions": versions[month]})
            grouped_size_by_month[month] = len(body)
            grouped_gzip_by_month[month] = len(compress(body, mtime=0))
            filename = entry["path"].replace("/index/", "/history/", 1).removesuffix(".json") + f"/{month}.json"
            grouped_references[month] = {"path": filename, "bytes": len(body), "sha256": sha256(body).hexdigest()}
            assert len(observations) == len(current_index["diseases"])
        group_index = json_bytes({
            "release_id": release,
            "latest": {disease: ref["latest"] for disease, ref in current_index["diseases"].items()},
            "history": grouped_references,
        })
        grouped_indexes[region] = {"path": entry["path"], "bytes": len(group_index), "sha256": sha256(group_index).hexdigest()}
        compressed_group_index = len(compress(group_index, mtime=0))
        index_bytes.append(len(index_body))
        grouped_index_bytes.append(len(group_index))
        for month, raw_size in grouped_size_by_month.items():
            raw_gzip = grouped_gzip_by_month[month]
            for _ in history[month]:
                grouped_payloads["history_raw"].append(raw_size)
                grouped_payloads["first_raw"].append(len(group_index) + raw_size)
                grouped_payloads["history_gzip"].append(raw_gzip)
                grouped_payloads["first_gzip"].append(compressed_group_index + raw_gzip)
        size += len(history)
        total += sum(grouped_size_by_month.values()) + len(group_index) - len(index_body)

    manifest["sources"][DATASET_ID]["region_indexes"] = grouped_indexes
    total += len(json_bytes(manifest)) - len(manifest_body)
    return {
        "months": sorted(months),
        "current": {"files": len(paths), "bytes": original_bytes,
                    "max_file_bytes": maximum, "index_max": max(index_bytes), **measurements(current_payloads)},
        "grouped": {"files": size, "bytes": total, "index_max": max(grouped_index_bytes),
                    **measurements(grouped_payloads)},
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--months", type=int, choices=(4, HISTORY_MONTHS), default=HISTORY_MONTHS)
    args = parser.parse_args()
    start = history_start(END, args.months)
    weeks = (END - start).days // 7 + 1
    with TemporaryDirectory() as directory:
        site = Path(directory) / "site"
        build(sample(weeks), site, base="/", generated_at=GENERATED)
        verified = verify_bundle(site)
        report = compare(site)
        assert report["current"]["files"] == verified["file_count"]
        assert report["current"]["bytes"] == verified["bytes"]
        print(json.dumps({"cutoff": start.isoformat(), "weeks": weeks, **report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
