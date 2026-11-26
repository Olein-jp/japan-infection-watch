# O-001　初回公開と手動更新の運用判定

対象は [Issue #25](https://github.com/Olein-jp/japan-infection-watch/issues/25)。2026-11-25（JST）。[入力の利用条件](../specifications/mvp-inputs.md)、[配布前検証](I-001-preview-check.md)、[統合検証](T-001-integrated-preview.md)を根拠に、公開前の監査と運用リハーサルを実施した。

**公式リンクの先行版を公開済み。** 本番配布が許可された数値データ・成果物は未確定。架空プレビューは `publication_allowed: false`。数値版の公開用入口・ワークフロー、復旧担当と本番版の保管先、公開承認は別途確認する。

## 公開範囲

| 候補 | 判定と条件 |
|---|---|
| 全国・都道府県の JIHS 週次集計 | IDWR 速報データを使った独自グラフは、出典と独自の編集・加工を別々に表示する条件で利用可能と確認。採用する各週の個別注記・第三者権利、描画用 JSON の配布条件、公開用成果物と公開承認は確認待ち。定期取得は許容頻度・訂正経路を別途確認する。[JIHS の回答](#jihs-の回答と数値版への反映)・[R-16 の利用条件](R-16-collection-operations.md#利用条件の判断) |
| 公式リンクだけの先行版 | 早期公開を選ぶ場合の候補。JIHS の第6項と岐阜市のリンク案内を確認。情報源を明記して公式ページへ案内し、数値、架空の観測、提供元の原本・画像・埋め込みを含めない。公開専用の成果物を作成して検証し、範囲を承認した後に進める。[公式 IDWR](https://id-info.jihs.go.jp/surveillance/idwr/)・[岐阜市のリンク・著作権](https://www.city.gifu.lg.jp/info/kouhou/1008373/site/1011572.html) |
| 厚労省・学校保健会・自治体別の数値 | 初回公開からは保留。資料の利用条件、対象と粒度を個別に確認する。学校保健会の回答待ちは #2、継続取得と再配布は #16 で扱う。[D-001 資料別の判定](../specifications/mvp-inputs.md#資料別の採用と保留) |

## 公開前監査

2026-11-25（JST）の追加確認。学校保健会の感染症情報マップは公式ポータルのリンク条件に従って案内する。JIHS の公式年別一覧と学校保健会の公式マップへのリンク、6暦月の推移を架空データの静的プレビューに反映した。[学校保健ポータルのリンク条件](https://www.gakkohoken.jp/about)・[JIHS の年別一覧](https://id-info.jihs.go.jp/surveillance/idwr/provisional/sokuhou.html)

JIHS の利用規約は冒頭と第1・2項で出典・加工表示と第三者権利の条件を定め、第7項で個別の転載注記と無断改変を扱う。確認済みの第45・46週の CSV を全期間の確認には使わず、実際に採用する各版の掲載注記・第三者権利を照合し、数値の意味を変更しない抽出・表示と静的 JSON の配布に適用する条件を確定する。学校保健会への問い合わせはこの判断の前提に含まれない。[JIHS の利用規約](https://id-info.jihs.go.jp/usage-contract.html)・[R-16 の資料別判断](R-16-collection-operations.md#利用条件の判断)

| 対象 | 実施内容と結果 |
|---|---|
| Git の履歴 | ローカル `e0d302b` 時点で、到達可能な全 ref の29コミットを Gitleaks 8.30.1 で検査し、認証情報に該当する検出は0件。ファイル名を確認して、原本 CSV・PDF、鍵・`.env` 実ファイル、地図などの生データ形式は検出せず。追跡対象のデータ JSON は架空のテストデータ。著者・コミッターメタデータに GitHub の noreply 形式以外のメールアドレスがある。公開 Git に初回プッシュする前に、連絡先の公開可否を所有者に確認する。既存コミットのアドレスと今後の設定はそれぞれ確認する。[GitHub のコミットメール設定](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) |
| GitHub | 公開リポジトリ。既定ブランチ名の設定は `main` だが、リモートのブランチ実体は0件で Pages は無効。公開 Issue 25件と既存コメント22件を読み取り、認証情報の検出は0件。Pull Request・Actions の実行履歴・artifact は各0件。GitHub-hosted runner での初回検証はコードのプッシュ後に行う。 |
| 成果物 | 架空プレビュー2,857ファイルを生成し、I-001 の範囲・サイズ・SHA-256 検証と Gitleaks 検査を実施した。認証情報の検出は0件。公開不可の状態を確認し、プレビューは配信用領域に出していない。本番用成果物は公開前に改めて監査する。 |

検査は公開前の点検であり、Gitleaks の検出0件だけで履歴全体の公開可否を確定しない。初回プッシュする版、Issue・コメント、初回 CI のログ、公開専用成果物について、対象と判断を更新する。スキャンの報告は認証情報をマスクし、一時ディレクトリに保持した。[Gitleaks の履歴検査仕様](https://github.com/gitleaks/gitleaks)

## 月0円の運用判断

2026-11-25（JST）に直近6か月の週次履歴と GitHub Pages を採用。同じリポジトリの GitHub Actions から検証済みの静的成果物を配布する。6か月分の架空データ一式は7,417ファイル、約22.4 MB で GitHub Pages の公開サイト上限1 GBを下回った。[週次履歴の設計比較](cloudflare-pages-history.md)・[GitHub Pages の上限](https://docs.github.com/ja/pages/getting-started-with-github-pages/github-pages-limits)

- 公開リポジトリの GitHub Pages と標準 Linux runner、標準 `github.io` を使用する。初回公開の候補 URL は `https://olein-jp.github.io/japan-infection-watch/`。リモートの配信 URL と応答は未確認。[GitHub Pages の標準 URL](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)・[Actions の課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- 所有者の課金画面を読み取り、Actions と Packages に超過支出を止める予算設定があることを確認した。個人アカウントのプランに関する公式表と画面上の Actions 保存枠の表示に差がある。上位枠を前提にせず、GitHub Free の共有500 MBを見積もりに使う。アップロード前に共有利用量と停止条件を再確認し、無料の範囲が判定できない場合は保留する。[Actions の共有枠](https://docs.github.com/en/billing/concepts/product-billing/github-actions#included-compute-usage-and-storage)・[予算設定](https://docs.github.com/en/billing/how-tos/set-up-budgets)
- 架空版の展開後は3,357,504バイト。ローカルで作った tar は8,898,560バイト、gzip 圧縮後は222,427バイト。公開上限の基準は展開後のサイズとし、実 artifact のサイズ、保持時間、同時保持数、Packages の既存使用量を別に管理する。試算では約9 MB相当を月12回、各1日保持して月平均約3.6 MB相当。既存使用量を含まず、実測した公開料金・帯域を示すものではない。配信帯域は月50 GBを管理目安、公開用の展開容量は500 MBを管理上限とする。[Pages の上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits#usage-limits)・[無料枠での運用設計](../architecture/pages-layout.md#無料枠での運用設計)

## 手動更新・停止・復旧の確認

1. ローカルでは、架空の入力で生成し、`scripts/check_preview.py` で候補のサイズ・範囲・版・ハッシュを照合した。公開用の入力を用意する段階では、対象号、取得・再配布条件、確認日、原本ハッシュ、変更・訂正理由を先に記録する。
2. [T-001 のブラウザ試験](../../tests/check_web_preview.cjs)を再実行した。破損、容量超過、古い候補、変更なしで配信中の版を維持し、確認済み候補を切り替えた後、保管版を復元して HTTP の manifest・索引・最新 JSON と代表画面を照合できた。元の一式の SHA-256 は `5f7c843f19f88050b451f43642e3ccd370837fd2a578e76a57d2f1433b9714c8`。現行の判定スクリプトは架空版専用で、公開用チェックや GitHub Pages 上の停止・復旧を代替しない。
3. 実運用では、運用担当と承認者、版を選び直す方法、現行と直前の成功版を取り出せる保管先を決める。問題が発生したら後続の更新を止め、現行の配信 URL・版と原因を確認する。撤回対象を除いた公開可能な保管版を再検証し、承認後に再投入する。[手動更新と復旧](../operations/mvp-release.md#手動更新と復旧)

依頼者の指示で公式リンク先行版の準備を開始。[公開ワークフロー](../../.github/workflows/publish-official-links.yml)の梱包工程をローカルで実行し、配布対象がトップページ・404・CSS の3ファイル（5,774バイト）であることと、各ファイルの SHA-256 を確認した。ローカルファイルを使った Chrome の検証では、320 CSS px の画面、公式リンク2件、プロジェクト配下の404とトップへの復帰を確認した。[先行版の配布手順](../operations/mvp-release.md#公式リンク先行版の配布)

依頼者の承認により、初回プッシュ予定の既存29コミットのメールアドレスを GitHub の `noreply` に置き換え、このリポジトリの今後のコミットも同じ設定にした。各コミットのファイル内容と作業中の差分が維持されたことを照合。先行版のコミットを含む公開予定の `main` 全30コミットについて、Gitleaks の検出は0件、著者・コミッターのメールアドレスはすべて `noreply`。

依頼者が承認した `main` 全30コミットを初回プッシュし、コミット `6f7cd69` を対象に [GitHub 上の検証](https://github.com/Olein-jp/japan-infection-watch/actions/runs/45522777320) と [先行版のデプロイ](https://github.com/Olein-jp/japan-infection-watch/actions/runs/45522869066) が成功した。Pages の公開元は GitHub Actions、公開環境の許可ブランチは `main`、HTTPS 強制は有効。公開サイトのトップが HTTP 200、未定義パスが HTTP 404 を返し、トップ・CSS・404 の本文が対象コミット内のファイルと一致した。[公開サイト](https://olein-jp.github.io/japan-infection-watch/)

JIHS の数値版は資料別の条件と公開用成果物を確認してから判断する。

### JIHS の数値版に向けた問い合わせ

2026-11-25（JST）に、国立感染症研究所の公式案内に掲載された総合窓口 `info@nih.go.jp` へ問い合わせを送信した。IDWR 事務局を担当する感染症サーベイランス研究部などへの取り次ぎを依頼した。[国立感染症研究所の問い合わせ案内](https://www.niid.jihs.go.jp/contacts/contacts.html)・[事務局の掲載箇所](https://id-info.jihs.go.jp/surveillance/idwr/idwr/2026/idwr2026-21.pdf#page=33)

> IDWR 速報の「定点把握疾患（週報告）、報告数、定点当たり報告数、都道府県別」の CSV について、全国と都道府県の公表値を無料のウェブサイトで直近6か月のグラフと表にして公開できるか確認したく、ご連絡しました。原資料の週別ページ、対象週、出典、当方で表示用に整形した旨を表示し、報告数・定点当たり報告数と欠損の意味は変更しません。グラフの描画に必要な数値は当サイト内の JSON に格納する予定です。
>
> 貴サイトの利用規約第1項・第7項に照らし、この用途で個別の許諾が必要か、必要な場合は手続きを教えていただけますでしょうか。対象 CSV に適用される個別条件や、指定の出典表記があれば併せてお知らせください。

対象資料の例は [2026年第46週の速報ページ](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/index.html)。初回は手動更新を想定し、定期取得の条件は別途扱う。

### JIHS の回答と数値版への反映

2026-11-26（JST）に、依頼者が共有した JIHS 国立感染症研究所 info 受付窓口経由の担当部署回答（S102）を確認した。回答は、IDWR 速報データの引用・転載・複製が出所の明示を条件に可能であり、独自グラフは出典と別に独自の編集・加工を明示するよう求めている。利用許諾の対象は元データの利用で、加工後の成果物の公認は含まれない。公開規約第1項の出典・加工表示と整合する。[JIHS 利用規約](https://id-info.jihs.go.jp/usage-contract.html)

数値版の表示例。出典欄には実際に使った各週の公式速報ページへのリンクを添える。

- **出典**　国立健康危機管理研究機構（JIHS）感染症情報提供サイト「IDWR速報データ」。
- **編集・加工**　Japan Infection Watch が速報 CSV をもとに独自に集計値を整形し、グラフを作成。

問い合わせには直近6か月分のグラフ・表と描画用 JSON を含めた。回答は独自グラフを例にデータ利用の条件を示しており、表・JSON の配布条件や採用対象の各週に固有の条件への個別の言及はなかった。公開判定では、規約の公衆送信に関する一般条件に加え、第2・7項、各週の注記、JSON の収録項目と出典・加工の表示方法を照合する。収録全週と公開用成果物の検証・依頼者の公開承認は未了。自動取得の頻度と長期保存は引き続き R-16 で扱う。本更新では回答と規約の文書照合を行った。

### 手元の Mac で実データを閲覧する

確認済みの2026年第45・46週の定点速報 CSV を手動取得し、Git 管理外の `artifacts/jihs-local/` に置く。リポジトリのルートで次のコマンドを実行し、表示された `http://127.0.0.1:8765/` を開く。停止は Ctrl+C。別のプロセスが同じポートを使用している場合は `--port` で変更できる。

```sh
python3 -B -m apps.web.local artifacts/jihs-local/2026-45-teiten.csv artifacts/jihs-local/2026-46-teiten.csv \
  --school-report artifacts/jihs-local/mhlw-report10.json --school-report artifacts/jihs-local/mhlw-report11.json
```

ローカルの入力から一時ディレクトリに閲覧用ファイルを作り、ループバックだけで配信する。公開用ワークフローでは使用せず、終了時に生成済みの閲覧用ファイルを片付ける。画面上で速報の対象週、原資料、出典、表示用に整形した旨を確認できる。

`--school-report` は任意。厚生労働省の第10・11報を [R-10 の抽出手順](../../poc/mhlw/README.md)で処理した JSON を指定すると、都道府県ごとの報告区分で、その週に学級閉鎖・学年閉鎖・休校を実施した施設数を棒グラフで表示する。別掲市の行は合算しない。未収録週や計数不明をゼロで補わない。原表へのリンクは各週に表示する。

トップの地域選択、全都道府県ページの学級閉鎖欄、個別の公式案内を登録済みの市区町村ページには、日本学校保健会の市区町村別・自治体指定のグラフへのリンクを共通表示する。学校保健会の指標は閉鎖中のクラス数で、厚労省の閉鎖措置を実施した施設数と区別する。岐阜市は確認した厚労省の報告で別掲されていない。[日本学校保健会の公式案内](https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping)・[厚労省第11報の地域表](https://www.mhlw.go.jp/content/001770872.pdf#page=4)

2026-11-25（JST）に各 CSV を1回取得し、HTTP 200、第45週11,238バイト、第46週11,269バイトを確認。Chrome で岐阜県のインフルエンザを開き、2週の報告数と定点当たり報告数を原 CSV と照合した。折れ線と週別出典の表示、画面内の通信がループバック宛てであること、別ホスト名でのアクセスが HTTP 403 になること、架空プレビューの検査が実データ版を拒否することを確認した。[第45週速報](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/45/index.html)・[第46週速報](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/index.html)

### 第45・46週の数値版の検証

2026-11-26 10:35 JST 前後に、公式の第45・46週の掲載ページと利用規約の冒頭・第1・2・7項を照合した。該当する週次定点 CSV の掲載欄では、速報値が週報・年報で修正され得る旨を確認し、個別の転載制限や第三者の権利表示は見当たらなかった。CSV は前日に取得した2ファイルだけを再利用し、新規の CSV 取得は0件。[利用規約](https://id-info.jihs.go.jp/usage-contract.html)・[第45週の掲載欄](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/45/index.html)・[第46週の掲載欄](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/index.html)

表示用 JSON の各観測行は、対象期間、指標、単位、値、値の状態、版 ID に絞る。地域・疾患は配信パスに含め、最新値と履歴の両方の JSON に出典、編集・加工の表示、対象週の公式 URL を保持する。原本 CSV、原本の行・列構造、厚労省の実集計を検証用の書き出しに含めない。対象2週の検討では、原資料の修正を伴わない抽出と表示用整形として公開規約に照らした。JSON 単体の配布に対する個別回答は得ておらず、公開判定では実際の配布項目と対象週で判断する。

| #25 の受入条件 | 今回の確認 |
|---|---|
| 利用条件、公開範囲、費用と監査 | HTML の出典と編集・加工の表示、および各 JSON の項目・出典・ハッシュと成果物の許可リストを検査した。2週分は1,945ファイル、展開後4,147,102バイト、ローカルの tar.gz は222,103バイト。GitHub Pages の容量条件に余裕がある規模。アカウントの共有枠の再確認と本番成果物の監査は公開前に行う。 |
| 手動更新・停止・復旧 | 元 CSV と履歴 JSON の3,648セルを照合し、数値2,544セルと原表ハイフン1,104セルが一致。第46週は最新値 JSON と履歴も一致。日時だけ変えた再生成は変更なし。保存した圧縮版から復元したハッシュは元の配布一式と一致し、1バイト追加した候補を拒否した。 |
| 公開 URL・版・代表ページと JSON | 先行版の既存の CI・デプロイが成功したことを GitHub Actions のジョブで再確認。数値版の manifest・索引・JSON はローカルファイルで照合し、公開可否は false。今回の環境ではループバック HTTP の待受が `[Errno 1] Operation not permitted` のためブラウザ統合試験の再実行は未完了。 |

Python 3.13.5 でテスト33件が通過。検証用一式の SHA-256 は `d684581453a85e6c0de81290ab2385d7eac87296c7c3d32669855d86c65a807b`（再現検証時の生成・入力読込日時は `2026-11-26T10:00:00+09:00` に固定）。操作の入口は[数値版のローカル検証手順](../operations/mvp-release.md#jihs-数値版のローカル検証)。収録する追加週の条件と入力、数値版の受け渡し・復旧担当と保管先、公開成果物の監査と公開承認が揃うまで、#25 は継続する。
