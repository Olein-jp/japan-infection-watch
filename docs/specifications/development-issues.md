# 開発 Issue

[初期版仕様](mvp.md)を小さな作業単位に分け、開発承認後に[開発マイルストーン](https://github.com/Olein-jp/japan-infection-watch/milestone/2)へ登録した。公開と定期取得はそれぞれの承認を待つ。

最初に読む箇所は各案の根拠欄に示す。受入条件に必要な直接の依存先だけを追加で確認し、関連テストを優先する。完了報告には変更、関係ファイル、検証結果、残課題を記す。

## [D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20)　開発範囲と公開可能な入力を確定する

前提は開発 Go の記録。最初に [R-18](../findings/R-18-feasibility.md)・[R-16](../findings/R-16-collection-operations.md)と[初期版仕様](mvp.md#提供範囲と情報源)を読む。開発範囲とデータセットの承認条件を整理する。

- [x] 承認日・フェーズ・採用技術・対象データを記録する。
- [x] 資料ごとに取得、加工、保存、再配布、公式案内への切り替え条件を記録する。
- [x] 未許諾資料を使わず架空データで作業できる範囲を示す。

## [F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21)　承認済みの週次集計を正規化する

[D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20) に依存。[R-09](../findings/R-09-jihs-csv.md)・[R-15 共通モデル](../schemas/observations.md)を確認する。架空の JIHS 形式の入力から週次観測を作る。厚労省の追加は別系列の条件が揃った場合に起票する。

- [x] 指標、単位、対象週、地域、原表記号と原本版を保持する。
- [x] 数値ゼロ、ハイフン、空欄、重複、異常な列を関係テストで確認する。
- [x] 許可されない入力や版を公開候補へ渡さない。

[実装と検証結果](../findings/F-001-jihs-normalization.md)

## [F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22)　地域・疾患ページと分割 JSON を生成する

[F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21) に依存。[画面仕様](mvp.md#画面と静的-url)・[R-17 の PoC](../../poc/pages/README.md)を確認する。公式案内への切り替えを含む静的ページ一式を生成する。

- [x] 全国・都道府県・疾患・公式案内を確認した市区町村の静的 URL を生成する。
- [x] 最初に読むファイルを絞り、対象の履歴だけ遅延取得する。
- [x] 出典・鮮度・欠損が表示され、リンク、キーボード、表で主要情報に到達できる。

[実装と検証結果](../findings/F-002-static-preview.md)

## [I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23)　公開前の Actions 検証と配布準備を組む

[F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21)・[F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22) に依存。[ワークフロー仕様](../architecture/mvp-publication.md#github-actions-と-pages)を確認する。架空データで検証・ビルドし、公開承認の条件を運用に渡す。

- [x] 成果物のハッシュ、配布範囲、容量、公開対象の差分が判定できる。
- [x] 未変更、検証失敗、容量超過、古い候補を判定し、架空プレビューは公開対象外とする。
- [x] 検証ジョブを読み取り専用とし、公開に必要な権限と適用先を記録する。実デプロイのジョブは公開承認後に追加する。

[実装と検証結果](../findings/I-001-preview-check.md)

## [T-001 #24](https://github.com/Olein-jp/japan-infection-watch/issues/24)　静的配信、アクセシビリティ、障害復旧を通しで検証する

[F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22)・[I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23) に依存。[公開前テスト](../operations/mvp-release.md#公開前テストと監査)と [R-17 の検証手順](../../poc/pages/README.md)を読む。

- [ ] プロジェクトパスとルートで直リンク、再読込、404、遅延取得が成功する。
- [ ] 狭幅とキーボードで操作でき、色を使わず欠損や状態を判別できる。
- [ ] 破損候補や更新失敗が旧版を上書きせず、保管した版で復旧を再現できる。

## [O-001 #25](https://github.com/Olein-jp/japan-infection-watch/issues/25)　初回公開と手動更新の運用を判定する

[D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20)・[I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23)・[T-001 #24](https://github.com/Olein-jp/japan-infection-watch/issues/24) に依存。[公開判定案](../operations/mvp-release.md)を確認する。承認前は監査・復旧確認・費用見積もりまで行い、依頼者の公開承認後に対象と設定を確認して初回公開を実施する。

- [ ] データ利用条件と公開対象、月0円のアカウント条件・共有枠、公開前監査を記録する。
- [ ] 担当者が手動更新・停止・復旧の判断と手順を再現できる。
- [ ] 承認を得た公開では、公開 URL、版、代表ページと JSON を照合する。

提供元別の定期取得、厚労省や自治体の集計追加、地図のデータ配布は、それぞれの利用条件と受入試験が確定した後に別 Issue とする。
