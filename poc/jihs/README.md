# JIHS CSV の PoC

[R-09 の調査結果](../../docs/findings/R-09-jihs-csv.md)を再現するためのローカル PoC。Python 3.11 以上の標準ライブラリで、速報の週次定点 CSV を1ファイルずつ縦持ち JSON に変換する。検証環境は Python 3.13.5。

## 再現手順

[IDWR 速報データの年別一覧](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/index.html)から対象週を開き、「定点把握疾患（週報告）、報告数、定点当たり報告数、都道府県別」の CSV リンクを確認する。リポジトリのルートで、確認したリンクを使って実行する。第46週を試す場合は、同週のページでリンクを確認してから `week` と `url` を差し替える。

```sh
(
  set -e
  week=45
  url='https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/45/2026-45-teiten.csv'
  workdir=$(mktemp -d)
  curl --fail --silent --show-error --max-time 30 \
    --output "$workdir/2026-$week-teiten.csv" --write-out 'HTTP %{http_code}\n' "$url"
  retrieved_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  python3 poc/jihs/normalize.py "$workdir/2026-$week-teiten.csv" \
    --source-url "$url" --retrieved-at "$retrieved_at" > "$workdir/2026-$week.json"
  printf '%s\n' "$workdir/2026-$week.json"
)
```

## 出力と検証

- 1レコードは1地域・1疾患・1週。ファイル共通項目に対象期間、原本 URL、作成日、取得日時、SHA-256、速報の区分を保持する。地域と疾患は公式のラベルを保持する。
- 報告数は整数、定点当たり報告数は表示精度を保つ小数文字列。各指標は `value` と `status` を持つ。数値ゼロは `numeric`、ハイフンは `dash`、空欄は `blank` とし、後二者の値は `null`。
- 週番号・期間・配布 URL、列構成、見出し、地域の重複・欠落、値の形式を検査する。対応外の入力では終了コード2で停止する。実データと変換結果は一時ディレクトリで扱う。
