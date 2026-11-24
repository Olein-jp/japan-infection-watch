# 厚生労働省 PDF の PoC

[調査結果](../../docs/findings/R-10-mhlw-absence-pdf.md)にある厚労省の報告書をローカルで処理する。Python 3.12.14 と pdfplumber 0.11.9 で第10・11報を検証した。リポジトリのルートから実行する。

```sh
(
  set -eu
  workdir=$(mktemp -d)
  python3 -m venv "$workdir/venv"
  "$workdir/venv/bin/python" -m pip install -r poc/mhlw/requirements.txt
  url='https://www.mhlw.go.jp/content/001770872.pdf'
  curl --fail --silent --show-error --max-time 30 \
    --write-out 'HTTP %{http_code}\n' --output "$workdir/report.pdf" "$url"
  "$workdir/venv/bin/python" poc/mhlw/extract.py "$workdir/report.pdf" \
    --source-url "$url" > "$workdir/report.json"
  printf '%s\n' "$workdir/report.json"
)
```

第10報は [2026/2027 シーズン一覧](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/kenkou/kekkaku-kansenshou01/houdou_00025.html)の11月13日公開 PDF に URL を差し替える。検証済みの環境に pdfplumber があれば、その Python を直接使用できる。PDF と JSON は一時ディレクトリで扱う。

- 地域表は都道府県の報告区分・別掲市・掲載全国計を分け、週次と累計を原表の列どおり保持する。全国の当週の施設種別内訳を別に保持する。出典は PDF URL、SHA-256、発表日、報番号、対象期間、物理ページ番号で追跡する。
- 数値は整数で、明示的な0も `numeric`。脚注で計数不明とされる `…` は `unknown_count`、空欄は `blank` とし、いずれも値は `null`。初発年月日は都道府県・別掲市の原表に対応する。
- `checks` に地域別の合計と施設種別内訳の検査結果を残す。計数不明等で合計を検算できない項目は `incomplete`。未対応の表構造や確認できる計数同士の不一致では、終了コード2で停止して JSON を出力しない。
