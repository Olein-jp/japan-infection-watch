"""架空データの Pages 用ビルドと、成功版のローカル切り替え。"""

import argparse
from collections import defaultdict
from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parents[1] / "tests/fixtures/r15-observations.json"
sys.path.insert(0, str(HERE.parent / "data-model"))
from verify_rules import observation_key, series_key, validate_batch

DATASET = "sample-sentinel"
DISEASE = "influenza"
REGIONS = {"sample-a": "青葉県（架空）", "sample-b": "白波県（架空）"}
SAFE_ID = r"[a-z0-9][a-z0-9-]*"


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def write(root, name, content):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content if isinstance(content, bytes) else content.encode())


def html_page(base, heading, content, *, script=False):
    script_tag = f'<script type="module" src="{base}assets/region.js"></script>' if script else ""
    return f"""<!doctype html>
<html lang="ja">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(heading)} | 感染症データの配信試験</title>
<link rel="stylesheet" href="{base}assets/style.css">
<header><a href="{base}">感染症データの配信試験</a><span>架空データ</span></header>
<main><h1>{escape(heading)}</h1>{content}</main>
{script_tag}
</html>
"""


def boundaries():
    # 架空の図形。直線辺の中間点を除いた後の形状を1件ずつ配布する。
    features = []
    for region, left in (("sample-a", 0), ("sample-b", 45)):
        ring = [[left, 0], [left + 40, 0], [left + 40, 26], [left, 26], [left, 0]]
        features.append({
            "type": "Feature", "id": region, "properties": {"name": REGIONS[region]},
            "geometry": {"type": "Polygon", "coordinates": [ring]},
        })
    return {"type": "FeatureCollection", "features": features}


def build(root, base, release, reject_candidate):
    fixture = json.loads(FIXTURE.read_bytes())
    if fixture.get("fictional") is not True:
        raise ValueError("架空データの明示が必要です")
    validate_batch(fixture["observations"], fixture["versions"])
    versions = {
        version["id"]: version for version in fixture["versions"] if version["dataset_id"] == DATASET
    }
    rank = {"sentinel-a": 0, "sentinel-b": 1}
    observations = {}
    for row in fixture["observations"]:
        if row["dataset_id"] != DATASET or row["region_id"] not in REGIONS:
            continue
        key = observation_key(row)
        if key not in observations or rank[row["version_id"]] > rank[observations[key]["version_id"]]:
            observations[key] = {k: v for k, v in row.items() if k != "source_token"}
            observations[key]["edition_kind"] = "provisional"
    if any(row["version_id"] not in versions for row in observations.values()):
        raise ValueError("版が確認できない観測があります")

    asset_dir = root / "assets"
    asset_dir.mkdir()
    for asset in ("style.css", "region.js"):
        shutil.copyfile(HERE / asset, asset_dir / asset)
    links = "".join(f'<li><a href="{base}regions/{key}/">{name}</a></li>' for key, name in REGIONS.items())
    write(root, "index.html", html_page(base, "地域を選ぶ", f"<ul>{links}</ul>"))
    write(root, "404.html", html_page(base, "ページが見つかりません", f'<p><a href="{base}">トップへ戻る</a></p>'))

    manifest = {
        "schema_version": "0.1-draft", "release_id": release,
        "generated_at": "2030-01-22T09:00:00+09:00",
        "sources": {DATASET: {
            "attribution": "架空の提供元・週次定点集計",
            "coverage": [{"region_kind": "prefecture", "region_id": region} for region in REGIONS],
            "latest_period_end": "2030-01-13", "source_updated_on": "2030-01-16",
            "last_fetch_succeeded_at": "2030-01-21T08:50:00+09:00",
            "published_version_fetched_at": "2030-01-20T08:50:00+09:00",
            "last_source_checked_at": "2030-01-21T08:50:00+09:00",
            "delivery_status": "unknown",
            "next_update_due_at": "2030-01-23T18:17:00+09:00",
        }},
        "files": [],
    }

    def publish(kind, path, payload, **dimensions):
        relative = f"releases/{release}/{path}"
        body = json_bytes(payload)
        write(root, f"data/{relative}", body)
        manifest["files"].append({
            "kind": kind, "path": relative, "bytes": len(body),
            "sha256": sha256(body).hexdigest(), **dimensions,
        })

    for region, name in REGIONS.items():
        content = f"""<section id="data" data-region="{region}" data-manifest="{base}data/manifest.json">
<p id="status" role="status">データを読み込み中です。</p>
<p id="age"></p>
<dl id="freshness"></dl>
<table><caption>週次の定点集計</caption><thead><tr>
<th scope="col">指標</th><th scope="col">値</th><th scope="col">対象期間</th>
</tr></thead><tbody id="latest"></tbody></table>
<figure><figcaption>架空の行政区域と報告状況</figcaption><div id="map"></div>
<p id="legend"></p></figure>
<button id="history-button" type="button" disabled>対象月の履歴を表示</button>
<ul id="history"></ul><p id="source"></p>
</section>"""
        write(root, f"regions/{region}/index.html", html_page(base, name, content, script=True))

        latest = {}
        by_month = defaultdict(list)
        for row in observations.values():
            if row["region_id"] != region:
                continue
            key = series_key(row)
            if key not in latest or row["period_end"] > latest[key]["period_end"]:
                latest[key] = row
            by_month[row["period_end"][:7]].append(row)

        dimensions = dict(dataset_id=DATASET, region_kind="prefecture", region_id=region, disease_id=DISEASE)
        publish("latest", f"latest/{DATASET}/prefecture/{region}/{DISEASE}.json",
                {"schema_version": "0.1-draft", "release_id": release, "observations": list(latest.values())},
                **dimensions)
        for month, rows in by_month.items():
            publish("history", f"history/{DATASET}/prefecture/{region}/{month}/{DISEASE}.json",
                    {"schema_version": "0.1-draft", "release_id": release, "observations": rows},
                    year_month=month, **dimensions)
    publish("map", "map/prefecture.geojson", boundaries())
    write(root, "data/manifest.json", json_bytes(manifest))
    if reject_candidate:
        first_path = manifest["files"][0]["path"]
        write(root, f"data/{first_path}", b"{}")

    for entry in manifest["files"]:
        body = (root / "data" / entry["path"]).read_bytes()
        if len(body) != entry["bytes"] or sha256(body).hexdigest() != entry["sha256"]:
            raise ValueError(f"公開候補のハッシュまたはサイズが不一致: {entry['path']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("release")
    parser.add_argument("--base", default="/japan-infection-watch/")
    parser.add_argument("--reject-candidate", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(SAFE_ID, args.release) or not re.fullmatch(rf"/(?:{SAFE_ID}/)?", args.base):
        parser.error("版 ID または base path が不正です")

    workspace = args.workspace.resolve()
    archive = workspace / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    release = archive / args.release
    started = perf_counter()
    if release.exists():
        parser.exit(2, "この版 ID は既に使用済みです\n")
    try:
        with TemporaryDirectory(dir=workspace) as staging:
            candidate = Path(staging) / "dist"
            candidate.mkdir()
            build(candidate, args.base, args.release, args.reject_candidate)
            candidate.rename(release)
            pointer = Path(staging) / "next"
            pointer.symlink_to(release, target_is_directory=True)
            os.replace(pointer, workspace / "active")
    except (OSError, ValueError) as error:
        parser.exit(2, f"公開候補を停止: {error}\n")
    files = [file for file in release.rglob("*") if file.is_file()]
    print(json.dumps({"release": args.release, "files": len(files), "bytes": sum(f.stat().st_size for f in files),
                      "wall_seconds": round(perf_counter() - started, 3)}))


if __name__ == "__main__":
    main()
