"""架空プレビューと JIHS 数値版の配布範囲・容量・整合性・差分を検証する。"""

import argparse
from datetime import date
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat


MAX_BYTES = 500_000_000
ID = re.compile(r"[a-z0-9][a-z0-9-]*")
REVISION = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"[0-9a-f]{64}")
MONTH = re.compile(r"[0-9]{4}-(?:0[1-9]|1[0-2])")
METADATA = re.compile(
    r"(<dt>(?:サイト生成日時|表示版の取得日時（架空）|CSV の読み込み日時)</dt><dd>)[^<]*(</dd>)".encode()
)
STATIC_ROOT = {"index.html", "404.html", "sources/index.html", "assets/site.css", "assets/site.js", "data/manifest.json"}
DISPLAY_FIELDS = {"period_start", "period_end", "metric_id", "unit", "value", "value_status", "version_id"}
VERSION_FIELDS = {"reporting_year", "reporting_week", "source_created_on", "retrieved_at"}
REFERENCE_FIELDS = {"path", "bytes", "sha256"}
SOURCE_FIELDS = {"attribution", "official_reference_url", "latest_period_end", "source_created_on",
                 "published_version_fetched_at", "delivery_status", "region_indexes"}


def check_fields(value, fields):
    if value.keys() != fields:
        raise ValueError("配布対象の項目が一致しません")


def digest(value):
    return sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def inventory(root, limit):
    if root.is_symlink() or not root.is_dir():
        raise ValueError("成果物のディレクトリを指定してください")

    def fail(error):
        raise error

    files = {}
    directories = set()
    total = 0
    for folder, subdirectories, filenames in os.walk(root, onerror=fail):
        for name in subdirectories + filenames:
            path = Path(folder) / name
            relative = path.relative_to(root).as_posix()
            metadata = path.lstat()
            if name.startswith("."):
                raise ValueError(f"隠しファイル・ディレクトリ: {relative}")
            if stat.S_ISDIR(metadata.st_mode):
                directories.add(relative)
                continue
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise ValueError(f"通常ファイル以外またはハードリンク: {relative}")
            total += metadata.st_size
            if total > limit:
                raise ValueError(f"容量超過: {total} バイト（上限 {limit} バイト）")
            files[relative] = metadata.st_size
    return files, directories, total


def comparable(value, release):
    if isinstance(value, list):
        return [comparable(item, release) for item in value]
    if not isinstance(value, dict):
        return value
    if value.keys() == REFERENCE_FIELDS:
        return {"path": value["path"].replace(f"releases/{release}/", "releases/current/", 1)}
    result = {key: comparable(item, release) for key, item in value.items()
              if key not in {"generated_at", "published_version_fetched_at", "local_input_read_at",
                             "input_read_at", "retrieved_at"}}
    if "release_id" in result:
        result["release_id"] = "current"
    return result


def verify_bundle(root, limit=MAX_BYTES, *, local_jihs=False, release_candidate=False,
                  published_jihs=False, expected_period_ends=None):
    if sum((local_jihs, release_candidate, published_jihs)) > 1:
        raise ValueError("検証する成果物の種類を1つ指定してください")
    pages_data = release_candidate or published_jihs
    real_data = local_jihs or pages_data
    files, directories, total = inventory(root, limit)
    raw_hashes = {}
    content_hashes = {}
    expected = set(STATIC_ROOT)

    def read(path):
        if path not in files:
            raise ValueError(f"参照先がありません: {path}")
        raw = (root / path).read_bytes()
        if len(raw) != files[path]:
            raise ValueError(f"検証中にサイズが変わりました: {path}")
        raw_hashes[path] = digest(raw)
        return raw

    manifest_path = "data/manifest.json"
    manifest = json.loads(read(manifest_path))
    check_fields(manifest, {"schema_version", "release_id", "generated_at", "fictional", "publication_status", "sources"})
    release = manifest["release_id"]
    release_prefix = "local-" if local_jihs else "preview-"
    label = "JIHS ローカル確認版" if local_jihs else "架空プレビュー"
    if pages_data:
        release_prefix = "candidate-"
        label = "JIHS 公開版" if published_jihs else "JIHS 公開候補"
    status = "pending_review" if release_candidate else "blocked"
    if published_jihs:
        status = "published"
    if not ID.fullmatch(release) or not release.startswith(release_prefix):
        raise ValueError(f"{label}の配布版 ID が必要です")
    if (manifest["schema_version"] != "0.1-draft" or manifest["fictional"] is not (not real_data)
            or manifest["publication_status"] != status):
        raise ValueError(f"{label}の公開状態またはデータ種別が不正です")

    dataset = "sample-jihs-weekly"
    source_fields = SOURCE_FIELDS
    provenance = {}
    if real_data:
        from apps.web.preview_data import LOCAL_ATTRIBUTION, LOCAL_PROCESSING
        from packages.data_normalizer.jihs_weekly import LOCAL_DATASET_ID, report_url

        dataset = "jihs-weekly" if pages_data else LOCAL_DATASET_ID
        timestamp_field = "input_read_at" if pages_data else "local_input_read_at"
        provenance = {"attribution": LOCAL_ATTRIBUTION, "processing": LOCAL_PROCESSING}
        source_fields = (SOURCE_FIELDS - {"published_version_fetched_at"}) | {timestamp_field, "processing"}

    def check_provenance(payload):
        for key, value in provenance.items():
            if payload[key] != value:
                raise ValueError("出典または編集・加工の明示がありません")
        rows = payload["observations"]
        versions = payload["versions"]
        if set(versions) != {row["version_id"] for row in rows}:
            raise ValueError("観測行と根拠資料の版が一致しません")
        for version in versions.values():
            check_fields(version, VERSION_FIELDS | ({"source_url"} if real_data else set()))
            if real_data and version["source_url"] != report_url(version["reporting_year"], version["reporting_week"]):
                raise ValueError("根拠資料の URL が対象週と一致しません")
        if real_data:
            for row in rows:
                version = versions[row["version_id"]]
                if date.fromisoformat(row["period_end"]).isocalendar() != (
                        version["reporting_year"], version["reporting_week"], 7):
                    raise ValueError("履歴と根拠資料の対象週が一致しません")

    def reference(entry, relative):
        check_fields(entry, REFERENCE_FIELDS)
        if entry["path"] != relative:
            raise ValueError(f"許可されていない参照先: {entry['path']}")
        path = "data/" + relative
        if path in expected:
            raise ValueError(f"参照先が重複しています: {path}")
        expected.add(path)
        raw = read(path)
        if len(raw) != entry["bytes"] or raw_hashes[path] != entry["sha256"]:
            raise ValueError(f"サイズまたは SHA-256 が一致しません: {path}")
        payload = json.loads(raw)
        if payload["release_id"] != release:
            raise ValueError(f"配布版が一致しません: {path}")
        logical = path.replace(f"/releases/{release}/", "/releases/current/", 1)
        content_hashes[logical] = digest(canonical(comparable(payload, release)))
        return payload

    content_hashes[manifest_path] = digest(canonical(comparable(manifest, release)))
    if set(manifest["sources"]) != {dataset}:
        raise ValueError("対象外のデータセットです")
    source = manifest["sources"][dataset]
    check_fields(source, source_fields)
    latest_end = date.fromisoformat(source["latest_period_end"])
    if expected_period_ends is not None and latest_end.isoformat() != max(expected_period_ends):
        raise ValueError("最新の対象週が承認済みの範囲と一致しません")
    if real_data:
        year, week, _ = latest_end.isocalendar()
        if (any(source[key] != value for key, value in provenance.items())
                or source["official_reference_url"] != report_url(year, week)):
            raise ValueError("manifest の出典または編集・加工の表示が不正です")
    indexes = source["region_indexes"]
    if set(indexes) != {"jp", *(f"{code:02}" for code in range(1, 48))}:
        raise ValueError("全国・47都道府県の地域索引が揃っていません")
    diseases = None
    for region, entry in sorted(indexes.items()):
        kind = "national" if region == "jp" else "prefecture"
        scope = f"{dataset}/{kind}/{region}"
        if kind == "prefecture":
            expected.add(f"prefectures/{region}/index.html")
        index = reference(entry, f"releases/{release}/index/{scope}.json")
        check_fields(index, {"release_id", "diseases"})
        codes = set(index["diseases"])
        if len(codes) != 19 or (diseases is not None and codes != diseases):
            raise ValueError("地域ごとの疾患索引が揃っていません")
        diseases = codes
        for disease, shards in index["diseases"].items():
            if not ID.fullmatch(disease):
                raise ValueError("疾患 ID が不正です")
            expected.add(f"diseases/{disease}/index.html")
            check_fields(shards, {"latest", "history"})
            prefix = f"releases/{release}"
            latest = reference(shards["latest"], f"{prefix}/latest/{scope}/{disease}.json")
            latest_fields = {"release_id", "observations"}
            if real_data:
                latest_fields |= {"versions", *provenance}
            check_fields(latest, latest_fields)
            if (len(latest["observations"]) != 2
                    or any(row.keys() != DISPLAY_FIELDS or row["period_end"] != latest_end.isoformat()
                           for row in latest["observations"])):
                raise ValueError("最新値の配布項目または対象週が不正です")
            if real_data:
                check_provenance(latest)
            if latest_end.isoformat()[:7] not in shards["history"]:
                raise ValueError("最新月の履歴がありません")
            history_period_ends = set()
            for month, item in shards["history"].items():
                if not MONTH.fullmatch(month):
                    raise ValueError("履歴の年月が不正です")
                history = reference(item, f"{prefix}/history/{scope}/{month}/{disease}.json")
                check_fields(history, {"release_id", "observations", "versions", *provenance})
                rows = history["observations"]
                if not rows or any(row.keys() != DISPLAY_FIELDS or row["period_end"][:7] != month for row in rows):
                    raise ValueError("履歴の配布項目または対象月が不正です")
                check_provenance(history)
                history_period_ends.update(row["period_end"] for row in rows)
            if expected_period_ends is not None and history_period_ends != expected_period_ends:
                raise ValueError("履歴の対象週が承認済みの範囲と一致しません")

    # #22 で確認済みの公式案内のみをプレビューの配布対象とする。
    expected.add("municipalities/21201/index.html")
    expected_directories = {parent.as_posix() for name in expected for parent in Path(name).parents
                            if parent != Path(".")}
    if set(files) != expected or directories != expected_directories:
        extra = sorted((set(files) - expected) | (directories - expected_directories))
        missing = sorted(expected - set(files))
        raise ValueError(f"配布範囲が不一致: 範囲外 {extra[:3]} / 不足 {missing[:3]}")
    notice = "自分用・ローカル閲覧" if local_jihs else "開発プレビュー"
    if pages_data:
        from apps.web.build import JIHS_PROVISIONAL

        notice = "JIHS の週次定点速報"
    for path in sorted(expected - raw_hashes.keys()):
        raw = read(path)
        if path.endswith(".html"):
            if notice.encode() not in raw:
                raise ValueError(f"{label}の表示がありません: {path}")
            if real_data and (path == "index.html" or path.startswith(("prefectures/", "diseases/"))):
                if any(value.encode() not in raw for value in (
                        "<dt>出典</dt>", "<dt>編集・加工</dt>", source["official_reference_url"], *provenance.values()
                )):
                    raise ValueError(f"出典または編集・加工の表示がありません: {path}")
                if pages_data and JIHS_PROVISIONAL.encode() not in raw:
                    raise ValueError(f"速報値が訂正される可能性の表示がありません: {path}")
            raw = METADATA.sub(rb"\1\2", raw)
            raw = raw.replace(f'data-release="{release}"'.encode(), b'data-release="current"')
            raw = raw.replace(f"/releases/{release}/".encode(), b"/releases/current/")
        content_hashes[path] = digest(raw)
    return {
        "bytes": total, "file_count": len(files), "sha256": digest(canonical(raw_hashes)),
        "content_sha256": digest(canonical(content_hashes)), "latest_period_end": latest_end.isoformat(),
    }


def evaluate(candidate, *, baseline=None, candidate_revision=None, expected_revision=None, limit=MAX_BYTES,
             local_jihs=False, release_candidate=False, expected_sha256=None):
    if candidate_revision is not None or expected_revision is not None:
        if not all(isinstance(value, str) and REVISION.fullmatch(value)
                   for value in (candidate_revision, expected_revision)):
            raise ValueError("候補と想定リビジョンには40桁の Git SHA を指定してください")
        if candidate_revision != expected_revision:
            raise ValueError("古い候補: 想定する Git リビジョンと一致しません")
    result = verify_bundle(candidate, limit, local_jihs=local_jihs, release_candidate=release_candidate)
    if expected_sha256 is not None:
        if not SHA256.fullmatch(expected_sha256):
            raise ValueError("候補一式の SHA-256 は64桁の小文字の16進数で指定してください")
        if result["sha256"] != expected_sha256:
            raise ValueError("候補一式の SHA-256 が照合済みの値と一致しません")
    change = "no_baseline"
    if baseline is not None:
        # 旧版の比較は現在の設定で許容する最大容量を上限に検証する。
        previous = verify_bundle(baseline, MAX_BYTES, local_jihs=local_jihs, release_candidate=release_candidate)
        if result["latest_period_end"] < previous["latest_period_end"]:
            raise ValueError("古い候補: 集計対象週が比較元より前です")
        change = "unchanged" if result["content_sha256"] == previous["content_sha256"] else "changed"
    return {**result, "change": change, "publication_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--candidate-revision")
    parser.add_argument("--expected-revision")
    parser.add_argument("--expected-sha256", help="照合済みの候補一式の SHA-256")
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--local-jihs", action="store_true", help="JIHS のローカル確認版を検証（公開不可）")
    mode.add_argument("--release-candidate", action="store_true", help="JIHS の公開候補を検証（承認前）")
    args = parser.parse_args()
    if (args.local_jihs or args.release_candidate) and not __package__:
        parser.error("JIHS 数値版はリポジトリのルートから python3 -m scripts.check_preview で実行してください")
    try:
        if not 0 < args.max_bytes <= MAX_BYTES:
            raise ValueError("容量上限は1〜500,000,000バイトの範囲を指定してください")
        report = evaluate(args.candidate, baseline=args.baseline, candidate_revision=args.candidate_revision,
                          expected_revision=args.expected_revision, limit=args.max_bytes, local_jihs=args.local_jihs,
                          release_candidate=args.release_candidate, expected_sha256=args.expected_sha256)
    except (OSError, KeyError, TypeError, ValueError, AttributeError) as error:
        parser.exit(2, f"プレビュー検証エラー: {error}\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
