# R-18　サービスの実現可能性と公開範囲

対象は [Issue #18](https://github.com/Olein-jp/japan-infection-watch/issues/18)。確認日 2026-11-24（JST）。既存の実行結果を突き合わせ、一次情報の掲載案内と規約を再確認した。容量計測と品質テストは架空データで再実行した。新規の実データ一括取得、提供元への照会、開発、公開はこの評価の対象外。判断の要約は[実現可能性報告](../final-report/README.md)を参照。

## 地域粒度と提供可否

| 提供範囲 | 取得・品質の根拠 | 利用条件・不足範囲 | 初期版での扱い |
|---|---|---|---|
| 全国・47都道府県の感染症発生動向 | JIHS の週次定点速報 CSV。2026年第45・46週の配布を確認し、第45週は19疾患×48地域×2指標の1,824セルを週報と照合。全国値は公式の掲載値を使う。[速報一覧](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/index.html)・[R-09](R-09-jihs-csv.md) | 2週の検証で全48地域の行を確認。疾患・地域により原表にハイフンがあり、通年の取得・連続性は未検証。規約の出典・加工表示、第三者権利、第7項の改変・転載条件を対象 CSV と変換後の配布に適用できるか確認。定期取得の許容範囲も未確認。[JIHS 規約](https://id-info.jihs.go.jp/usage-contract.html)・[R-16](R-16-collection-operations.md#利用条件の判断) | **集計表示の第一候補**。条件が明確になった疾患・週から開始し、未確認の期間は公表元への案内を候補とする。 |
| 全国・都道府県の報告区分と別掲政令市の学校休業 | 厚労省 PDF 第10・11報 p.4 は47都道府県区分、20別掲市、掲載全国計。p.5 は全国の当週施設種別。両報で地域表の各952セルと掲載計を確認。[第11報 pp.4–5](https://www.mhlw.go.jp/content/001770872.pdf#page=4)・[R-10](R-10-mhlw-absence-pdf.md) | 市町村全体を網羅する市別表と地域×施設種別の内訳は確認できていない。別掲市を含む範囲の解釈には原表の区分を使う。対象表の数値利用・出典・加工表示・個別条件・取得頻度を確認する。[厚労省規約](https://www.mhlw.go.jp/chosakuken/index.html)・[R-16](R-16-collection-operations.md#利用条件の判断) | **追加候補**。週次定点とは別の系列で、当週・累計・版を区別する。公開条件が未確定の間は公式発表の案内を候補とする。 |
| 市区町村・行政区・保健所管内の感染症発生動向 | 47都道府県の公式入口を確認。神奈川県に別掲政令市の定点率、岐阜県に8保健所の表があり、岐阜市保健所管内は岐阜市と一致。県岐阜保健所の値は周辺8市町を合わせた管内値。[R-11](R-11-gifu-region.md)・[R-12 全47件](R-12-prefecture-inventory.md#都道府県別一覧)・[R-14](R-14-master-joins.md) | 全市区町村の統一データと取得率は未確認。例えば青森市を含む合同管内や、確認した富山県・兵庫県の県集計 CSV から、市町村固有の値は得られない。別掲の範囲、時点別の境界、定点種別、指標、更新・訂正、資料ごとの利用条件を照合する。 | **自治体・管内の数値は後続候補**。初期は県の集計と利用条件を確認した公式リンクを案内できる。管内の値は管内単位で扱う。 |
| 市区町村の学校休業 | 岐阜市の現行市別値は未確認。神戸市・八王子市に市立等の発表、北九州市に週次施設数と現行と別経路の過去カタログ。東京都の確認資料は都全体。厚労省の20別掲市は原資料にある系列として扱える。[R-13 自治体別比較](R-13-local-closures.md)・[北九州市の現行案内](https://www.city.kitakyushu.lg.jp/contents/334_00031.html) | 公表対象校、指標、期間、提供経路、再配布条件が異なる。岐阜県の学校情報は停止案内。北九州市の2017/18〜2019/20年のカタログを現行週報の利用根拠に使わない。無発表日の意味は資料ごとに確認する。 | **全国一律の市区町村別表示は見送り**。資料を確認した地域の公式案内を候補とし、集計の追加は定義と許諾が揃った地域から評価する。 |
| 学校別・日本学校保健会の市区町村と学校集計 | 公式マップ案内と代表ビューの閲覧は確認済み。2024-03-25 の変更では学年閉鎖・休校に伴うクラスも閉鎖クラス数に計上。学校検索 API と疾病・閉鎖集計は別経路。[公式マップ案内](https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping)・[R-01](R-01-public-views.md)・[R-02](R-02-reuse-terms.md) | #2 の回答待ち。取得、加工、保存、再配布、期間、分母・参加範囲、学校コード照合、少数集計の推知対策が未確認。参加施設の年度割合から地域・週の報告率を推定しない。 | **初期版の学校別表示は見送り**。利用条件に合う公式案内を候補とする。#2 の回答を受けて #5〜#8 と #14 の学校側を評価する。 |

## 初期版の表示・更新案

- 全国・県の一覧、都道府県別の直接アクセスできるページ、疾患別の週次推移、公式出典と鮮度を候補とする。表示する疾患は、定点区分と継続性を確認できたものから選ぶ。履歴は取得と保持が確認できた公開済みの週から始め、直近1年を上限候補とする。初回から1年分が揃うことは公開条件に含めない。地図の配布条件や表示容量が未確定なら、地域一覧と表で開始できる。[R-15](R-15-data-model.md)・[R-17](R-17-pages-architecture.md)
- 報告件数と定点当たり報告数を区別し、定点数の逆算や率の合算は行わない。学校休業は施設数、学校数、閉鎖クラス数、当週・累計を出典どおりに区別する。明示ゼロ、原表のハイフン・空欄、未報告、秘匿、対象外、取得失敗、更新遅延を保持する。原表で意味が分からない記号は理由未確認のままとする。地図を追加する場合は欠損を凡例・表・テキストで示す。[共通モデル](../schemas/observations.md)
- 取得・公開の条件が揃った資料は発行周期に合わせて週次更新を候補とする。当面の運用案は公式公表を担当者が確認し、許容された取得を手動で実施する方式。自動取得は頻度・再取得・訂正時の扱いを確認し、別途承認を得てから有効にする。更新失敗や容量超過では最後の公開成功版を維持し、対象週・出典更新日・最終取得成功時刻・生成時刻・更新遅延を表示する。利用者登録や追跡を必要としない。[取得と復旧の運用案](../operations/collection-and-recovery.md)

## 月0円での成立条件

公開リポジトリの GitHub Free・GitHub Pages（標準アドレス）・標準 Linux runner を使う。公開物は HTML、CSS、JS、公開可能な JSON 等の一式に絞る。Pages は無料の公共情報閲覧を想定する。同サービスが制限するオンライン事業・商取引・商用 SaaS への利用と、リポジトリとサイトの公開範囲は別途判断する。[Pages の用途と上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)・[Pages 利用条件](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#pages)・[Actions の課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

| 項目 | 評価と運用の判断 |
|---|---|
| 公開サイズ | 47都道府県×19疾患×2指標の架空の週次1年分は、JSON 45.45 MB＋索引4.03 MB、計49.48 MB（JSON 11,609ファイル）。実際の HTML・全国系列・地図・その他の配布物を含めて管理目安500 MB、公式上限1 GBで評価する。1,741市区町村の日次1年分は約3.65 GB、索引を含め約3.70 GBの推計。今回の構成で全市区町村日次1年分は見送る。 |
| 配信と実行 | 管理目安は帯域50 GB/月、デプロイ5分。公式は帯域100 GB/月のソフト上限、デプロイ10分でタイムアウト。試算例は初回400 KB×10万回で40 GB/月。実際の閲覧数・履歴や地図の追加通信・GitHub 上の実行時間は未計測。利用可能な実績または配信量の推計で確認する。 |
| 保管・作業量 | 標準 runner は公開リポジトリで無料。公開用 artifact は原則1日で、GitHub Free の500 MB枠を Packages と共有する。100 MB×月12回×1日÷30日なら月平均40 MB相当（他の利用を除く仮定）。課金前の停止手段・実利用・容量は公開準備時に確認する。復旧版の保持先と期限は利用条件の範囲内で決める。担当者が週次で差分・訂正・失敗を確認する時間は未計測。無償で確保できる作業量で回らない場合は対象を絞る。 |
| 代替 | 容量や帯域に余裕がなくなれば、履歴期間・疾患・地域を絞り、公式リンクを残す。GitHub Pages を使えない場合は Cloudflare Pages の静的配信を候補にする。無料枠は2万ファイル・1ファイル25 MiBで、Wrangler の Direct Upload で検証済み成果物を渡す方式を文書確認した。日次フル履歴の約13.6万ファイルはこの無料枠にも収まらない。全成果物のファイル数・最大サイズ・公開条件・運用費を再評価し、承認を得てから切り替える。 |

根拠は [R-17 の計測・費用試算](R-17-pages-architecture.md#容量時間費用の試算)、[無料枠での運用設計](../architecture/pages-layout.md#無料枠での運用設計)、[Cloudflare Pages の上限](https://developers.cloudflare.com/pages/platform/limits/#files)、[Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)。本番の料金や容量を観測した結果はまだない。

## Go／No-Go 案と段階計画

1. **R-19 の仕様検討は条件付き Go 案。** 都道府県の週次集計を基本に、資料ごとの利用可否で切り替えられる仕様を作る。学校休業の補足と自治体拡張は別の採用判断にする。公開の根拠が揃わない資料は、リンク条件を確認したうえで公式案内を代替にする。
2. **開発着手は依頼者の判断待ち。** R-19 の仕様案をもとに、指標と対象範囲、運用担当、月0円での継続条件を説明して Go/No-Go を求める。
3. **実データ公開・定期取得は現時点で No-Go。** 採用資料ごとに加工・再公開・保持・表示と取得の条件を確定し、出典と原表の一致、更新失敗時の復旧、公開一式の容量と課金停止の条件を確認する。履歴・Issue・ログ・公開成果物の監査と依頼者の公開承認が揃ってから公開に進む。定期取得の有効化は許容頻度と再試行条件の確認後に判断する。
4. **市区町村の拡張は地域ごとに判断。** 公表単位・対象施設・指標・欠損・更新周期・利用条件を確認し、条件が揃った自治体だけを追加評価する。学校別は #2 の回答後、対応キーと少数集計の再識別防止まで確認できた場合に再評価する。

## 根拠の確認と再現

| 一次情報 | 2026-11-24 に照合した範囲 |
|---|---|
| [S15 JIHS IDWR](https://id-info.jihs.go.jp/surveillance/idwr/)・[2026年速報一覧](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/index.html)・[S53 利用規約](https://id-info.jihs.go.jp/usage-contract.html) | 週報・速報への導線、第45・46週の掲載、規約冒頭と第1・2・6・7・8項。規約の制定日は2014-08-25。 |
| [S16 厚労省 ARI 総合対策](https://www.mhlw.go.jp/stf/index2026.html)・[S60 利用規約](https://www.mhlw.go.jp/chosakuken/index.html) | 公表資料への導線、利用規約 §1.1・§1.4、リンク案内。表の照合は [R-10](R-10-mhlw-absence-pdf.md) 記録の第10・11報 pp.4–5 を使用。 |
| [S01 学校保健会の公式マップ案内](https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping)・[S24 北九州市現行案内](https://www.city.kitakyushu.lg.jp/contents/334_00031.html) | 2024-03-25 の変更告知と北九州市の2026/27シーズンの公表入口。市町村別の既存照合箇所は [R-12](R-12-prefecture-inventory.md)・[R-13](R-13-local-closures.md) に記録。 |
| [S26 Pages 上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits#usage-limits)・[S30 Actions 課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)・[S31 追加製品利用条件](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#pages) | Pages Usage limits、Actions Included compute usage and storage、追加条件 Pages 節（2026-08-27 発効表示）。 |
| [S97 Cloudflare Pages の上限](https://developers.cloudflare.com/pages/platform/limits/)・[Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) | 上限文書の Files、File size（2026-11-19更新表示）、Direct Upload の Wrangler（2026-04-21更新表示）。 |

リポジトリのルートから実行できる。2026-11-24 に Python 3 で実行し、都道府県の JSON 45,450,772バイト、索引4,034,198バイト、生成等1.71秒を確認。市区町村は12地域の架空データを基に推計し、実地域のファイルは取得していない。品質テスト15件は成功。地域直リンクと旧版保持のブラウザ結果は [R-17 の実測](R-17-pages-architecture.md#架空データによる実測)を参照。

```sh
python3 -B poc/pages/measure.py
python3 -B -m unittest discover -s poc/data-model
```

受入基準に対して、粒度別の可否・不足範囲・代替、月0円と Pages の制約つき Go/No-Go、一次情報の確認日と未確認範囲を記録した。調査結果は完了承認待ち。実運用可否に残る確認は上の段階計画から R-16・R-19 に引き継ぐ。
