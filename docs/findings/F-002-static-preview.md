# F-002　地域・疾患ページと分割 JSON

対象は [Issue #22](https://github.com/Olein-jp/japan-infection-watch/issues/22)。2026-11-25（JST）。[画面仕様](../specifications/mvp.md#画面と静的-url)、[公開アーキテクチャ](../architecture/mvp-publication.md)、[F-001 の正規化](F-001-jihs-normalization.md)に基づく。

- 全国、47都道府県、19疾患のページと、岐阜市の公式案内、出典、404を生成する。基準パスは `/japan-infection-watch/` と `/` を検証した。岐阜市ページでは、都道府県単位の集計や市の公式案内へリンクし、市の数値表示は行わない。コード `21201` は [R-14 の対照表](R-14-master-joins.md)に基づく。[公式 IDWR（S15）](https://id-info.jihs.go.jp/surveillance/idwr/)・[岐阜市公式案内（S67）](https://www.city.gifu.lg.jp/kenko/kansensyou/1004450/1004453.html)
- 全国・都道府県・疾患の最新値は HTML に含める。都道府県ページを開くと、選択地域のインフルエンザの履歴を読み込み、詳細表より上に折れ線グラフを表示する。疾患や月の切り替え時は選択対象の履歴を取得する。全国値は入力の全国行を用いる。都道府県と全国は同じ対象週で表示し、報告件数と定点当たりを別列にする。原表ハイフン、空欄、数値ゼロを文字と数値で区別する。
- 各データページで対象期間、出典、速報形式、原表の作成日、取得日時（架空）、サイト生成日時を表示する。履歴も各週の版の来歴を表示し、推移の図と同じ内容の表を提供する。キーボードで本文と主要な操作に到達できる。履歴の取得に失敗したときは、最新の表と表示済みの履歴を保ち、エラーを通知する。
- manifest は版、範囲と鮮度、地域索引への参照を持つ。地域索引は最新・月別履歴のパス、サイズ、SHA-256 を持つ。当初の52報告週は、現在は最新掲載週の終了日を基準とする直近6暦月に変更した。履歴を開くと、収録期間全体または指定月の表と推移を表示する。週の競合は選定済みの入力を求める。出力は架空で公開対象外と明示し、実データや公開候補を含む入力を受け入れない。

## ローカルで表示

標準ライブラリの Python 3 で実行できる。新規の一時領域に2週分の架空 CSV を正規化してサイトを生成する。続いて Pages の基準パスと 404 を模擬する既存サーバーを起動する。

```sh
work=$(mktemp -d)
PYTHONPATH=tests python3 -B -m fixtures.build_web_preview "$work/site"
ln -s "$work/site" "$work/active"
python3 -B poc/pages/serve.py "$work"
```

サーバーが表示したループバック URL に `/japan-infection-watch/` を付けて開く。ルート配置で試す場合は、別の一時領域で生成とサーバーの両方に `--base /` を指定する。F-001 が出力済みの架空観測 JSON を使う場合は `python3 -B -m apps.web.build input.json --output /path/to/new-directory`。複数週は1週につき1ファイルを渡す。

## 検証結果

当初は Python 3.13.5、Node.js 20.19.2、Playwright 1.58.2、Chrome 158.0.8127.37 で計測した。2週分から HTML 70件、JSON 2,785件、CSS・JS 2件を生成し、合計3,357,504バイトだった。地域索引と全参照ファイルのサイズ・SHA-256・版の整合を自動テストで照合した。

画面の見直し後は、Chrome の幅320pxで、トップの検索、都道府県ページの初期表示、月別の読み込み、直リンク、再読込、404、キー操作、取得失敗時の表示を確認した。架空の27週分では幅390px・高さ900pxと幅1280pxで、選択地域・疾患の月別JSONだけを7件読み込み、折れ線がスクロール前の画面に収まった。期間内の欠損値・未収録週で線を分け、報告値ゼロは軸上に残すことも確認した。

```sh
python3 -B -m unittest discover -s tests
python3 -B -m unittest discover -s poc/data-model
deps=$(mktemp -d)
npm install --prefix "$deps" --ignore-scripts --no-audit --no-fund playwright@1.58.2
NODE_PATH="$deps/node_modules" node tests/check_web_preview.cjs
```

Python テストは計25件が通過。GitHub Actions による配布判定は #23、統合検証は #24、実公開の判断は #25 へ引き継ぐ。地図は地域境界の配布条件の確認後に検討する。
