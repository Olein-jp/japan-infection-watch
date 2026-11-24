"""国土数値情報 N03 の2026年版から岐阜市の境界を変換して照合する。"""

import argparse
import json
from pathlib import Path

import fiona
from pyproj import Geod, Transformer
from shapely import orient_polygons, transform
from shapely.geometry import mapping, shape

SOURCE_STEM = "N03-20260101_21"
AREA_CODE = "21201"


def verify_boundary(source: Path, output: Path) -> None:
    with fiona.open(source / f"{SOURCE_STEM}.shp") as boundaries:
        if boundaries.crs.to_epsg() != 6668:
            raise ValueError("入力の座標参照系が JGD2011（EPSG:6668）ではありません")
        features = [f for f in boundaries if f.properties["N03_007"] == AREA_CODE]

    if len(features) != 1:
        raise ValueError(f"検証版で岐阜市の地物を1件想定しています。該当件数 {len(features)}")
    feature = features[0]
    if (feature.properties["N03_001"], feature.properties["N03_004"]) != ("岐阜県", "岐阜市"):
        raise ValueError("コードに対応する都道府県名または市町村名が一致しません")

    original = shape(feature.geometry)
    if original.geom_type not in {"Polygon", "MultiPolygon"} or original.is_empty or not original.is_valid:
        raise ValueError("入力の境界が有効な面ではありません")

    project = Transformer.from_crs(6668, 4326, always_xy=True, allow_ballpark=False)
    geometry = orient_polygons(transform(original, project.transform, interleaved=False))
    if not geometry.is_valid:
        raise ValueError("変換後の境界が無効です")

    reference = json.loads((source / f"{SOURCE_STEM}.geojson").read_bytes())
    reference_crs = reference.get("crs", {}).get("properties", {}).get("name")
    if reference_crs != "urn:ogc:def:crs:EPSG::6668":
        raise ValueError("照合元の GeoJSON が想定した EPSG:6668 ではありません")
    reference_features = [f for f in reference["features"] if f["properties"]["N03_007"] == AREA_CODE]
    if len(reference_features) != 1:
        raise ValueError("照合元の GeoJSON で岐阜市の地物を一意に特定できません")
    reference_feature = reference_features[0]
    if dict(feature.properties) != reference_feature["properties"]:
        raise ValueError("シェープファイルと配布 GeoJSON の属性が一致しません")

    reference_geometry = transform(shape(reference_feature["geometry"]), project.transform, interleaved=False)
    # 配布 GeoJSON の MultiPolygon と元のシェープファイルの面を同じ単位で比較する。
    if reference_geometry.geom_type == "MultiPolygon" and len(reference_geometry.geoms) == 1:
        reference_geometry = reference_geometry.geoms[0]
    if not geometry.equals_exact(reference_geometry, tolerance=1e-8, normalize=True):
        raise ValueError("シェープファイルの変換結果と配布 GeoJSON の境界が一致しません")

    area_m2, _ = Geod(ellps="WGS84").geometry_area_perimeter(geometry)
    result = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "id": AREA_CODE,
            "geometry": mapping(geometry),
            "properties": {
                "area_code": AREA_CODE,
                "municipality_name": feature.properties["N03_004"],
                "boundary_as_of": "2026-01-01",
                "source": "国土数値情報（行政区域データ）2026年版（国土交通省）を加工",
                "source_url": "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2026.html",
                "license": "CC BY 4.0",
                "license_url": "https://creativecommons.org/licenses/by/4.0/",
            },
        }],
    }
    encoded = json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    with output.open("x", encoding="utf-8") as stream:
        stream.write(encoded + "\n")

    print(f"{AREA_CODE} 岐阜市の属性・境界が配布 GeoJSON と一致（許容差 1e-8 度）")
    print(f"{geometry.geom_type} 1地物、面積 {abs(area_m2) / 1_000_000:.3f} km²")
    print("境界範囲（西・南・東・北）", tuple(round(x, 6) for x in geometry.bounds))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="公式 ZIP を展開したディレクトリ")
    parser.add_argument("output", type=Path, help="新規の GeoJSON ファイル")
    args = parser.parse_args()
    try:
        verify_boundary(args.source, args.output)
    except (OSError, ValueError, fiona.errors.FionaError) as error:
        parser.exit(2, f"照合停止: {error}\n")


if __name__ == "__main__":
    main()
