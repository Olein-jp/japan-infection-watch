"""公開 JSON の形とファイル数を架空データで計測する。"""

from calendar import monthrange
from datetime import date, timedelta
from gzip import compress
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from build import boundaries, json_bytes


def measure(label, regions, diseases, daily, sample_regions):
    started = perf_counter()
    release = "sample-capacity"
    dataset = f"sample-{label}"
    kind = "municipality" if daily else "prefecture"
    year = 2030
    dates_by_month = {
        month: [date(year, month, day) for day in range(1, monthrange(year, month)[1] + 1)
                if daily or date(year, month, day).weekday() == 6]
        for month in range(1, 13)
    }
    rows = files = byte_count = compressed_bytes = index_bytes = 0
    largest_shard = largest_index = 0
    with TemporaryDirectory(prefix="jiw-pages-size-") as scratch:
        for index in range(sample_regions):
            region = f"sample-{index:04d}"
            region_path = Path(scratch) / region
            region_path.mkdir()
            index_entries = []
            for disease_number in range(diseases):
                disease = f"disease-{disease_number:02d}"
                latest = []
                for month, ending_dates in dates_by_month.items():
                    observations = []
                    for day in ending_dates:
                        for metric_number in range(2):
                            reported = (day.day + index + disease_number + metric_number) % 13 != 0
                            rate = metric_number == 1 and not daily
                            value = (day.toordinal() * 17 + disease_number * 7 + index) % 991
                            metric = "sentinel_reports_per_site" if rate else (
                                "class_closure_facility_count" if daily and metric_number == 1
                                else "school_closure_facility_count" if daily else "sentinel_report_count"
                            )
                            observations.append({
                                "dataset_id": dataset, "region_kind": kind, "region_id": region,
                                "disease_id": disease, "coverage_id": "sample-coverage",
                                "facility_group": "all_in_scope", "period_kind": "daily" if daily else "weekly",
                                "period_start": (day if daily else day - timedelta(days=6)).isoformat(),
                                "period_end": day.isoformat(), "metric_id": metric,
                                "unit": "case_per_sentinel" if rate else "facility" if daily else "case",
                                "value": (f"{value / 100:.2f}" if rate else value) if reported else None,
                                "value_status": "reported" if reported else "dash",
                                "denominator": None, "denominator_status": "not_provided" if rate else "not_applicable",
                                "version_id": f"sample-{day.isoformat()}", "edition_kind": "provisional",
                            })
                    latest = observations[-2:]
                    path = f"history/{dataset}/{kind}/{region}/{year}-{month:02d}/{disease}.json"
                    index_entries.append((path, observations, "history"))
                index_entries.append((f"latest/{dataset}/{kind}/{region}/{disease}.json", latest, "latest"))
            entries = []
            for relpath, observations, shard_kind in index_entries:
                payload = json_bytes({"schema_version": "0.1-draft", "release_id": release, "observations": observations})
                (region_path / relpath.replace("/", "_")).write_bytes(payload)
                rows += len(observations)
                files += 1
                byte_count += len(payload)
                compressed_bytes += len(compress(payload, mtime=0))
                largest_shard = max(largest_shard, len(payload))
                entries.append({
                    "kind": shard_kind, "path": f"releases/{release}/{relpath}",
                    "dataset_id": dataset, "region_kind": kind, "region_id": region,
                    "disease_id": Path(relpath).stem, "bytes": len(payload), "sha256": sha256(payload).hexdigest(),
                    **({"year_month": relpath.split("/")[-2]} if shard_kind == "history" else {}),
                })
            region_index = json_bytes({"files": entries})
            (region_path / "index.json").write_bytes(region_index)
            index_bytes += len(region_index)
            largest_index = max(largest_index, len(region_index))
        elapsed = perf_counter() - started
    return {
        "profile": label, "sample_regions": sample_regions, "scaled_regions": regions,
        "sample_seconds": round(elapsed, 3),
        "projected_seconds": round(elapsed * regions / sample_regions, 2),
        "rows": round(rows * regions / sample_regions),
        "shards": round(files * regions / sample_regions),
        "shard_bytes": round(byte_count * regions / sample_regions),
        "shard_gzip_bytes": round(compressed_bytes * regions / sample_regions),
        "all_region_index_bytes": round(index_bytes * regions / sample_regions),
        "max_region_index_bytes": largest_index, "max_shard_bytes": largest_shard,
    }


def geometry_size():
    simplified = boundaries()
    dense = boundaries()
    for feature in dense["features"]:
        ring = feature["geometry"]["coordinates"][0]
        coordinates = []
        for (x, y), (next_x, next_y) in zip(ring, ring[1:]):
            coordinates.extend([round(x + (next_x - x) * n / 50, 3),
                                round(y + (next_y - y) * n / 50, 3)] for n in range(50))
        coordinates.append(coordinates[0])
        feature["geometry"]["coordinates"][0] = coordinates
    return {
        "dense_vertices": 402, "simplified_vertices": 10,
        "dense_bytes": len(json_bytes(dense)), "simplified_bytes": len(json_bytes(simplified)),
    }


if __name__ == "__main__":
    print(json.dumps(measure("prefecture", 47, 19, False, 47)))
    print(json.dumps(measure("municipality", 1741, 6, True, 12)))
    print(json.dumps(measure("including-wards", 1918, 6, True, 12)))
    print(json.dumps(geometry_size()))
