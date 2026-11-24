# R-04 Tableau 集計 API と CSV 出力の検証

- GitHub Issue [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4)
- 調査日 2026-11-24 JST
- 状態 検証済み・完了承認待ち。CSV ファイル内容と対象ビューからの集計取得は未確認。
- 結論 Tableau の公式サンプル1件で、集計 API の先頭ページを取得し、数値2件が画面表示と一致した。公式 CSV の出力 API は正常終了した。

## 対象と実施条件

[R-03](R-03-tableau-embedding.md) のローカル埋め込み手順を使い、対象を [Tableau の公式出力例に掲載された Superstore サンプル](https://public.tableau.com/views/Superstore_embedded_800x800/Overview)の `Overview` ダッシュボードに限定した。S10 が同じ URL をクロス集計出力の実装例として提供しているため、その用途の実行確認に用いた。出力ファイルやワークブックはリポジトリに含めない。

[R-02](R-02-reuse-terms.md#技術検証で許容する範囲) のとおり、日本学校保健会の代表ビューは公開メニューに CSV・データが表示されず、適用条件と取得経路も未確定。今回の検証では同会のビューを開かず、データ API や出力を試していない。

公式サンプル1ビュー、同時実行1、`Total Sales` ワークシートを対象とし、集計の呼び出しは先頭1ページ・最大2行。CSV は集計総行数が1〜12行のワークシートで1回だけ試す。対象や表示条件を変えず、元データ取得、全ページ取得、無人実行は行わない。

## 一次情報

確認日は 2026-11-24 JST。版と URL は[一次情報台帳](../source-register.md)を参照。

| ID | 該当箇所 | 確認事項 |
|---|---|---|
| S08・S11 | 対象ビューの掲載プロフィール、Authentication and Embedding | 日本学校保健会の公開表示とデータ取得条件の切り分け。Public の表示は通常認証不要 |
| S09・S48 | Get summary data from a worksheet、`Worksheet.getSummaryDataReaderAsync()` | ページサイズの指定、集計データ、列配列の順序に関する注意 |
| S47・S49 | DataTableReader、DataTable | `pageCount`、`totalRowCount`、`getPageAsync()`、`releaseAsync()`、`columns`、`data` |
| S10 | Export crosstab (CSV, Excel) | 公式サンプルの URL、シート指定、`CrosstabFileFormat.CSV` |
| S45 | Tableau Public 配信モジュール | Tableau Public と同じホストの v3 ライブラリを使用 |

## 再現手順と観測

[PoC の手順](../../poc/tableau/README.md#r-04-公式サンプルの集計と-csv-出力)を使用。2026-11-24 13:31〜13:52 JST、ChatGPT 内蔵ブラウザ、Python 3.13.5。PoC は `127.0.0.1:8030` で配信し、Tableau Public と匿名で接続。埋め込みの API 版表示は `3.17.0`。起動時のビューと集計・出力の間で初期フィルターを変更せず、ダッシュボードの選択アクションは実行しなかった。

| 項目 | 観測結果 |
|---|---|
| ビュー | `Superstore_embedded_800x800/Overview`。FirstInteractive を受信 |
| ワークシート | `Total Sales` |
| ページサイズ、ページ数、総行数 | 2、4、7（`DataTableReader` の値） |
| 実際に取得した範囲 | `getPageAsync(0)` の2行。読取後は `releaseAsync()` が完了 |
| API が報告した列と型 | `メジャー ネーム` が `string`、`メジャー バリュー` が `float` |
| CSV | `exportCrosstabAsync('Total Sales', CrosstabFileFormat.CSV)` の Promise が解決。保存ファイルの存在・中身はこの環境では確認できず |

### 集計 API と画面の照合

| 指標 | API の数値 | API の表示文字列 | ダッシュボードの表示 | 判定 |
|---|---:|---|---|---|
| Quantity | 37873 | 37,873.00 | 37,873 | 一致。桁区切り・小数桁の表示形式が異なる |
| Average Discount | 0.1562027216329931 | 0.16 | 16% | 一致。画面は割合を百分率に換算し整数に丸めている |

先頭ページでの行順は Quantity、Average Discount で、画面の指標ラベルの並びと異なる。行番号で比較せず表示ラベルで対応付けた。メジャー名の `value` は Tableau の識別子形式、`formattedValue` は表示ラベルだった。CSV はクロス集計であり、API の行・列の順序や形状と同じかは未確認。

### CSV の確認範囲

最初のブラウザ自動操作はダウンロード待ちで停止し、再開時に出力ボタンが有効なままで、出力処理が始まっていないことを確認した。同じセッションでボタンを手動操作し、API がエラーなく完了する表示を確認した。保存先の読み取りは実行環境で `Operation not permitted` となり、CSV の内容・ヘッダー・件数は照合できなかった。再検証では、ダウンロードを利用できるブラウザで保存ファイルを開き、`Quantity` と `Average Discount` をラベルで突合する。

## 受入基準と後続

- [x] 公式サンプルでページ数、総行数、先頭2行、列名・型、公式 CSV 出力 API の結果を記録した。
- [x] 同じ表示条件で集計 API の2値を画面と照合した。
- [x] 一次情報、実施範囲、CSV 実ファイルと日本学校保健会の集計が未確認である理由を記録した。
- [ ] CSV 実ファイルと画面・API の値を照合する。

日本学校保健会の実データに依存する R-05〜R-07 で、本件の列名、値、出力可否は前提にできない。対象データの取得条件が確認できるまで、公式資料と画面上で確認できる範囲を使い、取得の必要な項目は保留する。
