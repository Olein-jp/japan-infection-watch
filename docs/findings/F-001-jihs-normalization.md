# F-001　架空の JIHS 週次 CSV の正規化

対象は [Issue #21](https://github.com/Olein-jp/japan-infection-watch/issues/21)。2026-11-25（JST）。[D-001](../specifications/mvp-inputs.md)、[R-09 の形式・データ辞書](R-09-jihs-csv.md#形式データ辞書)、[R-15 の共通観測モデル](../schemas/observations.md)に基づき、架空入力の実装と検証を完了した。実データの取り扱いは [R-16](R-16-collection-operations.md#利用条件の判断)の確認と別途承認を要する。

- [週次 CSV のパーサー](../../packages/data_normalizer/jihs_csv.py)を既存の R-09 PoC と共有し、[架空入力の変換コマンド](../../packages/data_normalizer/jihs_weekly.py)で全国・47都道府県の週次観測を生成する。都道府県コードは R-12 のコード順と照合し、元の報告週・期間、作成日、取得日時、原本 SHA-256、速報の区分を版の情報に持たせた。再取得時刻だけが変わっても版 ID は同じ。原本が変わった場合は別版になり、訂正関係は推定しない。
- 報告件数と定点当たりを別の観測行にし、値の型・単位、元のセル文字列を保持する。ハイフンと空欄は別の状態で値は null。定点数は未提供として保持する。列数、指標・疾患の見出し、地域の重複・欠落、週の番号と期間、不正な値を検査する。[観測と原本版の共通検証](../../packages/data_model/observations.py)で、出力が R-15 の行と版の構造に合うことを確認する。
- CLI では架空入力であることを `--fixture` で明示する。有効な入力でも `fictional: true`、版は `publication_status: blocked`、`public_candidates` は空。標準出力の `observations` はローカル開発・検証に使う。実データの受け入れや公開判定の解除を行う入口は今回の対象外。形式が合わない場合は終了コード2で停止し、観測を出力しない。

## 再現と検証結果

Python 3.13.5（標準ライブラリ）。テストは架空値の Shift_JIS CSV を生成する。R-09 で確認した全国と47都道府県、19疾患の表に相当し、1回の正規化で1,824観測となる。実データの取得・保存・公開は未実施。

```sh
python3 -B -m unittest discover -s tests -p test_jihs_normalizer.py -v
python3 -B -m unittest discover -s poc/data-model
```

新規7件、既存15件が通過。調査用 CLI は同じ架空入力で変更前と出力がバイト単位で一致した。R-17 のローカル静的ビルドも共有検証コードで成功し、12ファイルと manifest を生成した。

架空 CSV を手元で変換する場合は、リポジトリのルートから実行する。

```sh
python3 -B -m packages.data_normalizer.jihs_weekly /path/to/fictional-weekly.csv \
  --fixture --retrieved-at 2030-01-16T09:00:00+09:00
```

#21 の受入条件は架空入力で検証し、2026-11-25（JST）に完了した。次の F-002 はこの観測を使って画面と分割 JSON を作る。
