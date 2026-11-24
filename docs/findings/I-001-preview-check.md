# I-001　Actions での静的プレビュー検証と配布準備

対象は [Issue #23](https://github.com/Olein-jp/japan-infection-watch/issues/23)。2026-11-25（JST）。[F-002 の静的生成](F-002-static-preview.md)に、[検証スクリプト](../../scripts/check_preview.py)と[検証ワークフロー](../../.github/workflows/preview-check.yml)を追加した。

## ワークフローと判定

- Pull Request と手動実行を入口とし、標準の Ubuntu runner でテストして架空の2週分を生成する。Pull Request はベース SHA を別にチェックアウトし、同じ生成手順が使える場合に比較元として用いる。手動実行と比較元に生成手順がまだない Pull Request は、差分を `no_baseline` として候補単体を検証する。同一の PR または参照の先行実行はキャンセルする。
- トークン権限は `contents: read`。checkout は公式リリースのフルコミット SHA に固定し、資格情報の保存を無効にする。サイトファイルは runner の一時領域に置き、結果の JSON だけをジョブの概要に表示する。artifact のアップロード、Pages の設定変更、定期取得、デプロイを行うジョブは置いていない。[ワークフロー構文](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)・[Actions の安全な利用](https://docs.github.com/en/actions/reference/security/secure-use)
- 既定の容量上限は展開後の500,000,000バイト。許可した HTML・CSS・JS・manifest とその参照先に範囲を限定し、リンク・隠しファイル・参照外のファイル、公開対象外の架空プレビュー表示がない一式を拒否する。地域索引と月別・最新 JSON のパス、サイズ、SHA-256、版、配布項目を検証する。
- 一式の実ファイルハッシュと、内容比較用ハッシュを個別に算出する。内容比較では配布版 ID、生成時刻と取得時刻、参照ファイルのサイズ・ハッシュを除く。観測、原本版、対象期間、出典の作成日、画面、基準パス、CSS・JS の差分は残る。変化があれば `changed`、同じ内容なら `unchanged` を返す。
- 破損、容量超過、想定 Git SHA の不一致、比較元より古い対象週は終了コード2。いずれの成功結果も `publication_allowed: false`。SHA の照合は候補を当該 CI イベントに対応付けるためのもの。デプロイを実装する段階では、公開直前にその時点の対象ブランチ・公開中の版・復旧時の明示理由を確認し、公開専用ジョブにのみ `pages: write`・`id-token: write` を付与する。[GitHub Pages の公開ジョブ](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages#deploying-github-pages-artifacts)

## ローカル再現

リポジトリのルートで実行する。Python 3.13.5 で実行確認済み。

```sh
work=$(mktemp -d)
PYTHONPATH=tests python3 -B -m fixtures.build_web_preview "$work/candidate"
PYTHONPATH=tests python3 -B -m fixtures.build_web_preview "$work/baseline"
python3 -B scripts/check_preview.py "$work/candidate" --baseline "$work/baseline"
python3 -B -m unittest discover -s tests
python3 -B -m unittest discover -s poc/data-model
```

一式は2,857ファイル、3,357,504バイト。ワークフローのビルド・検証シェルをローカルで再現し、手動相当は `no_baseline`、同内容を比較する Pull Request 相当は `unchanged` を確認。Python テスト31件が通過し、ワークフローは actionlint 1.7.12 の検査に合格した。テストでは実ファイルと内容用のハッシュの区別、画面アセットや観測の差分、同じサイズの破損、範囲外、容量超過、リンク、未許諾入力、古い SHA・対象週を確認した。

GitHub-hosted runner 上の実行は未確認。ローカルで検証した配布判定と失敗時の手順を #24 の統合検証に引き継ぐ。実運用の公開承認・課金の確認は #25 で扱う。
