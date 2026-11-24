# 進捗

更新日 2026-11-25（JST）

現在は設計・開発段階。2026-11-24（JST）に R-19 の仕様案での開発を承認された。[初期版の設計・開発（#2）](https://github.com/Olein-jp/japan-infection-watch/milestone/2) に開発 Issue 6件を登録。採用技術は Python による取得・正規化・静的生成と静的 HTML・CSS・JavaScript、GitHub Actions の標準 Linux runner、GitHub Pages。初期開発は架空の JIHS 週次定点集計を対象とし、実データの第一候補は全国・都道府県の JIHS IDWR 週次定点速報 CSV。[開発範囲と入力条件](specifications/mvp-inputs.md)

[調査・実現可能性評価（R-01〜R-19）（#1）](https://github.com/Olein-jp/japan-infection-watch/milestone/1) に調査 Issue 19件を登録済み。R-01 で日本学校保健会の公式案内を棚卸しし、[調査結果](findings/R-01-public-views.md)を記録した。R-02 で公開ビューの[利用条件](findings/R-02-reuse-terms.md)を調査し、R-03 で[ローカルの埋め込み表示](findings/R-03-tableau-embedding.md)を確認し、R-04 で[公式サンプルの集計と CSV ファイル](findings/R-04-tableau-summary.md)を検証した。

## 開発の進捗

- [D-001 #20](https://github.com/Olein-jp/japan-infection-watch/issues/20) の開発範囲・採用技術・入力条件を記録し、2026-11-25（JST）に完了。
- [F-001 #21](https://github.com/Olein-jp/japan-infection-watch/issues/21) は架空の週次定点 CSV の正規化を実装・検証し、2026-11-25（JST）に完了。[検証結果と使い方](findings/F-001-jihs-normalization.md)・[開発ロードマップ](issue-roadmap.md#設計開発のイシュー)
- [F-002 #22](https://github.com/Olein-jp/japan-infection-watch/issues/22) は架空観測の静的ページと分割 JSON を実装・検証し、2026-11-25（JST）に完了。[検証結果と表示手順](findings/F-002-static-preview.md)
- [I-001 #23](https://github.com/Olein-jp/japan-infection-watch/issues/23) は Actions の検証ワークフローと配布前判定を実装し、ローカル検証を経て2026-11-25（JST）に完了。[検証結果と再現手順](findings/I-001-preview-check.md)

## 調査の着手候補

R-04 の公式サンプルで確認できた動作は記録済み。日本学校保健会のデータが必要な R-05〜R-07 は、R-02 の条件確認まで公式資料と画面で確認できる範囲に限る。R-02 の完了承認後は学校検索 API の R-08 [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8) も候補。2026-11-24（JST）に R-01・R-03・R-04・R-09・R-10・R-11・R-12・R-13・R-15・R-17・R-18・R-19 を完了として閉じた。

## イシュー別の状態

| 調査 ID | GitHub Issue | 状態 | 未確認の主な事項 | 着手前に確認する依存 Issue |
|---|---|---|---|---|
| R-01 | [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) | 完了 | 一部のリンク名と疾患指定の食い違い、個別ビューの初期表示、日・地域別の報告範囲 | なし |
| R-02 | [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) | 回答待ち | 日本学校保健会側の回答待ち。適用規約、集計の取得・保存・再配布・商用利用の条件 | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) |
| R-03 | [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) | 完了 | 別ビューの埋め込み可否、日付コントロールの操作範囲 | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1)、R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) |
| R-04 | [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | 完了 | 日本学校保健会の集計取得可否 | R-03 [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) |
| R-05 | [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5) | 未着手 | 市区町村別のキー・分母・粒度 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-06 | [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6) | 未着手 | 学校コード・学校種別・閉鎖種別 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-07 | [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7) | 未着手 | 取得可能な最古・最新と期間 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-08 | [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8) | 未着手 | 学校検索 API の認証・応答・キャッシュ | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) |
| R-09 | [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9) | 完了 | 第46週の週報との照合、訂正時の版管理と継続利用条件 | なし |
| R-10 | [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10) | 完了 | 異なる年度・画像表の書式、継続利用条件 | なし |
| R-11 | [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | 完了 | 他市町村の値、過去の管轄変更、個別の再利用条件 | なし |
| R-12 | [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12) | 完了 | 未確認の地域粒度・資料別の利用条件は R-14・R-16 に引き継ぎ | なし |
| R-13 | [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13) | 完了 | 岐阜市別の現行資料、神戸市システムの出力条件、現行資料の継続利用は保留 | なし |
| R-14 | [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) | 自治体・地理の検証済み。学校側の照合待ち | 学校コード、学校別データ、市区町村キー・API 応答との照合 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-08 [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8) |
| R-15 | [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) | 完了 | 学校保健会データの指標・対象・期間・分母、公開条件 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-14 [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) の学校側 |
| R-16 | [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) | JIHS・厚労省の少量再取得を検証済み。運用案を作成 | 学校保健会の条件、許容される定期取得、保管先・復旧の構成 | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) の未確定範囲 |
| R-17 | [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) | 完了 | 実データの公開条件、GitHub 上の時間・費用・復旧 | R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) の実運用条件 |
| R-18 | [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) | 完了 | 資料別の加工・再配布と取得条件、実運用の容量・課金、開発・公開承認 | R-12 [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12)、R-13 [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15)、R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16)、R-17 [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) |
| R-19 | [#19](https://github.com/Olein-jp/japan-infection-watch/issues/19) | 完了 | 資料別の公開・定期取得条件、復旧と月0円の実運用 | R-18 [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) |

## R-01 で判明した事項

- 公式案内に Tableau Public へのリンク98件。市区町村別のインフルエンザ閉鎖地図1件を閲覧し、対象日・元データ時点・フィルターを確認。
- 2024-03-25 の変更で、学年閉鎖と休校のクラスも閉鎖クラス数に合算する仕様を確認。
- 参加範囲の公式資料は年度単位。全国総施設を分母とする2025年度利用率は小学校55.7%、中学校52.4%、高校55.8%。日・地域・疾患単位の報告率は未確認。

## R-02 で判明した事項

- 対象ビューは通常閲覧と公式共有が可能。代表ビューのデータ出力メニューに CSV・クロス集計・データ・ワークブックは表示されず、集計の読取 API は実行していない。
- R-03 の手動ローカル表示は1ビューに限定する。取得、定期実行、保存、加工、再配布の扱いは適用規約と公開者の条件を確認するまで保留。
- 2026-11-24（JST）に依頼者が日本学校保健会側の窓口へ問い合わせを送信。現在は回答待ち。回答が届いたら取得経路と利用条件を [R-02 の調査記録](findings/R-02-reuse-terms.md#問い合わせ案)に反映する。
- 学校検索 API は別規約。R-08 で少数 GET の利用条件、更新義務、掲載停止、キャッシュと保存の扱いを確認する。

## R-03 で判明した事項

- 代表ビュー1件で Embedding API v3 の描画と FirstInteractive を確認。公開シート2件、ダッシュボードのフィルター名4件を記録。
- 日付は画面のページコントロールにあり、ダッシュボードのフィルター返却一覧には含まれなかった。集計行は未取得。

## R-04 で判明した事項

- 公式サンプルで集計総行数7・4ページ、先頭2行と2列の型を確認。画面上の2指標と一致した。
- 公式サンプルの CSV 実ファイルを照合し、数量と平均割引率が集計 API・画面と一致した。日本学校保健会の集計取得は R-02 の条件確認待ち。

## R-09 で判明した事項

- JIHS 公式速報 CSV 2週分で、全国と47都道府県の19疾患を正規化した。第45週は週報 PDF の全1,824セルと一致した。[調査結果と再現手順](findings/R-09-jihs-csv.md)
- 速報の区分・出典・版と、定点当たり報告数の表示精度・ハイフンを保持する。定期取得、訂正版の扱いと公開条件は R-15/R-16 へ引き継ぐ。

## R-10 で判明した事項

- 厚労省の第10・11報から都道府県47行・別掲政令市20行・全国計と、全国の当週施設種別を構造化した。地域の合算と施設種別の和は掲載計と一致した。[調査結果と再現手順](findings/R-10-mhlw-absence-pdf.md)
- 学級閉鎖は学校数。累計には過去分の修正が入る。これらの指標・版と地域区分を R-15 に、書式変更や継続利用の条件を R-16 に引き継ぐ。

## R-11 で判明した事項

- 県の週報・Excel から県計と8保健所の定点報告を確認。インフルエンザの第44〜46週で定点当たり報告数27セルが一致した。[調査結果と再現手順](findings/R-11-gifu-region.md)
- 岐阜市保健所は岐阜市のみ、県の岐阜保健所は周辺8市町。医療圏は別区分。市統計書の感染症届出数は年度単位。地域・指標・形式の確認方法を R-12〜R-14、継続利用条件を R-16 に引き継ぐ。

## R-12 で判明した事項

- 47都道府県の公式入口を特定。主に2026年第46週の公表資料で、保健所・医療圏・地区・市の別掲、形式、更新周期、利用条件を確認した。[都道府県別一覧と確認方法](findings/R-12-prefecture-inventory.md)
- 神奈川はインフルエンザの市・保健所等の定点率を CSV で配布。富山・兵庫の確認 CSV は県集計。各集計単位と自治体の対応を R-14 に、資料ごとの利用条件を R-16 に引き継ぐ。

## R-13 で判明した事項

- 岐阜市、神戸市、北九州市、東京都、八王子市の公表資料を比較。北九州市の現行週報は週・施設単位で重複調整し、2017/18〜2019/20年の閉鎖データは別途 CSV・XLSX で公開されている。岐阜県が案内する学校情報は停止中。[調査結果と全国展開の条件](findings/R-13-local-closures.md)
- 全国の共通集計を基準に、定義と利用条件が確認できた自治体を追加する方針を整理した。指標・欠測は R-15、継続利用の判断は R-16 に引き継ぐ。

## R-14 で判明した事項

- 岐阜市保健所と県の岐阜保健所が所管する9市町を、団体コードと2026年1月1日版の行政区域に照合。岐阜市の境界は GeoJSON に変換し、同梱の図形と一致を確認した。[照合結果と変換手順](findings/R-14-master-joins.md)
- 旧柳津町の編入と浜松市の区再編から、コードと地域種別に適用時点を添えて管理する方針を整理。学校側の検証は R-05・R-06・R-08 の結果待ち。[地域照合の項目案](schemas/region-crosswalk.md)

## R-15 で判明した事項

- JIHS の報告件数・定点当たりと厚労省の学校休業関連集計を別指標としてモデル化した。版・欠損・重複・訂正・原表照合・集計の品質ルールは架空データの15件で検証した。[調査結果と検証手順](findings/R-15-data-model.md)
- 公開用 JSON の地域・終了年月・疾患別の分割、latest と履歴、出典・鮮度を示す manifest を設計案に記録。資料ごとの公開可否は R-16、配布・運用構成は R-17 に引き継ぐ。[共通モデルと公開 JSON 案](schemas/observations.md)

## R-16 で判明した事項

- JIHS の第46週定点 CSV と厚労省の第11報 PDF を少量再取得し、以前と同じハッシュを確認した。条件付き取得は JIHS が304、厚労省は同一内容で200。定期取得の許容条件は未確認。[資料別の運用検証](findings/R-16-collection-operations.md)
- 訂正と同一版の判定、失敗時の公開成功版の保持、部分更新、復旧、保持・削除案を整理。Pages 上での一式の公開・復旧とストレージ構成は R-17 で検証する。[取得・公開と復旧の手順案](operations/collection-and-recovery.md)

## R-17 で判明した事項

- 架空データでプロジェクトパスとルート配置、地域ページ直リンク・再読込、404、分割 JSON、更新予定超過と欠損の表示、失敗時の公開成功版の維持をローカル確認。[構成比較と計測](findings/R-17-pages-architecture.md)
- 都道府県週次の1年分を初期候補とする。全市区町村の日次1年分は現行行形式で約3.65 GBの試算で、配布期間・形式・保管構成を R-18 で評価する。[容量・時間・費用の試算](findings/R-17-pages-architecture.md#容量時間費用の試算)

## R-18 で判明した事項

- 月0円の初期版は JIHS の全国・都道府県の週次定点集計が第一候補。厚労省の学校休業は追加候補で、市区町村の全国一律表示と学校別表示は見送る。[地域粒度と提供可否](findings/R-18-feasibility.md#地域粒度と提供可否)
- 仕様検討は条件付き Go、実データ公開・定期取得は現時点で No-Go の案。資料別の利用条件と運用費を確認し、R-19 の仕様案をもとに開発承認を受ける。[実現可能性評価](final-report/README.md)

## R-19 で判明した事項

- JIHS の週次定点集計を第一候補とする画面・静的配信、月0円の公開判定・更新・復旧、開発 Issue 案6件を作成。2026-11-24（JST）に依頼者が開発を承認。実データ公開と定期取得は別途承認を得る。[仕様案と根拠](findings/R-19-mvp-specification.md)

## 初期構築で確認した事項

- ローカルは初回コミット前の `main`。GitHub 側の既定ブランチ名は `main` で、ブランチの実体は初回 push 後に作られる。
- GitHub は Public、Issues 有効、Pages 無効。Issue フォームはローカルに配置済みで、GitHub のフォーム選択画面への反映には既定ブランチへの反映が必要。
- 初期構築時に一次情報台帳へ31件の候補を登録。情報源、利用条件、対象範囲、設計・費用の調査は各 Issue で行う。
