# Pages・Actions の構成候補

[R-17 の調査結果](../findings/R-17-pages-architecture.md)と[取得・復旧の運用案](../operations/collection-and-recovery.md)を参照。ここで示す構成は調査段階の候補。

## 無料枠での運用設計

- 公開は GitHub Free の Pages と標準の `github.io` アドレスを使い、取得・正規化・生成・配布は公開リポジトリの標準 GitHub-hosted runner で行う。MVP の維持に有料プラン、独自ドメイン、外部ストレージを必要とする構成は対象外とする。[Pages の利用条件と上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)・[Pages の標準 URL](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)・[Actions の課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- 公開可能な都道府県の週次集計を初期候補とする。R-17 の架空データで1年分の JSON は約45 MB。HTML・地図・索引を含めた公開一式の目安を500 MBとし、月間帯域は取得できる実績または配信量の試算で50 GBを目安に評価する。Pages の公式上限は公開サイト1 GB、帯域は月100 GBのソフト上限。容量が増えたら履歴期間、地域、データ形式を見直す。[R-17 の容量試算](../findings/R-17-pages-architecture.md#容量時間費用の試算)・[Pages の上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits#usage-limits)
- 公開可否と品質の検証後、配布内容に変更がある場合だけ新しい版を公開する。公開用 artifact は受け渡しに使い、保持は原則1日とする。GitHub Free の artifact 保管枠は500 MBで GitHub Packages と共有されるため、公開サイトのサイズとは別に、アーカイブの容量・保持時間と共有枠の利用を見積もる。課金設定の確認は公開準備時に行い、従量課金の停止設定が使える範囲を確認する。[Actions の保管枠](https://docs.github.com/en/billing/concepts/product-billing/github-actions#included-compute-usage-and-storage)・[Pages artifact の保持](https://github.com/actions/upload-pages-artifact#inputs-)・[GitHub の予算設定](https://docs.github.com/en/billing/how-tos/set-up-budgets)
- 容量や保管枠の超過が見込まれるときは、新しい版の公開を保留して最後の成功版を維持する。鮮度は画面に表示する。復旧用の版は、利用条件で許される範囲で、既存のローカル保管先など追加費用のない方法を R-19 で具体化する。

## ビルドから公開まで

1. 取得・正規化・品質検証・公開可否判定を行い、許可済みの集計のみから静的 HTML と JSON を生成する。ブラウザは公開成果物の JSON を読み込む。収集処理と提供元へのアクセスはビルド側で実行する。地図は簡略化した配布用データを使い、欠損を凡例と表でも示す。
2. 公式構成の `configure-pages` で本番のベースパスを取得する。公開専用ディレクトリを `upload-pages-artifact` に渡し、ファイル・ハッシュ・出典・権利・直リンクを検証する。成果物に調査文書、原本、内部ログ、秘密情報、シンボリックリンク、ハードリンクを含めない。
3. 同一ワークフロー内の依存ジョブとして `deploy-pages` を実行する構成を第一候補とする。公開ジョブだけに `pages: write` と `id-token: write` を付け、`github-pages` 環境のブランチ制約を適用する。取得・ビルド側は原則 `contents: read`。既定ブランチ、ワークフロー、公開条件の変更はレビュー対象にする。Action はフルコミット SHA または適用可能なワークフロー依存ロックで固定する。[カスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)・[GitHub の安全な利用](https://docs.github.com/en/actions/reference/security/secure-use)
4. 更新ジョブと手動再実行は同じ公開制御の対象とする。古いジョブの完了で新しい公開版を戻さないよう、直列化に加えて最新の公開版との比較を行う。構成を分離する場合は `workflow_call` または明示的な `workflow_dispatch` と検証済み成果物の受け渡しを検討する。対象リポジトリの `GITHUB_TOKEN` による push から通常の `push` ジョブが起動する構成は採用しない。[同時実行制御](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency)・[GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token)

計画上の例として、火曜18:17 JST は火曜09:17 UTC、金曜18:23 JST は金曜09:23 UTC。公式 `schedule` は UTC が既定で、IANA タイムゾーンの指定も可能。毎時00分付近を避け、提供元の公表予定・許容頻度を優先する。公式文書は混雑時の遅延・取りこぼし、公衆リポジトリで60日間活動がない場合の無効化、既定ブランチ上での実行を示している。最終確認時刻を監視し、無効化された場合は権限を持つ運用担当が再有効化を判断する。`workflow_dispatch` は対象資料・対象期間を確認した手動復旧に使う。例示はワークフロー設定に追加していない。[schedule の仕様](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## 静的生成の比較

| 構成 | 使う場合の設計 | 評価範囲 |
|---|---|---|
| 静的 HTML＋JS | 地域ごとに `index.html` を生成し、少量の JS でデータを遅延取得する。404、アセット、出典表示を明示的に整備 | 今回のローカル PoC で実行確認。地域・疾患ページが増える場合はテンプレートと共通要素の保守を評価 |
| Astro の静的生成 | 地域・疾患の静的ルートと共通コンポーネントを持ち、プロジェクトサイトでは `base` を設定する | GitHub Pages 用の公式手順を文書確認。ページ数が増える場合の有力候補。大規模ビルドの実測は未実施。[Astro の Pages 指南](https://docs.astro.build/en/guides/deploy/github/) |
| Vite＋静的 HTML | `base` を設定し、ビルド時に各地域 HTML を静的出力する構成。テンプレート生成は別途用意する。単一ページ構成は地域直リンクへの応答を確認する必要がある | Pages の公式手順を文書確認。Vite 側の比較ビルドは未実施。[Vite の静的配信](https://vite.dev/guide/static-deploy.html#github-pages) |

## 配布と復旧に使う保管先の比較

| 候補 | 利点 | 運用条件 |
|---|---|---|
| Git の小容量スナップショット | コードと対応する版の追跡がしやすい | 公開してよい小容量のデータに限定。履歴の肥大化と削除後の残存を考慮する。過去の配布版や原本の既定保管先には向かない |
| Actions artifact・cache | 同一ワークフロー内の受け渡しと依存の再利用 | 有効期限と共有容量あり。成功版を長期的に復元する保管先は別に持つ |
| アクセス制御・期限設定ができるオブジェクト保管 | 検証済みの原本・公開成功版を用途別に保持し、削除期限を管理できる | 提供元の条件、ストレージ料金、アクセス監査とリストアの試験が必要。製品・保管期間は未選定 |
| Pages の HTML・最新値と別の静的配信先の履歴 | ページ容量・帯域の予算を超える履歴を分離できる | 閲覧側はプロジェクトが管理する公開ファイルだけを読み込む。CORS、帯域・キャッシュ、費用、権利撤回時の配信停止を検証する |

全国向けには、ルート manifest に全履歴のパスとハッシュを列挙する方式の代わりに、地域・データセット単位の索引を候補とする。入口には版、提供元の鮮度、対応地域、索引への参照だけを置き、開いた地域に必要な索引と履歴を読み込む。PoC は少数地域の単一 manifest を実測し、索引分割の容量は別途試算した。#18・#19 では、提供可能な粒度、履歴期間、容量予算が揃った段階で採用判断を行う。

公開中に開かれたページが旧 manifest を保持したまま遅延読み込みする場合も考慮する。旧版の参照先を許可された期間だけ併載する案と、取得できないときにページの再読み込みを案内する案を、キャッシュ・保存予算とあわせて比較する。今回の旧版保持試験は候補版を公開しなかった場合の確認。
