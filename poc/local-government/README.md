# 岐阜県の週報と Excel の照合

[R-11 の調査結果](../../docs/findings/R-11-gifu-region.md)にある資料のうち、2026年第46週のデータ・グラフ編 PDF と、当時公開されたインフルエンザの旧 Excel 形式をローカルで照合する。Python 3.12.14、pdfplumber 0.11.9、xlrd 2.0.2 で確認した。

[週報一覧](https://www.pref.gifu.lg.jp/page/107799.html)の2026年第46週および[発生動向調査データ](https://www.pref.gifu.lg.jp/page/9553.html)の ARI 定点から配布元を確認できる。下記は当時の版の URL。県側で差し替え・削除される場合がある。

```sh
(
  set -eu
  workdir=$(mktemp -d)
  python3 -m venv "$workdir/venv"
  "$workdir/venv/bin/python" -m pip install -r poc/local-government/requirements.txt
  curl -fsS --max-time 25 -w 'HTTP %{http_code}\n' -o "$workdir/week46.pdf" \
    'https://www.pref.gifu.lg.jp/uploaded/attachment/524050.pdf'
  curl -fsS --max-time 25 -w 'HTTP %{http_code}\n' -o "$workdir/influenza.xls" \
    'https://www.pref.gifu.lg.jp/uploaded/attachment/523690.xls'
  "$workdir/venv/bin/python" poc/local-government/verify_gifu.py \
    "$workdir/week46.pdf" "$workdir/influenza.xls"
)
```

県計・8保健所の列が一致することを確認した後、報告数の地域計、定点当たり報告数、最新週の定点数による率の検算を行う。成功時は確認した件数を表示する。対象外の書式、空欄・記号、数値の不一致は終了コード2で停止する。原表の記号は人が確認し、ゼロ補完や市町村への按分は行わない。
