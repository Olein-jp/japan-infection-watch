# 初期版の更新・復旧・公開判定案

対象は[初期版仕様](../specifications/mvp.md)と[公開アーキテクチャ](../architecture/mvp-publication.md)。取得の詳細は [R-16 の運用案](collection-and-recovery.md)。下記の運用は開発・公開と各操作の承認後に適用する。確認済みの範囲と初回公開までの残件は [O-001 の公開判定](../findings/O-001-release-readiness.md)を参照。

公開先は GitHub Pages。Pages の公開元は GitHub Actions を使い、このリポジトリの既定ブランチから手動で公開ワークフローを起動する。公開前検証を通過した静的成果物一式を `github-pages` 環境に配布する。[GitHub Pages のワークフロー](https://docs.github.com/ja/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

## 手動更新と復旧

1. 担当者が公式の掲載予定と対象号を確認し、提供元ごとに承認された公式経路から、許容された回数だけ取得する。初期は手動で入力を用意し、既定ブランチから対象号と承認済み入力を指定して実行する。公開 Git へ保持できると判定した小容量の正規化済み入力に限り、レビュー済みリビジョンを渡せる。永続公開が許されない資料は Git に入れず、承認済みの取得・受け渡し経路が揃うまで数値公開を保留する。
2. 提供元ごとに同時取得1、接続5秒・全体20秒を初期候補とし、公式条件を優先する。タイムアウト・一時的5xxの再試行は許容回数内で間隔を置いて最大1回。401・403・429・CAPTCHA は対象の取得を止めて再試行しない。404、HTML への変化、列変更、合計不一致、期間ずれ、予期しない欠損は原因を確認してから再開する。
3. 取得・検証・公開判定が通らない場合は、公開継続が許可された最後の成功版を維持する。先行版がなければ掲載できる公式案内を表示し、未確認を値で補わない。初期運用は一式の更新を原則とする。独立した系列の部分更新は、旧版の使用許可、系列別の鮮度、参照の整合を検証できる場合に限り後続で検討する。
4. GitHub Actions の実行結果と担当者が利用できる通知で、工程・対象号・理由・現在の公開版と次の対応を記録する。稼働時は公式発表予定の経過と最終成功日時を照合する。閲覧画面には公開版で分かる最新の状態を表示し、公開できなかった取得試行の時刻は管理用記録に残す。
5. デプロイ失敗や応答不明時は、後続のデプロイを止めて公開 URL の manifest・主要 JSON・代表ページを確認する。不整合時は公開可能な検証済み成功版一式を再生成または再投入し、版・ハッシュ・URL を確認する。現行と直前2版を保持候補とし、許可された配布版を担当者の既存保管先に置く案を優先する。Git に保存が認められた入力・コードから再現する場合は、版と依存を固定する。原本は許可された保存先・期間だけ保持する。復旧用の入力経路と所要時間を実地確認し、期限付き artifact が消えても復旧できることを公開前に確認する。
6. 権利条件や個別の掲載許可が撤回された時は、対象を公開・復旧候補から外す。必要に応じて公開停止を判断し、削除後に配布ファイル、過去版、ログ、保存先、キャッシュと Git 履歴を点検する。もし Git に保存した場合は過去のコミット等にも残る前提で判断する。

定期取得を承認した場合は、提供元の公表日と許容頻度を登録し、既定ブランチの schedule に追加する。JST 基準で、例えば火曜18:17 JSTは火曜09:17 UTC。提供元の承認前に時刻を確定しない。毎時00分付近を避け、混雑時の遅延や取りこぼし、公開リポジトリで60日活動がない場合の無効化を想定する。停止や遅延の確認には手動起点を残す。[GitHub の schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## 月0円と公開上限

| 項目 | 運用の目安と超過時の扱い |
|---|---|
| 費用 | 公開リポジトリの GitHub Free、標準 runner、`github.io`。公開前にアカウントの課金・共有利用の実態と停止設定の効力を確認する。従量課金を止められる設定は適用範囲を確認し、必要な承認を得る。有料プラン、独自ドメイン、外部ストレージ料金に依存する構成は初期対象外。 |
| デプロイ前に測れる項目 | 展開後の配布一式は500 MBを管理上限案とし、境界を超えた候補の公開を止める。公式の公開サイト上限は1 GB。tar のサイズと保管実績を別に見る。公開用 artifact は原則1日で、GitHub Free の500 MBは Packages と共有。残枠と保持時間から超過を見込む場合はアップロードを保留する。 |
| 実績で評価する項目 | デプロイ5分、月間帯域50 GBを管理目安とする。公式条件はデプロイ10分、帯域100 GB/月のソフト上限。配信データ量・閲覧実績または想定回数を確認する。帯域は推計であり、更新を止めても公開中のページの転送は続く。予測や実績で逼迫した場合は履歴期間・地図・対象を縮め、必要なら公開範囲を再判断する。 |
| 代替 | GitHub Pages の条件を満たせないときは、公式案内への縮小か、無料枠に収まる静的成果物による Cloudflare Pages を再評価する。公開先の変更と実デプロイは別途判断する。 |

[無料枠での運用設計](../architecture/pages-layout.md#無料枠での運用設計)・[R-18 の成立条件](../findings/R-18-feasibility.md#月0円での成立条件)・[GitHub Actions 課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)・[GitHub 予算設定](https://docs.github.com/en/billing/how-tos/set-up-budgets)

## 公開前テストと監査

| 確認 | 合格条件 |
|---|---|
| データ変換と公開可否 | 架空データでゼロ、ハイフン、欠損、秘匿、重複、同一原本、訂正版、禁止資料を確認する。承認済みの少量データでは原表の地域・期間・指標・値を照合する。 |
| 配信と画面 | 正常、欠損、更新遅延、未掲載の地域、分割履歴の取得失敗を試す。直接アクセス・再読込、404、基準パス、320 CSS px 相当の幅で主要操作、キーボードと凡例・表で内容が確認できる。地図やグラフに代替テキスト・表がある。 |
| 出典と加工表示 | JIHS 数値版では、収録した週の公式速報ページへのリンクと、本サイトによる独自の編集・加工の表示を別に確認できる。配布する描画用 JSON の項目、出典と加工の表示方法、各週の掲載注記を確認する。[JIHS の回答と表示例](../findings/O-001-release-readiness.md#jihs-の回答と数値版への反映) |
| 週次履歴 | 最新週の終了日から6暦月の境界を算出でき、月末・年またぎで境界当日以降の報告週だけが成果物に含まれる。収録期間が短い場合は実際の期間を表示し、6か月より前は JIHS の年別一覧へ案内する。 |
| 更新・障害時 | 変更なし、容量超過、検証失敗、デプロイ結果不明、競合、明示的なロールバックを試す。検証済みの版だけを配布し、失敗時に旧版の値が維持される。権利撤回されたデータは旧版維持の対象から外す。 |
| 公開可否と監査 | Git 全履歴、Issue とコメント、Actions ログと artifact、公開成果物を点検する。許可した集計だけが配布対象で、秘密情報・原本・非公開資料・再配布不可データがない。最小権限、対象ブランチ、アカウント課金、復旧担当・復旧入力の取得を確認し、依頼者の公開承認を記録する。 |

テストは架空データを基本とし、開発中の CI で実デプロイや提供元の定期取得を起動しない。ローカル結果と GitHub 上での結果は分けて記録する。架空版の切り替え・復旧を含むローカルの試験は [T-001 の統合検証](../findings/T-001-integrated-preview.md)を参照。

## JIHS 数値版のローカル検証

初回公開候補は2026年第45・46週。検証と公開前監査は、[初回の収録範囲と JSON の配布条件](../findings/O-001-release-readiness.md#初回数値版の収録範囲と-json-の配布条件)に照らして行う。確認済みの2週の CSV を使い、Git 管理外の一時ディレクトリへ検証用一式を生成する。同じ手順で、対象を確認した更新候補と保管版を比較できる。

```sh
work=$(mktemp -d)
python3 -B -m apps.web.local artifacts/jihs-local/2026-45-teiten.csv \
  artifacts/jihs-local/2026-46-teiten.csv --output "$work/site"
python3 -B -m scripts.check_preview "$work/site" --local-jihs
```

保管版があれば `--baseline` でそのディレクトリを指定する。失敗、古い候補、変更なしの場合は現行版を維持する。復旧時は保管した一式の別コピーを検証し、正常版の SHA-256 と照合する。この検証は常に `publication_allowed: false` を返す。数値版の本番配布では、承認された入力と検証済み成果物を受け渡す方法を決め、公開後に同じ版の代表ページと JSON を照合する。

## 初回数値版の公開候補

第45・46週の照合済み CSV を使い、本番と同じ `/japan-infection-watch/` 配下のパスで生成する。生成スクリプトは週と原本の SHA-256 が登録済みの2ファイルに一致することを確認する。候補の manifest は `pending_review`、検証結果は `publication_allowed: false`。公開判定には下記の成果物と別途の承認を使う。

```sh
work=$(mktemp -d)
initial_inputs=artifacts/jihs-release-archive/candidate-62aa14d1881e5f334818/jihs-reviewed-inputs.json
python3 -B -m scripts.build_release_candidate \
  artifacts/jihs-local/2026-45-teiten.csv artifacts/jihs-local/2026-46-teiten.csv \
  --reviewed-inputs "$initial_inputs" \
  --generated-at 2026-11-26T11:02:41+09:00 --output "$work/site"
python3 -B -m scripts.check_preview "$work/site" --release-candidate
```

### 直近6か月の配布候補を再現

第20〜44週は一度取得した `artifacts/jihs-local/2026-w20-w44/` の原本を使い、第45・46週を合わせる。[照合済み原本の一覧](../../config/jihs-reviewed-inputs.json)と一致する入力で、承認前の候補をローカルに再現できる。取得時の記録は同じディレクトリの `attempts.jsonl`。

```sh
work=$(mktemp -d)
python3 -B -m scripts.build_release_candidate \
  artifacts/jihs-local/2026-w20-w44/2026-*-teiten.csv \
  artifacts/jihs-local/2026-45-teiten.csv artifacts/jihs-local/2026-46-teiten.csv \
  --generated-at 2026-11-26T15:11:26+09:00 --output "$work/site"
python3 -B -m scripts.check_preview "$work/site" --release-candidate \
  --expected-sha256 19f386a5c4481dd3bc28138a0def12a847d3ce1a3e21e34b108bd43c75fdae10
```

### Actions での候補の受け渡し

[公開候補の検証ワークフロー](../../.github/workflows/check-jihs-candidate.yml)は、既定ブランチでの手動実行を受け付ける。入力は `source`、対象コミットの完全な SHA を示す `revision`、候補生成時の `generated_at`、候補一式の `expected_sha256`。値はローカルの候補検証結果に合わせる。チェックアウトしたコミットと候補一式のハッシュが両方一致した場合に、候補専用の artifact として1日間渡す。配布は[数値版の手動公開](#数値版の手動公開)で行う。[手動実行](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)・[候補の梱包に使う公式 action](https://github.com/actions/upload-pages-artifact/blob/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml)

1. 初回の Actions 試験は `source=fixture` を選ぶ。ローカルで `PYTHONPATH=tests python3 -B -m fixtures.build_web_preview "$work/fixture" --generated-at 2030-02-05T13:00:00+09:00` と `python3 -B -m scripts.check_preview "$work/fixture"` を実行し、同じ日時とハッシュを指定する。成功版の artifact を展開して再検証し、ハッシュを1桁変えた実行では artifact が作られないことを確認する。
2. `source=reviewed-jihs` の実行前に、実データの取得と公開リポジトリ上の artifact 共有の承認を記録し、共有枠・保持期間を確認する。リポジトリ変数 `JIHS_APPROVED_CANDIDATE_SHA256` に承認済みの候補ハッシュを設定した後、同じハッシュを実行時に指定する。設定が空、または入力が異なる場合は JIHS への通信前に停止する。照合後は、[確認済み入力の一覧](../../config/jihs-reviewed-inputs.json)に載る公式 CSV を runner の一時領域に順に各1回取得する。HTTP 200 以外や原本のハッシュ不一致で停止し、正常時は静的成果物のディレクトリだけを梱包する。[設定変数の仕様](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables)
3. 初回の復旧担当はリポジトリ所有者 `Olein-jp` とする。候補の圧縮版と検証記録は、担当者の Mac の Git 管理外にある `artifacts/jihs-release-archive/<版 ID>/` に保存する。初回分は `candidate-62aa14d1881e5f334818` ディレクトリに保管済み。初回の公開に失敗した場合の復旧先は Git 上の公式リンク先行版。Mac とは別の保管先と、原本が変更された場合に数値版の保管物を GitHub Actions へ渡す経路は、数値版の継続運用前に確定する。

ローカルの保管版を使って配布用一式を復元するときは、保管ディレクトリを `archive_dir` に指定し、下記を実行する。圧縮版の SHA-256 と生成前後のハッシュは `final-preflight.json` に保存している。

```sh
archive_dir=artifacts/jihs-release-archive/candidate-62aa14d1881e5f334818
work=$(mktemp -d)
archive_hash=$(jq -r .archive_sha256 "$archive_dir/final-preflight.json")
candidate_sha256=$(jq -r .candidate_sha256 "$archive_dir/final-preflight.json")
pages_sha256=$(jq -r .pages_sha256 "$archive_dir/final-preflight.json")
test "$(shasum -a 256 "$archive_dir/site.tar.gz" | awk '{print $1}')" = "$archive_hash" &&
  python3 -B -m tarfile --filter data -e "$archive_dir/site.tar.gz" "$work" &&
  (cd "$work/site" && python3 -B -m tarfile -c "$work/artifact.tar" .) &&
  python3 -B -m scripts.prepare_jihs_pages "$work/artifact.tar" --output "$work/pages" \
    --reviewed-inputs "$archive_dir/jihs-reviewed-inputs.json" \
    --candidate-sha256 "$candidate_sha256" --pages-sha256 "$pages_sha256"
```

### 数値版の手動公開

[数値版の公開ワークフロー](../../.github/workflows/publish-jihs.yml)は、候補を作成したのと同じ既定ブランチのコミットで手動実行する。配布承認時に、運用担当と復旧用の保管先、GitHub の共有枠、候補の利用条件と有効期限を確認する。候補の取得・共有の承認は、前節の手順で先に扱う。

1. 承認対象の候補を梱包した `artifact.tar` を用意する。下記のコマンドで最終配布版の SHA-256 を算出する。候補の出典・表示項目・対象週は再照合され、manifest の公開状態だけを `published` に更新したときのハッシュが返る。算出だけの場合は出力ディレクトリは作られない。

   ```sh
   python3 -B -m scripts.prepare_jihs_pages "$work/artifact.tar" \
     --output "$work/pages" --candidate-sha256 "$candidate_sha256"
   ```

2. 公開承認を記録し、リポジトリ変数 `JIHS_APPROVED_RELEASE` に1件の JSON オブジェクトを設定する。必須項目は候補検証の実行 ID を文字列で示す `run_id`、候補を作った完全なコミット SHA の `revision`、`weeks`、`candidate_sha256`、`pages_sha256`。`weeks` は確認済み入力の一覧にある全週を年月週の昇順に並べた配列とする。初回版なら `["2026-W45", "2026-W46"]`。承認内容が一致しなければ配布前に停止する。
3. `publish-jihs.yml` に `candidate_run_id` を指定して手動実行する。候補検証の同一リポジトリ・既定ブランチ・同一コミットの成功実行を照合し、`jihs-candidate-reviewed-jihs` だけを取得する。候補と Pages 配布版の両方のハッシュ、照合済みの全週の履歴が一致した場合に、配布ジョブへ進む。先行版の公開と同じ同時実行グループを使う。[実行メタデータの仕様](https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run)・[Pages の公開ジョブ](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
4. 公開結果の URL を開き、トップ、岐阜県、インフルエンザ、404 の画面と `data/manifest.json` を確認する。manifest の版・公開状態・参照ハッシュを承認済み配布版と比較し、岐阜県の索引から参照されるインフルエンザの最新・履歴 JSON を取得してハッシュと対象週を照合する。失敗時は公開中の版を確認し、復元が必要なら次節を使う。

## 公式リンク先行版の配布

先行版は JIHS の速報一覧と日本学校保健会の感染症情報マップを案内する。[公開ワークフロー](../../.github/workflows/publish-official-links.yml)は、トップページ・404・CSS の3ファイルを一時ディレクトリに揃え、SHA-256 を記録して配布する。

数値版の初回配布に失敗した場合は、現在の公開版を先に確認する。復旧が必要なら、承認後に既定ブランチから `publish-official-links.yml` を `restore_initial=true` で手動実行する。公開済みの初版 `6f7cd69` から3ファイルを梱包する。完了後は GitHub Actions が返すページ URL でトップページ、CSS、未定義パスでの404と戻り先を確認し、ファイルのハッシュを照合する。[公式リンク初版の公開実行](https://github.com/Olein-jp/japan-infection-watch/actions/runs/45522869066)
