# R-03 Tableau Embedding API v3 による公開ビューの表示

- GitHub Issue [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3)
- 調査日 2026-11-24 JST
- 状態 検証済み・完了承認待ち
- 結論 市区町村別学級閉鎖地図1件を匿名でローカルに埋め込み、`FirstInteractive`、公開シート2件、フィルター名4件を確認した。

## 対象と実施条件

[R-01 の掲載ビュー](R-01-public-views.md)と [R-02 の許容範囲](R-02-reuse-terms.md#技術検証で許容する範囲)に従い、インフルエンザの市区町村別学級閉鎖地図を検証した。依存 Issue は GitHub 上で完了承認待ちだが、両調査の成果物で確認できた公式入口と表示検証範囲を使った。

実行は1ビュー、1セッション、同時実行1。集計値の読取・ダウンロード、元データへのアクセス、フィルターの変更操作、公開環境への配置は対象外。API からはシート名・種別とフィルター名を記録した。

## URL の根拠

- 公式案内の[インフルエンザ・市区町村別の学級閉鎖地図](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=3)を開き、ビュー内の「共有」を確認した。ダイアログのリンクは Tableau Public の `/shared/` 形式。埋め込みコードは共有パスと疾患区分 `3` を指定し、ローダーには `viz_v1.js` を使っていた。
- v3 では S38 の「Add the tableau-viz component」と「Use JavaScript to initialize」にある `/views/<workbook>/<view>` 形式を使用した。ワークブックとビューのパスは同じ公開ページに描画されたビューの URL と一致し、初期フィルターは公式案内の区分 `3` を引き継いだ。使用した[埋め込み URL](https://public.tableau.com/views/__16470709141460/1?疾患・症状の区分=3)で同じ地図が表示された。画面が発行した一時的な共有パスやローダー引数は正規 URL に含めていない。

## 一次情報

確認日はすべて 2026-11-24 JST。S 番号は[一次情報台帳](../source-register.md)に対応する。

| ID | 参照箇所 | 確認事項 |
|---|---|---|
| S01・S08 | 日本学校保健会の公開マップ案内、Tableau Public の掲載ページと共有ダイアログ | 対象ビューと初期フィルター、共有形式 |
| S11・S38 | `Authentication and Embedding`、`Basic Embedding` | Tableau Public の匿名表示、v3 の表示 URL と初期化方法 |
| S42 | `Add Event Listeners` | `FirstInteractive` の購読 |
| S43 | `Get filters` | `Dashboard.getFiltersAsync()` の取得範囲 |
| S44 | `activeSheet`、`publishedSheetsInfo` | 現在のダッシュボードと公開シート一覧 |
| S45・S46 | Tableau Public 配信モジュールの先頭の版注記、`Accessing the library on Tableau` | 同じ配信元からライブラリを読み込む方法と観測時の版 |

## 実行環境と再現手順

- 2026-11-24 13:26 頃 JST。ChatGPT 内蔵ブラウザ（User-Agent 表記 `Chrome/157.0.0.0`）、Python 3.13.5。
- [PoC の手順](../../poc/tableau/README.md)に沿い、`python3 -m http.server 8030 --bind 127.0.0.1 --directory poc/tableau` で起動した。ローカルの HTML と JavaScript を読み込んだ後、起動ボタンを1回押して表示と API の結果を照合した。
- Tableau Public の公式 `tableau.embedding.3.latest.min.js` は HTTP 200。取得時のライセンス注記は `3.17.0-pre.14`、ブラウザの埋め込みコンポーネント上の API 版表記は `3.17.0`。PoC は同じ配信元の互換版をロードする方式で、再実行時に配信版が変わる可能性がある。
- 初回のローカルサーバー起動は実行環境のポート制限で `PermissionError: [Errno 1] Operation not permitted`。ループバックへのバインドを許可した環境で起動でき、Tableau 側の初期化エラーは発生しなかった。

## ブラウザで確認した結果

| 項目 | 結果 |
|---|---|
| 描画 | 市区町村別の学級閉鎖地図を表示。画面表記の対象日は 2026-11-23、元データ時点は 2026-11-24 11時 |
| 初期化 | 匿名のまま `FirstInteractive` を受信。認証要求、読み込みエラー、タイムアウトは発生せず |
| アクティブシート | ダッシュボード 1（`dashboard`） |
| 公開シート | ダッシュボード 1、シート 2 |
| ダッシュボード内のワークシート | シート 2 |
| フィルター名 | 疾患・症状の区分、疾患名、都道府県区分、都道府県 |

画面には「日付」のページコントロールもあるが、今回のダッシュボードの `getFiltersAsync()` の返却一覧には含まれなかった。日付を指定できる範囲と操作方法は R-07 で確認する。上のフィルター一覧はダッシュボードでの観測で、別ビューや別シートの全フィールドを表すものではない。

## 判定と後続

- [x] 公式共有と表示を照合し、v3 で動く埋め込み URL を記録した。
- [x] ブラウザでの描画、`FirstInteractive`、公開シートとフィルター名を確認した。
- [x] 確認日、公式資料、再現手順、版、起動時のエラーと対処を記録した。

R-04 での集計 API・CSV は [R-02 の取得条件](R-02-reuse-terms.md#技術検証で許容する範囲)に従う。実データは対象ビューと公式経路の条件が確認できるまで取得保留。架空データや利用許可を確認したサンプルでの検証は切り分けられる。
