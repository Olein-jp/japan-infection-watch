# 調査ロードマップ

GitHub のマイルストーン [調査・実現可能性評価（R-01〜R-19）（#1）](https://github.com/Olein-jp/japan-infection-watch/milestone/1) に R-01〜R-19 を集約する。
設計・開発・公開・運用は承認後に別マイルストーンで管理する。後続 Issue の ID は D-001（設計）、F-001（機能）、T-001（テスト）、I-001（基盤）、O-001（運用）、B-001（不具合）を使用する。

着手順は依存関係を優先する。優先度は P0 が日本学校保健会・Tableau、P1 が他の情報源・品質・運用、P2 が最終評価・開発仕様案。取得不可でも理由・代替案を記録すれば後続で評価できる。依存関係の変更時は根拠を本書に残す。

| 調査 ID | GitHub Issue | タイトル | 優先度 | 依存 Issue | 成果物 |
|---|---|---|---|---|---|
| R-01 | [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) | 日本学校保健会の公開ビュー・公式資料を棚卸しする | P0 | なし | [公開ビューと公式資料の棚卸し](findings/R-01-public-views.md) |
| R-02 | [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) | Tableau・日本学校保健会の利用条件と自動取得条件を調査する | P0 | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) | [公開ビューと学校検索 API の利用条件](findings/R-02-reuse-terms.md) |
| R-03 | [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) | Tableau Embedding API v3で公開ビューを表示するPoC | P0 | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1)、R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) | [埋め込み検証結果](findings/R-03-tableau-embedding.md)、[表示 PoC](../poc/tableau/README.md) |
| R-04 | [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | Tableauの集計データ取得・CSV出力を検証する | P0 | R-03 [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) | [集計と CSV の検証結果](findings/R-04-tableau-summary.md)、[再現手順](../poc/tableau/README.md#r-04-公式サンプルの集計と-csv-出力) |
| R-05 | [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5) | 市区町村別の感染症・閉鎖データの構造を特定する | P0 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | `docs/findings/R-05-municipal-schema.md`、`docs/schemas/` |
| R-06 | [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6) | 学校別・学校種別・閉鎖種別の取得可否を検証する | P0 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | `docs/findings/R-06-school-closure-granularity.md` |
| R-07 | [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7) | 過去データの取得可能期間と日付フィルターを検証する | P0 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | `docs/findings/R-07-history-range.md` |
| R-08 | [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8) | 日本学校保健会の学校情報等検索REST APIを検証する | P0 | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) | `docs/findings/R-08-school-search-api.md`、`poc/school-api/` |
| R-09 | [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9) | JIHSの感染症発生動向CSVを取得・正規化するPoC | P1 | なし | [CSV 検証結果](findings/R-09-jihs-csv.md)、[正規化 PoC](../poc/jihs/README.md) |
| R-10 | [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10) | 厚労省の学校欠席者数PDFを構造化するPoC | P1 | なし | [PDF 抽出結果](findings/R-10-mhlw-absence-pdf.md)、[構造化 PoC](../poc/mhlw/README.md) |
| R-11 | [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | 岐阜県・岐阜市をモデルに地域別感染症データを調査する | P1 | なし | [地域・形式の調査結果](findings/R-11-gifu-region.md)、[PDF・Excel 照合 PoC](../poc/local-government/README.md) |
| R-12 | [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12) | 47都道府県の感染症情報源と地域粒度を棚卸しする | P1 | R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | [都道府県別一覧と確認方法](findings/R-12-prefecture-inventory.md) |
| R-13 | [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13) | 自治体・教育委員会の閉鎖情報とオープンデータを調査する | P1 | R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | [自治体別比較と全国展開の条件](findings/R-13-local-closures.md) |
| R-14 | [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) | 自治体・学校・地理マスターデータの照合を検証する | P1 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-08 [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8)、R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | [自治体・地理の照合](findings/R-14-master-joins.md)、[地域照合の項目案](schemas/region-crosswalk.md) |
| R-15 | [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) | 共通データモデルと品質管理ルールを設計する | P1 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-09 [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9)、R-10 [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10)、R-14 [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) | [調査と品質検証](findings/R-15-data-model.md)、[共通モデル・公開 JSON 案](schemas/observations.md) |
| R-16 | [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) | 定期取得・保存・再公開の運用可能性を検証する | P1 | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2)、R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-09 [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9)、R-10 [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) | [資料別の運用検証](findings/R-16-collection-operations.md)、[取得・公開と復旧の手順案](operations/collection-and-recovery.md) |
| R-17 | [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) | デプロイ・運用構成と費用を比較する | P1 | R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) | [構成比較・計測・費用](findings/R-17-pages-architecture.md)、[公開と保管の構成案](architecture/pages-layout.md)、[ローカル PoC](../poc/pages/README.md) |
| R-18 | [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) | サービスの実現可能性・対象範囲を評価する | P2 | R-12 [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12)、R-13 [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15)、R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16)、R-17 [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) | [対象範囲・費用・Go／No-Go](findings/R-18-feasibility.md)、[実現可能性評価](final-report/README.md) |
| R-19 | [#19](https://github.com/Olein-jp/japan-infection-watch/issues/19) | 検証結果から本開発用仕様書を作成する | P2 | R-18 [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) | [開発判断と根拠](findings/R-19-mvp-specification.md)、[仕様・公開・運用・開発 Issue 案](specifications/README.md) |

## 設計・開発のイシュー

[初期版の設計・開発（#2）](https://github.com/Olein-jp/japan-infection-watch/milestone/2)。2026-11-24（JST）に開発を承認。調査の R-19 を根拠とする。

| Issue | 作業 | 依存 | 根拠・成果物 |
|---|---|---|---|
| [D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20)（完了） | 開発範囲と入力条件 | [R-19 #19](https://github.com/Olein-jp/japan-infection-watch/issues/19)（完了） | [条件の記録](specifications/mvp-inputs.md) |
| [F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21)（完了） | 週次集計の正規化 | [D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20) | [実装と検証結果](findings/F-001-jihs-normalization.md)・[共通モデル](schemas/observations.md) |
| [F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22)（完了） | 地域・疾患ページと分割 JSON | [F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21) | [実装・検証](findings/F-002-static-preview.md)・[画面仕様](specifications/mvp.md#画面と静的-url) |
| [I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23)（完了） | Actions 検証と配布準備 | [F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21)・[F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22) | [実装・検証](findings/I-001-preview-check.md)・[公開アーキテクチャ](architecture/mvp-publication.md) |
| [T-001 #24](https://github.com/Olein-jp/japan-infection-watch/issues/24) | 静的配信・アクセシビリティ・復旧の検証 | [F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22)・[I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23) | [公開前テスト](operations/mvp-release.md#公開前テストと監査) |
| [O-001 #25](https://github.com/Olein-jp/japan-infection-watch/issues/25) | 初回公開・手動更新の判定 | [D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20)・[I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23)・[T-001 #24](https://github.com/Olein-jp/japan-infection-watch/issues/24) | [運用と公開判定](operations/mvp-release.md) |

## GitHub Pages に関する調査の分担

- R-15 は来歴と欠損を保つモデル、品質検査、公開データの分割と manifest を設計する。
- R-16 は取得・保存・再公開の条件、提供元別の鮮度、訂正、旧版保持と復旧を検証する。
- R-17 は架空データの静的ビルド、base path、JSON、直リンク、容量・時間、旧版保持を試験し、Pages/Actions の条件・費用・定期実行・権限を比較する。
- R-18 は根拠と制約をまとめ、対象範囲・代替案・Go/No-Go を評価する。
- R-19 は同一リポジトリでの開発仕様案、静的サイト・データ配信と更新・復旧・公開前監査・運用費用、開発 Issue 案を用意する。

GitHub Actions は取得、正規化、品質検証、公開可否判定、静的生成を担う構想。GitHub Pages には公開専用成果物を渡す。検証対象と承認の節目は[プロジェクト範囲](project-scope.md)を参照する。

## 依存関係の変更履歴

2026-11-24 に初期指示書記載の33件を登録。
