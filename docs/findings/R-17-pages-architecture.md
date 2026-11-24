# R-17　GitHub Pages・Actions の構成比較とローカル検証

対象は [Issue #17](https://github.com/Olein-jp/japan-infection-watch/issues/17)。確認日 2026-11-24（JST）。架空データの静的ビルドと復旧のローカル試験まで検証し、2026-11-24（JST）に調査を完了した。実際のデータの定期取得・保存・公開は [R-16](R-16-collection-operations.md) の条件確認と承認を要する。

**検証結果。** 都道府県の週次集計は、容量に余裕を持つ初期構成の候補。全市区町村の日次履歴1年分は、今回の行形式で約3.65 GBとなり、データだけで Pages の公開サイト上限を超える。日次の公開期間・対象地域を絞るか、履歴の配布先を分ける構成を #18 で比較する。

## GitHub の公式条件

| 項目 | 確認結果と適用範囲 |
|---|---|
| リポジトリとサイト | `gh api repos/Olein-jp/japan-infection-watch` で公開、既定ブランチ `main`、`has_pages: false` を確認。GitHub Free は公開リポジトリから Pages を利用できる。Private からは GitHub Pro・Team・Enterprise などが対象。リポジトリが Private でもサイトは一般公開され得る。サイトそのものを非公開にする機能は組織の Enterprise Cloud 等の要件がある。[Pages の対象プラン](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)・[サイトの非公開設定](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/about-privately-published-github-pages-sites) |
| Pages の使用量 | ソースリポジトリは1 GB推奨。公開サイトは1 GB以下、デプロイは10分でタイムアウト、帯域は月100 GBのソフト上限。時間当たり10ビルドのソフト上限はカスタム Actions ワークフローに適用されない。artifact の tar の条件と公開サイト上限は別。公開用ディレクトリの実サイズを計る。[Usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits#usage-limits)・[artifact 条件](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages#configuring-the-upload-pages-artifact-action) |
| 利用用途 | 無料の公共情報閲覧サイトを候補とする。オンライン事業、EC、商取引・商用 SaaS を主目的とする用途に無償ホスティングを使用することは制限される。寄付ボタン等が一部認められる記載はある。広告・有料機能を含める場合は実際の用途と条件を再評価する。[追加製品利用条件 Pages 節](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#pages) |
| Actions の処理時間 | GitHub-hosted runner のジョブは最大6時間。Pages のデプロイ工程の上限は10分。処理はローカル試験で計測し、GitHub-hosted Linux での実行時間はまだ未計測。[Actions limits](https://docs.github.com/en/actions/reference/limits) |
| 課金 | 標準 GitHub-hosted runner は Public と GitHub Pages 用途で無償とされ、大型 runner は Public でも課金対象。Private の一般処理の月次同梱枠は Free が12 USD、Pro・Team が18 USD、Enterprise Cloud が300 USD。標準 Linux x64／2コアは0.006 USD/分換算で、Free は2,000分、Pro・Team は3,000分に相当する。他の利用と枠は共有。artifact の同梱は Free 500 MB、Pro 1 GB、Team 2 GB、Enterprise Cloud 50 GB、超過は0.25 USD/GB月。cache はリポジトリごとに10 GBを含み、上限を拡張した際の超過は0.07 USD/GB月。[Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) |
| プラン料金 | 現状の公開リポジトリには Free 構成を候補とする。組織向けの表示価格は Team が4 USD/ユーザー月、Enterprise が21 USD/ユーザー月。個人の Private で使う場合は GitHub Pro のアカウント料金を確認する。実アカウントの契約、残枠、税・外部保管料は本試算に含めていない。[GitHub Pricing](https://github.com/pricing) |
| schedule・トークン・権限 | schedule の UTC 既定・タイムゾーン指定、毎時00分付近の遅延・取りこぼし、60日無活動の無効化、既定ブランチ、手動復旧を確認。公開ジョブの権限と、トークンによる push の後続起動制限は[構成候補](../architecture/pages-layout.md)に記載。[schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)・[公開ジョブ](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages#deploying-github-pages-artifacts) |

## 架空データによる実測

[再現手順](../../poc/pages/README.md)。macOS arm64、Python 3.13.5、Node.js 20.19.2、Playwright 1.58.2、Chrome 158.0.8127.37。ローカル HTTP サーバーをループバックに限定し、ブラウザからのテスト対象外へのリクエストを遮断した。

| 試験 | 結果 |
|---|---|
| 配布一式・ビルド | 架空2地域・1疾患の静的 HTML、CSS、JS、manifest、最新・履歴 JSON、GeoJSON。プロジェクトパスは1版12ファイル・14,523バイト。ビルドは3回とも約0.003秒（Python 起動前の時間は含まない）。ルート配置は12ファイル・14,163バイト。別試行で tar.gz を作り、通常ファイル・ディレクトリだけで構成されることを確認 |
| プロジェクトパスとルート | `/japan-infection-watch/` 配下で直リンクと再読み込みに成功。末尾スラッシュなしからありに転送。アセット・最新 JSON と地図は同一パス配下。存在しない地域は HTTP 404 と独自の戻りリンク。独自ドメイン相当の `/` 配置でも直リンクとデータ読み込みが成功。実ドメイン・DNS は未試験 |
| 分割読み込みと鮮度 | 対象地域の最新 JSON と GeoJSON を読み、月別履歴はボタン操作後に取得。初回のリクエストに他地域の最新 JSON や月別履歴は含まれなかった。値と対象期間、提供元の更新日、取得時刻、生成時刻を表示。時計を更新予定後に固定し、予定超過の表示を確認 |
| スマートフォン相当 | 幅390 CSS px で横スクロールなし。初回は7リソース、HTTP 応答本文が計10,161バイト。DOMContentLoaded 約44 ms（ローカル1試行、低速回線・実機の性能は未測定）。GeoJSON を2図形で表示し、欠損地域にテキストの凡例と表を表示。架空矩形の直線上の中間点を除いた比較では402→10頂点、5,027→370バイト。実境界の形状・面積への影響は未検証 |
| 失敗時の旧版保持 | 候補版の JSON を破損させ、サイズ・ハッシュの不一致で終了コード2。アーカイブに候補を追加せず、公開先の参照と manifest の内容を維持。Chrome で旧版の地域ページを再読込できた。ローカル切り替えの検証結果で、Pages サーバーの障害・実デプロイの復旧は未検証 |

Astro、Vite、静的 HTML＋JS の比較、公開ジョブの権限、保管先の比較は[構成候補](../architecture/pages-layout.md)。実測したビルドは静的 HTML＋JS。フレームワークの採用は対象ページの規模を見て判断する。

## 容量・時間・費用の試算

`python3 poc/pages/measure.py` で R-15 の行に沿った JSON を作り、1年分の最新・月別履歴、各索引のサイズを測った。2030年の架空日付を使用。都道府県は47件、市区町村は12件分の実測を日次数と地域数で比例拡大した。市町村計1,724（6村を含む）から6村を除き、特別区23を加えた1,741を基準に、行政区171と6村を含む1,918も上振れ側として試算した。これは容量計算上の仮定であり、公開対象地域の決定ではない。[e-Stat 市区町村数（2026-01-01）](https://www.e-stat.go.jp/municipalities/number-of-municipalities?day=1&file_format=csv&form_id=city_count_form&month=1&year=2026)

| 想定 | 観測行・JSON 分割数（最新・履歴） | 未圧縮・JSON のみ | 地域別索引の全合計 | JSON 生成・書込・ハッシュ・gzip |
|---|---:|---:|---:|---:|
| 47都道府県 × 19疾患 × 2指標、週次1年 | 94,658行・11,609ファイル | 45.45 MB | 4.03 MB | 1.53秒（47件実測） |
| 1,741市区町村 × 6疾患 × 2指標、日次1年 | 7,646,472行・135,798ファイル | 約3.65 GB | 約48.42 MB | 約55秒（12件で0.382秒） |
| 1,918市区町村等、その他は同じ | 8,423,856行・149,604ファイル | 約4.05 GB | 約54.24 MB | 約63秒（12件で0.395秒） |

容量は十進単位。上表の時間は HTML の大量生成、地図生成、tar 作成、runner 起動、通信、アップロード・デプロイを含まない。小ファイルが多いためファイル数の増加が tar 作成やアップロード時間に及ぼす影響は別途測る。各ファイルを gzip にした合計の試算は、順に約5 MB、127 MB、142 MB。転送・圧縮で小さくなっても、公開サイトの容量判定は展開後の成果物全体で評価する。地図、複数提供元、別途保管する版、アーカイブのメタデータは別枠。

全ファイルの参照を単一 manifest に置くと、毎回読み込む索引が大きくなる。地域別索引の最大は都道府県で約86 KB、市区町村で約28 KBだった。ルート manifest は少量の出典・鮮度と対象範囲を持ち、該当地域の索引を追加取得する案を比較する。日次履歴の最新＋直近1か月は、31日を一様とみなす簡易計算で約0.32 GB（`3.65 × (31 + 1) / (365 + 1)`）。地図・別系列・HTML を含めて予算を再確認する。

- **初期予算の候補。** 公開一式500 MB、月間帯域50 GB、デプロイ5分を管理上の予算とする。初回400 KBを10万回配信すると40 GB/月。リピート時のキャッシュや圧縮、履歴の追加閲覧、地図の影響は利用実態で再計測する。
- **Actions 使用量の候補。** 月12回×8分＝96分（週次2系統と再実行を含む仮定）。一般の Private の Linux 2コア課金換算で0.576 USD相当で、同梱枠に空きがあれば追加分は0 USD。毎日1回と月6回の再実行を仮定した36回×8分でも288分・1.728 USD相当。8分は見積もり枠。標準 runner での計測や他のワークフローの使用量は今後確認する。
- **保管の予算。** 100 MBの artifact が同時に2件あると200 MB。1日で消えるビルド引渡し用 artifact と、復旧用に長期保持する配布版を分ける。前者の計算には Packages との共有量と月内の保持時間を含める。後者の保存先・実料金は公開対象容量と契約を確認して決める。

## 受入基準と残課題

Pages・Actions の利用条件、公開範囲、制限、費用と余裕を確認し、付録Aの静的生成・分割配布・地域ページ・障害時の公開維持を架空データのローカル試験で評価した。公開設定、実デプロイ、定期実行、課金設定は調査対象外とした。#18 には、都道府県週次の初期候補と、市区町村の拡張時の期間短縮・データ形式の圧縮・静的配信の分離を引き継ぐ。実データの公開、全地域の取得可否、実境界の簡略化、GitHub 上の時間・費用・復旧は後続で確認する。
