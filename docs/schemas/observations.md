# 共通観測データモデル案

[R-15 の調査結果と確認範囲](../findings/R-15-data-model.md)を参照。以下は調査段階の案。ID、内容、数値を含む例は架空。

## 観測と来歴

| 対象 | 項目 | 定義 |
|---|---|---|
| 提供元とデータセット | `source_id`、`dataset_id`、提供者名、集計制度 | 同じ提供者の異なる集計制度・系列に個別のデータセット ID を割り当てる |
| 地域 | `region_kind`、`region_id`、`source_region_label`、必要時に行政区域のコードと基準日 | 全国・都道府県・市区町村・行政区・保健所管轄・医療圏を区別。行政区域全域との一致を確認していない報告区分には `reporting_prefecture`・`reporting_city` を使い、提供元に紐付く ID を持つ。[地域照合の項目案](region-crosswalk.md) |
| 集計対象 | `coverage_id`、対象施設・定点種別、集計対象・除外の記述、`facility_group` | 同じ指標でも対象が変われば別系列。施設種別の内訳と全対象を区別。確認できない分母や対象校の範囲は明示する |
| 対象期間 | `period_start`、`period_end`、`period_kind`、出典の報告年・週またはシーズン | 期間の両端を含む JST 日付。日次、週次、シーズン累計を区別。年またぎは提供元の週対応表に従う。ページの掲載日と集計対象日は別項目 |
| 観測 | `disease_id`、`metric_id`、`unit`、`value`、`value_status`、`source_token` | インフルエンザとインフルエンザ様疾患を別 ID にする。件数は非負整数、率は出典の表示精度を保持する十進文字列。原表の文字列は照合用に保持 |
| 分母 | `denominator_status`、`denominator`、分母の単位・範囲 | `known` は提供元に根拠のある分母、`not_provided` は分母未提供、`not_applicable` は分母を用いない指標。定点当たりの数値を分母へ逆算しない |
| 原本と版 | `version_id`、`publication_key`、資料区分、原本 URL、表・列・ページ、SHA-256、`supersedes`、変更根拠 | 同一データセットの同じ号・資料区分を `publication_key` で識別する。原本のハッシュが同一なら再取得を記録し、同じ原本版を参照する。差し替えは別版とし、確認できた訂正元を `supersedes` で指す。速報・週報・年報には別の資料区分を割り当て、同じ観測の対応が確認できた場合に比較する |
| 利用条件 | `publication_status`、条件の出典・適用範囲・確認日、権利と集計粒度の判断、公開用出典文 | `allowed`・`pending`・`blocked`。加工・再公開に必要な条件を満たした `allowed` の範囲だけを公開用に変換する。原本の取得・保存と再公開の判断は個別に記録する |

観測キーは `dataset_id, region_id, region_kind, disease_id, coverage_id, facility_group, metric_id, unit, period_kind, period_start, period_end`。同一版内で一意とし、保存時は `version_id` と組み合わせる。観測キーから期間の開始・終了を外したものを系列キーとする。系列が異なる値を一律に比較・加算しない。集計公表ごとに同じキーが並ぶ場合は版の選択・訂正の根拠を記録する。

## 指標の対応

| 指標 ID | 単位 | 対象範囲・期間・分母 |
|---|---|---|
| `sentinel_report_count` | `case` | JIHS の定点の週次報告件数。対象は報告定点 |
| `sentinel_reports_per_site` | `case_per_sentinel` | JIHS の定点当たり報告数。試験対象 CSV には分母の定点数欄がない。小数第2位の表示値を保持 |
| `closure_affected_facility_count`・`school_closure_facility_count`・`grade_closure_facility_count`・`class_closure_facility_count` | `facility` | 厚労省 PDF の休業措置に関連する施設数、休校、学年閉鎖学校数、学級閉鎖学校数。当週とシーズン累計は別期間。施設種別は全国当週に掲載された内訳の範囲で扱う |
| `closure_enrolled_person_count`・`closure_patient_person_count`・`closure_absent_patient_count` | `person` | 厚労省 PDF の休業措置直前の対象範囲での人数。欠席者は患者の内数。「在籍者」は全国の全在籍者数を意味しない |
| 出席停止人数、閉鎖中のクラス数、新規閉鎖件数、複数種別の合算 | 確認待ち | 学校保健会の実データの定義、計上時点、分母、対象施設を #5〜#7 で確認。閉鎖実施学校数や定点報告数との代用や換算を行わない |

## 値の状態と更新時刻

| 項目 | 状態・型 | 扱い |
|---|---|---|
| `value_status` | `reported` | 原表が数値を公表。件数の `0`、丸めた率の `"0.00"` はいずれも表示値を保持 |
| `value_status` | `blank`、`dash`、`unknown_count`、`not_reported`、`suppressed`、`not_applicable` | `value` は null。空欄、意味が特定できないハイフン、出典に定義がある計数不明、未報告、秘匿、対象外を区別する。出典の明示や適用条件がなければ未報告・秘匿などと推定しない |
| 対象期間と提供元時刻 | `period_end`、`source_updated_on` または `source_updated_at` | 提供元が日付しか示さない場合は時刻を作らない。日付とオフセット付き日時を型として区別 |
| 取得と公開の時刻 | `last_attempted_at`、`last_fetch_succeeded_at`、`published_version_fetched_at`、`generated_at` | ISO 8601 のオフセット付き日時。取得成功後の品質検査で棄却された版と現在の公開版を区別する |
| 運用状態 | `last_attempt_status`（`succeeded`・`failed`・`not_attempted`）、`last_validation_status`（`passed`・`failed`・`not_run`）、`delivery_status`（`on_time`・`delayed`・`unknown`） | データセルの状態と提供元別の運用状態を分ける。検証結果は直近の取得試行に対応付ける。提供予定が確かめられた範囲で遅延を判定し、取得失敗や検証失敗で旧版の値を書き換えない |

## GitHub Pages 向け公開 JSON 案

公開ファイルは専用ビルド成果物に配置する。観測の期間終了日（JST）の年月で履歴を分け、月をまたぐ週・シーズン累計は終了月のファイル1件に格納する。粒度・地域・年月・疾患・データセットで絞り込める。ファイル名に使う ID は固定した ASCII の安全な形式とし、内部の地域コード表などで対応を管理する。

- `data/manifest.json` は現在公開する配布版の入口。配布版 ID・生成時刻、データセットごとの出典・対象地域・鮮度、各 JSON の相対パス、サイズと SHA-256 を管理する。地図を配布する場合は行政区域の版と基準日も参照する。
- `data/releases/<release_id>/latest/<dataset_id>/<region_kind>/<region_id>/<disease_id>.json` は該当する観測のうち、公開条件と品質判定を通過した各系列の最新値を格納する。提供元が異なる系列の対象期間は揃うとは限らないため、行ごとに表示する。
- `data/releases/<release_id>/history/<dataset_id>/<region_kind>/<region_id>/<YYYY-MM>/<disease_id>.json` は同じ条件を満たした各観測の選定版を格納する。公開中の履歴にも原本版と期間を付ける。訂正前の原本や内部の版履歴の保存期間・提供可否は R-16 で判断する。
- manifest のパスは manifest のある `data/` を基準に解決し、GitHub Pages のプロジェクト名を含む base path に対応する。ビルドでファイルの存在・サイズ・ハッシュと参照整合性を確認してから一括公開し、失敗した場合は前回の公開版を維持する。
- 公開 JSON は許可した項目から組み立てる。公開対象外の観測、内部ログ、未許諾の原文・資料、認証情報は除外する。閲覧側は公開済みの JSON を読み込む。Web ページ側で提供元の API 等を呼び出す必要はない。

manifest の架空例。パスとサイズ・ハッシュは構成を示すための例示値。

```json
{
  "schema_version": "0.1-draft",
  "release_id": "sample-20300122-01",
  "generated_at": "2030-01-22T09:00:00+09:00",
  "sources": {
    "sample-sentinel": {
      "attribution": "架空の提供元・週次定点集計",
      "source_url": "https://example.invalid/reports",
      "coverage": [{"region_kind": "prefecture", "region_id": "sample-a"}],
      "latest_period_end": "2030-01-13",
      "source_updated_on": "2030-01-16",
      "last_attempted_at": "2030-01-22T08:50:00+09:00",
      "last_attempt_status": "failed",
      "last_validation_status": "not_run",
      "last_fetch_succeeded_at": "2030-01-21T08:50:00+09:00",
      "published_version_fetched_at": "2030-01-20T08:50:00+09:00",
      "delivery_status": "unknown"
    }
  },
  "files": [
    {
      "kind": "history",
      "dataset_id": "sample-sentinel",
      "region_kind": "prefecture",
      "region_id": "sample-a",
      "year_month": "2030-01",
      "disease_id": "influenza",
      "path": "releases/sample-20300122-01/history/sample-sentinel/prefecture/sample-a/2030-01/influenza.json",
      "bytes": 1234,
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ]
}
```

最新・履歴ファイルは、配布版と観測行を持つ。行には提供元の版・期間・値の状態・分母を添える。以下は上記の履歴ファイルに対応する例。

```json
{
  "schema_version": "0.1-draft",
  "release_id": "sample-20300122-01",
  "observations": [
    {
      "dataset_id": "sample-sentinel",
      "region_kind": "prefecture",
      "region_id": "sample-a",
      "disease_id": "influenza",
      "coverage_id": "sample-sentinel-sites",
      "facility_group": "all_in_scope",
      "period_kind": "weekly",
      "period_start": "2030-01-07",
      "period_end": "2030-01-13",
      "metric_id": "sentinel_reports_per_site",
      "unit": "case_per_sentinel",
      "value": "0.50",
      "value_status": "reported",
      "denominator": null,
      "denominator_status": "not_provided",
      "version_id": "sentinel-b",
      "edition_kind": "provisional"
    }
  ]
}
```
