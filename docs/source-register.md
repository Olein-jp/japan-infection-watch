# 一次情報管理台帳

初期指示書に挙がった候補。提供主体、到達性、資料の版、利用条件、実データの取得形式は各調査で確定する。形式欄は候補 URL の参照先形式。

確認後は日付（JST）、改訂日、規約のリンク・該当箇所・適用範囲、検証結果を記入する。移転時は旧 URL と置換先を併記する。

| ID | 提供主体・運営（候補） | 資料 | URL | 公開・改訂日 | 確認日（JST） | 形式（候補） | 利用条件 | 検証状態 |
|---|---|---|---|---|---|---|---|---|
| S01 | 日本学校保健会 | 日本学校保健会 マップビュー・API案内 | <https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping> | 2024-03-25（最新の変更告知） | 2026-11-24 | Web | 通常閲覧可。集計の外部利用は確認待ち | R-01 で掲載表、R-02 で提供経路の区別を確認 |
| S02 | 日本学校保健会 | 学校情報等検索API仕様 | <https://www.gakkohoken.jp/files/ccenter/mapview/20220825api_specification.pdf> | — | — | PDF | 未確認 | 未検証 |
| S03 | 日本学校保健会 | 学校情報等検索API利用規約 | <https://www.gakkohoken.jp/files/ccenter/mapview/terms_of_use.pdf> | 2022年4月（表紙） | 2026-11-24 | PDF | 学校検索 API に適用。制限・更新義務あり | R-02 で第1・2・4・5・7条を確認 |
| S04 | 日本学校保健会 | システム使用規程 | <https://www.gakkohoken.jp/files/ccenter/system/20230803/202308mapview.pdf> | 2014-01-01 施行、2023年8月改訂（附則） | 2026-11-24 | PDF | 使用資格と統計化情報の公開条件。外部再利用は確認待ち | R-02 で第2・5〜13・18項と附則を確認 |
| S05 | 日本学校保健会 | マップビューマニュアル | <https://www.gakkohoken.jp/files/ccenter/20220412/mapview-manual.pdf> | 2022-04-12（S01 掲載） | 2026-11-24 | PDF | 未判定 | R-01 で当時の表示仕様を確認 |
| S06 | 日本学校保健会 | マップビュー研修資料 | <https://www.gakkohoken.jp/files/ivent/20240722/program-02.pdf> | 2024-07-22（研修開催日） | 2026-11-24 | PDF | 未判定 | R-01 で定義・日付操作を確認 |
| S07 | 日本学校保健会 | 表示変更資料 | <https://www.gakkohoken.jp/files/ccenter/mapview/202303view_change.pdf> | 2023-03-15（S01 告知） | 2026-11-24 | PDF | 未判定 | R-01 で疾患区分・市区町村実績表の追加を確認 |
| S08 | 日本学校保健会のマップビュー掲載プロフィール（Tableau Public） | Tableau Publicプロフィール | <https://public.tableau.com/app/profile/jssh.absence.information.mapping.service> | 不明 | 2026-11-24 | Web | 通常閲覧可。公開集計の取得・再配布は確認待ち | R-01 で公開入口、R-02 で代表ビューの共有と出力メニューを確認 |
| S09 | Tableau | Tableau Embedding API データ取得 | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_data.html> | 不明 | 2026-11-24 | Web | 一般仕様。対象ビューからの取得許可は未確認 | R-04 で公式サンプルの先頭ページを取得 |
| S10 | Tableau | Tableau エクスポート | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_export.html> | 不明 | 2026-11-24 | Web | 一般仕様。代表ビューのメニューに CSV なし | R-04 で公式サンプルの出力と CSV ファイルの2指標を照合 |
| S11 | Tableau | Tableau 認証 | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_auth.html> | 不明 | 2026-11-24 | Web | Public の埋め込みは通常認証不要 | R-02 で認証要件の一般仕様を確認 |
| S12 | Tableau | Tableau 利用規約 | <https://www.tableau.com/tos> | 2022-07-19 最終更新 | 2026-11-24 | Web | 公開コンテンツの許諾あり。対象集計と S35 との関係は未確定 | R-02 で適用対象、投稿許諾、権限の保証と制限を確認 |
| S13 | Tableau | Tableau Public FAQ | <https://help.tableau.com/current/pro/desktop/ja-jp/public_faq.htm> | 不明 | 2026-11-24 | Web | 共有と出力は機能・公開者設定に依存 | R-02 で FAQ の共有・ダウンロード項目を確認 |
| S14 | Tableau | Tableau Public Data Policy | <https://public.tableau.com/app/data-policy> | 不明 | 2026-11-24 | Web | 投稿者が掲載に責任を負う | R-02 でブラウザ表示から掲載責任・削除条件を確認 |
| S15 | JIHS | JIHS IDWR | <https://id-info.jihs.go.jp/surveillance/idwr/> | 不明 | 2026-11-24 | Web | S53 を参照 | R-09 で速報年別一覧と週報一覧への導線を確認 |
| S16 | 厚生労働省 | 厚労省 令和8年度急性呼吸器感染症対策 | <https://www.mhlw.go.jp/stf/index2026.html> | 不明 | 2026-11-24 | Web | S60 を参照 | R-10 で週次報道発表の案内と学校欠席者数の集計対象を確認 |
| S17 | 岐阜県 | 岐阜県感染症情報センター | <https://www.pref.gifu.lg.jp/page/9550.html> | 不明 | 2026-11-24 | Web | S70 | R-11 で週報・患者報告数データ・制度説明の入口を確認 |
| S18 | 岐阜県 | 岐阜県週報 | <https://www.pref.gifu.lg.jp/page/107799.html> | 2026-11-19（第46週） | 2026-11-24 | Web・PDF | S70 | R-11 で2026年第46週の情報編とデータ・グラフ編、発行頻度を確認 |
| S19 | 岐阜県 | 岐阜県発生動向データ | <https://www.pref.gifu.lg.jp/page/9553.html> | 2026年第46週まで掲載 | 2026-11-24 | Web・Excel | S70 | R-11 で全数・定点の形式を確認し、S66 を実行検証 |
| S20 | 総務省 | 全国地方公共団体コード | [登録時の URL](https://www.soumu.go.jp/denshijiti/code.html)・[e-Gov データポータル](https://data.e-gov.go.jp/data/dataset/soumu_20140909_0395) | 配布元の版を参照 | 2026-11-24 | Web | 今回はコード体系の参照 | 登録時の URL は調査環境で本文を取得できず。S76・S87 を参照 |
| S21 | 文部科学省 | 文科省 学校コード | <https://www.mext.go.jp/b_menu/toukei/mext_01087.html> | — | — | Web | 未確認 | 未検証 |
| S22 | 国土交通省 | 国土数値情報 N03 行政区域 | [総合案内](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html)・[2026年版](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2026.html) | 2026-01-01基準、2026年4月更新 | 2026-11-24 | GML・シェープファイル・GeoJSON | 2026年版は CC BY 4.0 表示。測量法の公表・再配布手続は R-16 | 岐阜県 ZIP を取得し、岐阜市の図形を変換・照合 |
| S23 | 神戸市保健所 | 神戸市感染症統合情報システムの学級閉鎖情報 | <https://kobecity-kmss.jp/classclosure> | 市の運用案内は2026-09-01更新 | 2026-11-24 | Web・PDF／CSV表示 | 外部ドメインの個別利用条件は未確認 | 市公式案内で運営を確認。地図・表・CSV 表示を文書確認 |
| S24 | 北九州市保健所 | インフルエンザ様疾患による学級閉鎖等の報告状況 | <https://www.city.kitakyushu.lg.jp/contents/334_00031.html> | 2026-11-20更新 | 2026-11-24 | HTML・PDF | 市サイトのリンク・著作権案内。カタログとは適用経路が異なる | 報告日別の表頭、延長の扱い、週次集計のリンクを確認 |
| S25 | 東京都 | 東京都オープンデータ API カタログ | [登録時の URL](https://spec.api.metro.tokyo.lg.jp/)・[都の API 一覧](https://portal.data.metro.tokyo.lg.jp/opendata-api/) | 仕様表示1.0.0 | 2026-11-24 | Web | 個別 API・データの規約を参照 | 登録時の URL は本文を読み取れず、都の公開一覧で閉鎖該当項目を確認できなかった |
| S26 | GitHub | GitHub Pages 制限 | <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits> | 閲覧時の仕様 | 2026-11-24 | Web | 対象プラン・用途・容量・帯域など | R-17 で Usage limits と対象プランを照合。R-18 で月0円の評価に再確認 |
| S27 | GitHub | GitHub Pages カスタムワークフロー | <https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages> | 閲覧時の仕様 | 2026-11-24 | Web | artifact と公開権限の要件 | R-17 で build と deploy、公開用 artifact の条件を確認 |
| S28 | GitHub | GitHub Pages 公開元の設定 | <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site> | 閲覧時の仕様 | 2026-11-24 | Web | 対象プランと設定権限 | R-17 でブランチと Actions の公開元を比較 |
| S29 | GitHub | GitHub Actions イベント・schedule | <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule> | 閲覧時の公式文書 | 2026-11-24 | Web | 文書参照 | schedule の遅延・未実行、既定ブランチ、公開リポジトリの無活動による無効化を確認 |
| S30 | GitHub | GitHub Actions 課金 | <https://docs.github.com/en/billing/concepts/product-billing/github-actions> | 閲覧時の料金 | 2026-11-24 | Web | 計算枠と超過料金はプラン別 | 旧 URL の転送先。R-17 で runner と保管費用を確認 |
| S31 | GitHub | GitHub 追加製品利用条件 | <https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#pages> | 2026-08-27発効表示 | 2026-11-24 | Web | Pages 節の用途制限 | R-17 で営利用途と静的配信の扱いを文書確認 |
| S32 | 日本学校保健会 | 2024年のマップビュー表示変更 | <https://www.gakkohoken.jp/files/ccenter/mapview/20240325view_change.pdf> | 2024-03-25（S01 告知） | 2026-11-24 | PDF | 未判定 | R-01 で初期表示・閉鎖クラス合算を確認 |
| S33 | 日本学校保健会 | 登録状況・利用状況の推移（2020・2025年度比較） | <https://www.gakkohoken.jp/files/ccenter/system/registration_status_and_usage_status_2025.pdf> | 公開日は不明。2025年度分は 2026-03-31 時点 | 2026-11-24 | PDF | 未判定 | R-01 で施設種別、登録率と利用率の分母を確認 |
| S34 | 株式会社エスイーシー（日本学校保健会掲載） | 2026年マップビュー研修資料 | <https://www.gakkohoken.jp/files/ivent/20260722online/20260722siryo-01.pdf> | 2026-07-22（研修開催日） | 2026-11-24 | PDF | 未判定 | R-01 で指標・表示対象日・更新時点を確認 |
| S35 | Salesforce | Salesforce サイト利用規約 | <https://www.salesforce.com/company/legal/sfdc-website-terms-of-service/> | 2025-04-08 最終更新 | 2026-11-24 | Web | 第三者コンテンツ利用には権限等が必要 | R-02 で代表ビューのフッターからの導線と E〜G 節を確認 |
| S36 | Salesforce | Acceptable Use and External-Facing Services Policy | <https://c1.sfdcstatic.com/content/dam/web/en_us/www/documents/legal/Agreements/policies/ExternalFacing_Services_Policy.pdf> | 2025-03-10 改訂 | 2026-11-24 | PDF | サービスの利用制限。第三者サイトへのクロール条項あり | R-02 で第1・3・5・6節を確認 |
| S37 | 日本学校保健会 | ポータルの著作権とリンク条件 | <https://www.gakkohoken.jp/about> | 不明 | 2026-11-24 | Web | ポータル掲載物の営利再利用制限、条件付きリンク | R-02 で第3〜5節を確認 |
| S38 | Tableau | Embedding API 基本表示 | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_basic.html> | 不明 | 2026-11-24 | Web | 公開ビューの埋め込み機能。集計取得の条件は確認待ち | R-03 で代表ビューの v3 表示を確認 |
| S39 | 日本学校保健会 | 2026年度自治体向けオンライン説明会資料 | <https://www.gakkohoken.jp/files/ivent/20260624/siryo1.pdf> | 2026-06-24（開催日） | 2026-11-24 | PDF | 自治体向け個別ビュー案内。外部データ提供の要件は確認待ち | R-02 で pp.83–86、p.88 を確認 |
| S40 | Tableau | Tableau Public robots.txt | <https://public.tableau.com/robots.txt> | 不明 | 2026-11-24 | テキスト | クロールの設定 | R-02 で HTTP 200 と Crawl-delay を確認 |
| S41 | Tableau | Tableau Public Desktop EULA | <https://mkt.tableau.com/legal/tableau_eula_public.pdf> | 2024年11月版 | 2026-11-24 | PDF | 対象デスクトップ製品の利用・商用制限 | R-02 で第1・3・6節と Public サイトとの適用対象の違いを確認 |
| S42 | Tableau | Embedding API イベント購読 | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_event.html> | 不明 | 2026-11-24 | Web | 公式仕様 | R-03 で FirstInteractive の受信を確認 |
| S43 | Tableau | Embedding API フィルター | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_filter.html> | 不明 | 2026-11-24 | Web | 公式仕様 | R-03 でダッシュボードのフィルター名4件を確認 |
| S44 | Tableau | Embedding API Workbook | <https://help.tableau.com/current/api/embedding_api/en-us/reference/interfaces/Workbook.html> | 不明 | 2026-11-24 | Web | 公式仕様 | R-03 で公開シート2件を確認 |
| S45 | Tableau | Tableau Public 配信の Embedding API モジュール | <https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js> | 観測時 3.17.0-pre.14（ファイル先頭の注記） | 2026-11-24 | JavaScript | 表示検証に使用。対象ビューのデータ再利用は確認待ち | R-03 で HTTP 200 と動作を確認 |
| S46 | Tableau | Embedding API の入手と互換性 | <https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_get.html> | 文書生成 2026-11-23 UTC | 2026-11-24 | Web | 公式仕様 | R-03 で同一配信元のライブラリを使用 |
| S47 | Tableau | DataTableReader | <https://help.tableau.com/current/api/embedding_api/en-us/reference/interfaces/DataTableReader.html> | 不明 | 2026-11-24 | Web | 公式 API 仕様 | R-04 でページ数・総行数・先頭ページ・解放を確認 |
| S48 | Tableau | Worksheet | <https://help.tableau.com/current/api/embedding_api/en-us/reference/interfaces/Worksheet.html> | 不明 | 2026-11-24 | Web | 公式 API 仕様 | R-04 で getSummaryDataReaderAsync のページサイズ指定を確認 |
| S49 | Tableau | DataTable | <https://help.tableau.com/current/api/embedding_api/en-us/reference/interfaces/DataTable.html> | 不明 | 2026-11-24 | Web | 公式 API 仕様 | R-04 で列・型・行の取得結果を確認 |
| S50 | JIHS | IDWR速報データ 2026年第45週 | <https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/45/index.html> | 2026-11-17 掲載 | 2026-11-24 | Web・CSV | S53 を参照。R-09 で少数取得・ローカル検証 | 更新欄と週次定点 CSV を確認。S52 と全指標を照合 |
| S51 | JIHS | IDWR速報データ 2026年第46週 | <https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/index.html> | 2026-11-24 掲載 | 2026-11-24 | Web・CSV | S53 を参照。R-09 で少数取得・ローカル検証 | 更新欄と週次定点 CSV を確認。第46号 PDF は未刊行 |
| S52 | JIHS | IDWR 2026年第45号 | <https://id-info.jihs.go.jp/surveillance/idwr/idwr/2026/idwr2026-45.pdf> | 2026-11-20 発行 | 2026-11-24 | PDF | p.37 に個別の転載注記 | pp.32–34 の週次定点表を S50 と照合。p.37 に訂正方針 |
| S53 | JIHS | 感染症情報提供サイト利用規約 | <https://id-info.jihs.go.jp/usage-contract.html> | 2014-08-25 制定（8項） | 2026-11-24 | Web | 出典、加工明示、第三者権利、個別注記等の条件あり | R-09 で冒頭と1・2・5・7・8項を確認。継続運用と公開は R-16 |
| S54 | JIHS | 報告週対応表 2026年 | <https://id-info.jihs.go.jp/surveillance/idwr/calendar/2026/index.html> | 不明 | 2026-11-24 | Web | S53 を参照 | R-09 で公式週対応表の提供を確認 |
| S55 | JIHS | IDWR週報に関する訂正のお詫びとお願い | <https://id-info.jihs.go.jp/niid/ja/allarticles/surveillance/4755-teisei-owabi.html> | 不明 | 2026-11-24 | Web | S53 を参照 | R-09 で発生動向総覧の本文訂正例を確認 |
| S56 | JIHS | 感染症発生動向調査事業年報訂正箇所一覧 | <https://id-info.jihs.go.jp/surveillance/idwr/annual/correction/index.html> | 2012-10-09 公開、2026-11-02 訂正例 | 2026-11-24 | Web・Excel | S53 を参照 | R-09 で年報の集計表に対する訂正告知を確認 |
| S57 | 厚生労働省 | インフルエンザに関する報道発表資料 2026/2027 シーズン | <https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/kenkou/kekkaku-kansenshou01/houdou_00025.html> | 2026-11-20 時点の最新発表 | 2026-11-24 | Web | S60 を参照 | R-10 で11月13日・20日の公式 PDF へのリンクを確認 |
| S58 | 厚生労働省 | インフルエンザ様疾患発生報告 第10報 | <https://www.mhlw.go.jp/content/001768730.pdf> | 2026-11-13 発表 | 2026-11-24 | PDF | S60・S61。pp.4–5 の固有注記は確認されず | 地域表・脚注・施設種別内訳を実行確認 |
| S59 | 厚生労働省 | インフルエンザ様疾患発生報告 第11報 | <https://www.mhlw.go.jp/content/001770872.pdf> | 2026-11-20 発表 | 2026-11-24 | PDF | S60・S61。pp.4–5 の固有注記は確認されず | 地域表・脚注・施設種別内訳を実行確認 |
| S60 | 厚生労働省 | 利用規約・リンク・著作権等 | <https://www.mhlw.go.jp/chosakuken/index.html> | 不明 | 2026-11-24 | Web | PDL1.0 準拠。出典・加工の表記と適用外の別紙 | R-10 で冒頭と §1.1・§1.4・別紙を確認 |
| S61 | デジタル庁 | 公共データ利用規約（第1.0版） | <https://www.digital.go.jp/resources/open_data/public_data_license_v1.0> | 第1.0版 | 2026-11-24 | Web | 条件付き二次利用・商用利用 | R-10 で §1、§1.1–1.4 の出典・加工・第三者権利・例外を確認 |
| S62 | 岐阜県 | 発生動向調査とは・所管市町村表 | <https://www.pref.gifu.lg.jp/page/9576.html> | 2025-05-01 更新 | 2026-11-24 | Web・画像 | S70 | 5圏域・8保健所の所管表を原画像で確認 |
| S63 | 岐阜県 | 感染症サーベイランスシステムについて | <https://www.pref.gifu.lg.jp/page/246729.html> | 2026-10-15 更新 | 2026-11-24 | Web | 報告用アカウント申請制 | 施設所在地別の保健所を確認 |
| S64 | 岐阜県 | GIDWR 第46週 情報編 | <https://www.pref.gifu.lg.jp/uploaded/attachment/524049.pdf> | 2026-11-19 発行 | 2026-11-24 | PDF | S70 | p.1 の期間・発行日・保健所別地図を確認 |
| S65 | 岐阜県 | GIDWR 第46週 データ・グラフ編 | <https://www.pref.gifu.lg.jp/uploaded/attachment/524050.pdf> | 2026-11-19（第46週） | 2026-11-24 | PDF | S70 | pp.1、5、6 で保健所・医療圏・定点数を確認、S66 と照合 |
| S66 | 岐阜県 | インフルエンザ（ARI定点） | <https://www.pref.gifu.lg.jp/uploaded/attachment/523690.xls> | 2026年第46週まで | 2026-11-24 | XLS | S70 | 第44〜46週で県計・保健所別の列と値を検証 |
| S67 | 岐阜市 | インフルエンザについて | <https://www.city.gifu.lg.jp/kenko/kansensyou/1004450/1004453.html> | 2026-10-02 更新 | 2026-11-24 | Web | S71 | 県情報とリアルタイムシステムへの案内を確認 |
| S68 | 岐阜市 | 令和7年版岐阜市統計書 14.保健及び衛生 | <https://www.city.gifu.lg.jp/info/toukei/1008686/1038653/1038669.html> | 2026-04-01 更新 | 2026-11-24 | Web・XLS | S69 | シート「３(2)」の令和6年度届出数と脚注を確認 |
| S69 | 岐阜市 | 令和7年版岐阜市統計書 利用条件 | <https://www.city.gifu.lg.jp/info/toukei/1008686/1038653/1038654.html> | 2026-04-01 更新 | 2026-11-24 | Web・PDF | PDL1.0 と個別の重要情報 | 出典・加工の明記と第三者権利の条件を確認 |
| S70 | 岐阜県 | リンク・著作権・免責事項について | <https://www.pref.gifu.lg.jp/page/79328.html> | 2020-11-26 更新 | 2026-11-24 | Web | 原則リンク可。無断複製・転用を制限 | 週報・Excel のオープンライセンス表示は未確認 |
| S71 | 岐阜市 | リンク・著作権・免責事項 | <https://www.city.gifu.lg.jp/info/kouhou/1008373/site/1011572.html> | 不明 | 2026-11-24 | Web | 無断複製・転用を制限 | 市統計書・衛生年報の個別条件と区別 |
| S72 | 岐阜県 | オープンデータカタログ 利用方法・利用規約 | <https://www.pref.gifu.lg.jp/page/75247.html> | 2025-10-01 更新 | 2026-11-24 | Web | カタログに適用。原則 CC BY 4.0、個別注記あり | 県・市の共用カタログで配布形式を検索 |
| S73 | 岐阜県 | 新型コロナウイルス感染症に関する県内の感染動向等 | <https://gifu-opendata.pref.gifu.lg.jp/dataset/c11223-001> | 2023-05-08 更新（UTC） | 2026-11-24 | Web・CSV | データセット表記 cc-by-21-jp | 旧制度の居住地別週間集計の配布案内を確認 |
| S74 | 岐阜県医師会のドメイン | 岐阜県リアルタイム感染症サーベイランス | <https://infect.gifu.med.or.jp/influ/> | 不明 | 2026-11-24 | Web | データの個別条件未確認 | 市案内から転送、公開一時停止の表示を確認 |
| S75 | 東京都健康安全研究センター | 各地の感染症情報（地方感染症情報センター一覧） | <https://idsc.tmiph.metro.tokyo.lg.jp/klink/> | 2026-11-12 更新 | 2026-11-24 | Web | センターのサイト利用案内を参照。リンク先の条件は各提供元で確認 | 47都道府県の入口の発見に使用。到達性と代替根拠は [R-12 の一覧](findings/R-12-prefecture-inventory.md#都道府県別一覧) |
| S76 | 総務省（e-Gov データポータル） | 全国地方公共団体コード | <https://data.e-gov.go.jp/data/dataset/soumu_20140909_0395> | データセットの版は配布元に従う | 2026-11-24 | Web | 今回はコード体系の参照 | S20 の補助。都道府県の先頭2桁を一覧に使用 |
| S77 | 神奈川県衛生研究所 | 2026年第46週 インフルエンザ CSV・週報 | [CSV](https://www.pref.kanagawa.jp/sys/eiken/003_center/0001_weekly/csv/20261119-influenza_2026.csv)・[週報 p.8](https://www.pref.kanagawa.jp/sys/eiken/003_center/0001_weekly/pdf/wrR08_46.pdf#page=8) | 2026-11-19 | 2026-11-24 | CSV・PDF | 県サイトの利用案内あり。資料固有条件は未確認 | 市・保健所等の列を確認。第46週の全県と3市の定点率を照合 |
| S78 | 島根県・山口県の感染症発生動向データ提供サイト | 感染症発生動向調査のデータ抽出画面 | [島根県](https://pref.shimane.didss.dsvc.jp/nesid/opendata)・[山口県](https://pref.yamaguchi.didss.dsvc.jp/nesid/opendata) | 表示上の改訂日は未確認 | 2026-11-24 | Web・CSV選択画面 | 個別のライセンス本文は未確認 | 週定点・保健所別を選択可能。出力ファイルは未照合 |
| S79 | 福岡県 | 感染症発生動向調査週報 2026年 | <https://www.pref.fukuoka.lg.jp/contents/idwr2026.html> | 第46週 2026-11-19 | 2026-11-24 | Web・PDF | 県庁サイトに権利帰属の案内。研究所別サイトは適用範囲未確認 | 研究所の入口が HTTP 503 のため代替。県集計を確認 |
| S80 | 岐阜県感染症情報センター | 学校サーベイランスの案内、2024/25シーズン報告 | [案内](https://www.pref.gifu.lg.jp/page/107795.html)・[報告 pp.7–8](https://www.pref.gifu.lg.jp/uploaded/attachment/478328.pdf#page=7) | 入口は2026-11-19更新。報告は2025-12-10付 | 2026-11-24 | Web・PDF | S70。転送先の個別条件は未確認 | 学校情報リンクは停止案内に転送。シーズン中の閉鎖実施校数は県報告の表5で確認 |
| S81 | 神戸市教育委員会 | 感染症による学級閉鎖情報 | [発表一覧](https://www.city.kobe.lg.jp/a61516/kosodate/education/information/gakkyuheisa.html)・[11月20日発表](https://www.city.kobe.lg.jp/documents/80496/20261120841501.pdf) | 2026-11-20発表分 | 2026-11-24 | PDF | [一般規約](https://www.city.kobe.lg.jp/documents/19135/20170630041802-1.pdf)は出典・加工表示、第三者権利等を条件とする | 市立学校園、閉鎖学級数・始終期の見出しを確認 |
| S82 | 北九州市保健所 | インフルエンザ様疾患による学級閉鎖等の第46週集計 | <https://www.city.kitakyushu.lg.jp/files/001239461.pdf> | 2026-11-19発表 | 2026-11-24 | PDF | [市サイト利用案内](https://www.city.kitakyushu.lg.jp/category/file_0003.html)。資料固有条件は未確認 | p.1 の当週施設数と内訳を照合。週・施設単位の優先順位を確認 |
| S83 | 北九州市 | インフルエンザ施設別発生状況 | [データセット](https://data.bodik.jp/dataset/401005_influenzashisetsubetsuhasseijyokyo)・[利用規約](https://odcs.bodik.jp/401005/tos/) | 2025-03-28カタログ更新 | 2026-11-24 | CSV・XLSX | リソースに CC 表示。カタログ規約は原則 CC BY 4.0、個別条件・第三者権利あり | 2017/18〜2019/20年の配布を確認し、2019/20年 CSV の表頭12列を確認 |
| S84 | 東京都感染症情報センター | インフルエンザ様疾患による臨時休業の状況 | <https://idsc.tmiph.metro.tokyo.lg.jp/diseases/flu/flu/> | 2026-11-19更新 | 2026-11-24 | HTML・グラフ | [センター利用案内](https://www.tmiph.metro.tokyo.lg.jp/riyou/) | 第5節で都の施設種別累計と速報注記を確認 |
| S85 | 八王子市教育委員会 | 市立小中学校学級閉鎖状況・年度版教育統計 | [現行案内](https://www.city.hachioji.tokyo.jp/kurashi/kyoiku/003/009/001/p004843.html)・[2026年度版](https://www.city.hachioji.tokyo.jp/kurashi/kyoiku/002/011/p037863.html) | 現行案内2026-11-24更新 | 2026-11-24 | PDF | [市サイト著作権](https://www.city.hachioji.tokyo.jp/987/p012154.html)。現行 PDF の個別条件は未確認 | 現行の配布案内と年度表の指標、重複調整を確認 |
| S86 | 福岡県 | 学級閉鎖等の状況報告 2026/27シーズン | <https://www.pref.fukuoka.lg.jp/contents/seasonal-flu-alert-2026-2027.html> | 2026-11-20更新 | 2026-11-24 | Web・PDF | 県公式サイトの利用案内 | 県の公表対象から北九州市・福岡市・久留米市を除外する旨を確認 |
| S87 | 地方公共団体情報システム機構（J-LIS） | 全国地方公共団体コードの仕様・岐阜県内市町村 | [仕様・検査数字](https://www.j-lis.go.jp/spd/code-address/cms_1750514.html)・[岐阜県一覧](https://www.j-lis.go.jp/spd/code-address/tyuubu/cms_14214182.html) | 閲覧時の一覧 | 2026-11-24 | Web | コード・仕様の参照 | 6桁形式と検査数字を確認。9市町を N03 に照合 |
| S88 | 総務省統計局・統計センター | e-Stat 標準地域コード・岐阜市廃置分合 | [標準地域コード](https://data.e-stat.go.jp/lodw/provdata/lodRegion)・[岐阜市履歴](https://www.e-stat.go.jp/municipalities/cities/absorption-separation-of-municipalities/21201) | 柳津町編入は2006-01-01 | 2026-11-24 | Web | コード・履歴の参照 | 5桁、行政区分、旧柳津町の編入を確認 |
| S89 | 国土交通省 | 国土数値情報ダウンロードサイト利用規約 | <https://nlftp.mlit.go.jp/ksj/other/agreement.html> | 2026-03-23施行 | 2026-11-24 | Web | PDL1.0 と出典・加工表示、個別許諾条件を参照 | N03 の個別ページの版別条件と照合 |
| S90 | 浜松市 | 行政区の再編について | <https://www.city.hamamatsu.shizuoka.jp/kikaku/kuseido/> | 2024-01-01再編 | 2026-11-24 | Web | 変更履歴の参照 | 旧北区が中央区・浜名区に分かれたことを確認 |
| S91 | 岐阜市 | 市の位置・面積・人口 | <https://www.city.gifu.lg.jp/info/syoukai/1006141/1006142.html> | 面積は2025-04-01時点 | 2026-11-24 | Web | 面積公表値の参照 | N03 2026年版から計算した面積の規模を照合 |
| S92 | IETF | RFC 9110 HTTP Semantics | <https://www.rfc-editor.org/rfc/rfc9110.html#section-13> | 2022年6月 | 2026-11-24 | Web | 仕様参照 | §13.1.2・§13.1.3・§15.4.5 を条件付き取得と304の解釈に使用 |
| S93 | GitHub | Actions の同時実行、artifact の保持、履歴からの削除 | [同時実行](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency)・[artifact](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts)・[Git 履歴](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | 閲覧時の公式文書 | 2026-11-24 | Web | 文書参照 | 公開処理の直列化、artifact の期限、履歴残存を運用案に反映 |
| S94 | GitHub | プラン価格、Actions 上限・トークン仕様 | [プラン価格](https://github.com/pricing)・[Actions limits](https://docs.github.com/en/actions/reference/limits)・[GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) | 閲覧時の公式文書 | 2026-11-24 | Web | 文書参照 | R-17 で月次費用・ジョブ時間・後続トリガーの条件を確認 |
| S95 | e-Stat | 2026年1月1日現在の市区町村数 | <https://www.e-stat.go.jp/municipalities/number-of-municipalities?day=1&file_format=csv&form_id=city_count_form&month=1&year=2026> | 2026-01-01基準 | 2026-11-24 | Web | 件数の参照 | R-17 で市町村計・特別区・行政区数を容量試算に使用 |
| S96 | Astro・Vite・Microsoft（Playwright） | 静的配信・ブラウザの公式仕様 | [Astro](https://docs.astro.build/en/guides/deploy/github/)・[Vite](https://vite.dev/guide/static-deploy.html)・[Playwright](https://playwright.dev/docs/browsers) | 閲覧時の公式文書 | 2026-11-24 | Web | 文書参照 | Pages の base 設定を比較。Chrome でローカル Playwright を実行 |
| S97 | Cloudflare | Pages の上限と Direct Upload | [上限](https://developers.cloudflare.com/pages/platform/limits/)・[Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) | 2026-11-19／2026-04-21 更新表示 | 2026-11-24 | Web | Free のファイル数とファイルサイズに上限 | R-18 で静的配信の無料代替として文書確認 |

学校情報等検索 API のベース URL 候補は <https://opendata.jssh.site/siss/resources/>。現行仕様で照合する。Tableau の S01 掲載 URL は [R-01 の一覧](findings/R-01-public-views.md#公開ビュー-url-一覧)を参照する。

[R-15 の共通モデル案の根拠](findings/R-15-data-model.md#一次情報から確認した定義)は、定点と訂正の S50・S52・S56、週次・累計と休業指標の S58・S59、地域範囲の S22・S62。資料の適用範囲は各台帳行に従う。

[R-16 の少量再取得](findings/R-16-collection-operations.md#少量の再取得と変更判定)では S51 の CSV と S59 を照合した。利用条件は S52・S53・S60・S61、公表・訂正の根拠は S50・S51・S55〜S59 を参照。
