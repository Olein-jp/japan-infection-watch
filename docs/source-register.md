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
| S15 | JIHS | JIHS IDWR | <https://id-info.jihs.go.jp/surveillance/idwr/> | — | — | Web | 未確認 | 未検証 |
| S16 | 厚生労働省 | 厚労省 令和8年度急性呼吸器感染症対策 | <https://www.mhlw.go.jp/stf/index2026.html> | — | — | Web | 未確認 | 未検証 |
| S17 | 岐阜県 | 岐阜県感染症情報センター | <https://www.pref.gifu.lg.jp/page/9550.html> | — | — | Web | 未確認 | 未検証 |
| S18 | 岐阜県 | 岐阜県週報 | <https://www.pref.gifu.lg.jp/page/107799.html> | — | — | Web | 未確認 | 未検証 |
| S19 | 岐阜県 | 岐阜県発生動向データ | <https://www.pref.gifu.lg.jp/page/9553.html> | — | — | Web | 未確認 | 未検証 |
| S20 | 総務省 | 総務省 全国地方公共団体コード | <https://www.soumu.go.jp/denshijiti/code.html> | — | — | Web | 未確認 | 未検証 |
| S21 | 文部科学省 | 文科省 学校コード | <https://www.mext.go.jp/b_menu/toukei/mext_01087.html> | — | — | Web | 未確認 | 未検証 |
| S22 | 国土交通省 | 国交省 行政区域 | <https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html> | — | — | Web | 未確認 | 未検証 |
| S23 | 神戸市（要確認） | 神戸市 学級閉鎖情報候補 | <https://kobecity-kmss.jp/classclosure> | — | — | Web | 未確認 | 未検証 |
| S24 | 北九州市 | 北九州市 学級閉鎖情報候補 | <https://www.city.kitakyushu.lg.jp/contents/334_00031.html> | — | — | Web | 未確認 | 未検証 |
| S25 | 東京都 | 東京都オープンデータAPIカタログ | <https://spec.api.metro.tokyo.lg.jp/> | — | — | Web | 未確認 | 未検証 |
| S26 | GitHub | GitHub Pages 制限 | <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits> | — | — | Web | 未確認 | 未検証 |
| S27 | GitHub | GitHub Pages カスタムワークフロー | <https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages> | — | — | Web | 未確認 | 未検証 |
| S28 | GitHub | GitHub Pages 公開元の設定 | <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site> | — | — | Web | 未確認 | 未検証 |
| S29 | GitHub | GitHub Actions イベント・schedule | <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows> | — | — | Web | 未確認 | 未検証 |
| S30 | GitHub | GitHub Actions 課金 | <https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions> | — | — | Web | 未確認 | 未検証 |
| S31 | GitHub | GitHub 追加製品利用条件 | <https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features> | — | — | Web | 未確認 | 未検証 |
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

学校情報等検索 API のベース URL 候補は <https://opendata.jssh.site/siss/resources/>。現行仕様で照合する。Tableau の S01 掲載 URL は [R-01 の一覧](findings/R-01-public-views.md#公開ビュー-url-一覧)を参照する。
