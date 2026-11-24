# T-001　静的配信・アクセシビリティ・復旧の統合検証

対象は [Issue #24](https://github.com/Olein-jp/japan-infection-watch/issues/24)。2026-11-25（JST）。[F-002 の静的生成](F-002-static-preview.md)と [I-001 の配布前検証](I-001-preview-check.md)を、[公開前テスト・監査案](../operations/mvp-release.md#公開前テストと監査)に沿ってローカルで通し検証した。

| 受入条件 | 確認結果 |
|---|---|
| プロジェクトパスとルートでの静的配信 | `/japan-infection-watch/` と `/` の双方で、直接アクセス、末尾スラッシュへの転送、再読み込み、404 と戻りリンクを確認。表示時に履歴の JSON は取得せず、操作すると該当の地域・疾患・月の履歴を取得した。岐阜市のページは公式案内リンクを表示する。 |
| 狭い画面とキーボード、色に頼らない状態表示 | Chrome の幅320 CSS px で画面全体に横スクロールがなく、疾患別の最新表の列が収まった。Tab・Enter で本文への移動と履歴表示を確認した。強制配色モードで空欄・原表ハイフン・数値がテキストで区別でき、履歴取得失敗をテキストで通知しながら表示済みの表を維持した。 |
| 候補の拒否と保管版からの復旧 | 正常版2,857ファイルを保管。破損、容量超過、想定 SHA の不一致、変更なしの各候補で配信先は切り替わらず、manifest・地域索引・最新 JSON の版とハッシュを HTTP で確認した。検証済み修正版へ切り替えて架空値24→26を確認し、保管版のコピーを再検証して切り替え、同じ版・ハッシュと架空値24を確認した。 |

正常版の一式 SHA-256 は `5f7c843f19f88050b451f43642e3ccd370837fd2a578e76a57d2f1433b9714c8`。破損試験は最新 JSON のサイズを変えずに1バイトだけ変更。容量超過はテスト用の上限3バイトで模擬した。切り替えはローカル HTTP サーバーが参照するシンボリックリンクを原子的に置き換える試験用操作で、復旧時は保管ディレクトリから別のディレクトリへコピーした。

## 再現手順

リポジトリのルートで実行する。Python 3.13.5、Node.js 20.19.2、Playwright 1.58.2、Chrome 158.0.8127.37 を使用した。ブラウザ通信は試験用のループバックに限定した。

```sh
python3 -B -m unittest discover -s tests
python3 -B -m unittest discover -s poc/data-model
deps=$(mktemp -d)
npm install --prefix "$deps" --ignore-scripts --no-audit --no-fund playwright@1.58.2
NODE_PATH="$deps/node_modules" node tests/check_web_preview.cjs
```

Python テスト31件と、拡張した[ブラウザ統合試験](../../tests/check_web_preview.cjs)が通過。Chrome で確認した操作・表示の範囲は上表のとおり。スクリーンリーダー・実機の検証、GitHub-hosted runner と GitHub Pages 上での実配信・ロールバック、公開用の保持先と課金の確認は残る。実公開の判断は #25 に引き継ぐ。
