# R-19　初期版の開発仕様案と開発移行の判断

対象は [Issue #19](https://github.com/Olein-jp/japan-infection-watch/issues/19)。確認日 2026-11-24（JST）。[R-18](R-18-feasibility.md) と [初期指示書の付録A](../../CODEX_INITIAL_PROMPT.md#付録a-github-pages-を前提とした設計検証要件r-15r-19に反映)から、開発の Go 判断に使う仕様案を作成した。調査結果は完了承認待ち。

| 成果物 | 記載範囲 |
|---|---|
| [初期版の開発仕様案](../specifications/mvp.md) | データ候補と公開条件、全国・都道府県・市区町村・疾患別の静的 URL、公式案内への切り替え、指標・出典・更新・欠損、アクセシビリティ、段階計画。 |
| [公開アーキテクチャ案](../architecture/mvp-publication.md) | 同一リポジトリでの配置候補、取得・正規化・品質と許諾判定、分割 JSON と静的生成、専用 artifact、GitHub Actions と Pages の権限・公開確認。 |
| [更新・復旧・公開判定案](../operations/mvp-release.md) | 手動更新、定期取得の開始条件、訂正と旧版維持・復旧、月0円の判定、テストと公開前監査。 |
| [開発 Issue 案](../specifications/development-issues.md) | 準備、正規化、画面と JSON、Actions、検証、初回公開の6件。調査根拠、依存関係と確認できる受入条件を記載。 |

## 開発と公開の判断案

- **開発の初期範囲**。JIHS の週次定点集計を全国・都道府県で表示する仕様を第一案とする。利用条件が確定するまでは架空データで作業できる。画面は公式案内にも切り替えられる。Python での静的生成と HTML・CSS・JavaScript を第一案とし、長期の保守とページ構成を最初の開発 Issue で確認する。履歴は利用可能な週から開始し、直近52報告週を上限候補とする。
- **公開の条件**。再配布可能な資料と保存方法、公開・復旧に必要な入力の受け渡し、担当者、無料枠と課金停止の確認、ソース・履歴・公開物の監査が揃った段階で判断する。許諾未確定の数値は公開対象に含めない。開発の Go と公開の承認は別に記録する。
- **保留事項**。日本学校保健会の回答と学校別の取扱い、JIHS・厚労省の資料個別の加工・再公開・保持と自動取得頻度、地図の配布条件、実際の復旧先・保持期限、GitHub 上の時間・費用・配信実績。厚労省の休業系列と自治体データは条件が揃った範囲で追加判断する。仕様成立をこれらの未確認項目に依存させない。

## 一次情報と検証の範囲

| 一次情報 | 2026-11-24 に照合した範囲 |
|---|---|
| [S26 Pages 上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)・[S31 追加製品利用条件](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#pages) | 対象プラン、Usage limits、追加条件の Pages 節（2026-08-27 発効表示）。公開サイト上限、帯域、デプロイ時間と用途を運用案に反映。 |
| [S27 カスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)・[S28 公開元](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | 公開元の GitHub Actions、artifact の構成、公開ジョブの権限・依存・環境。 |
| [S29 イベント仕様](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) | schedule と workflow_dispatch。既定ブランチ、遅延、UTC とタイムゾーン指定、公開リポジトリの60日無活動を反映。 |
| [S30 Actions 課金](https://docs.github.com/en/billing/concepts/product-billing/github-actions)・[S99 予算設定](https://docs.github.com/en/billing/how-tos/set-up-budgets) | 標準 runner の無償対象、共有 artifact 枠、予算の適用範囲と課金停止。対象アカウントの設定は未確認。 |
| [S98 WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 2024-12-12 勧告版のキーボード操作、色の使用、コントラスト、リフロー、フォーカス、状態通知を画面と確認項目に反映。適合性そのものは公開前に検証する。 |

資料の取得結果は [R-09](R-09-jihs-csv.md)・[R-10](R-10-mhlw-absence-pdf.md)、利用条件は [R-16](R-16-collection-operations.md)、ブラウザ試験と容量の根拠は [R-17](R-17-pages-architecture.md)・[R-18](R-18-feasibility.md)。今回は仕様案と調査記録を照合し、既存の架空データ品質テスト15件と文書の内部リンク・開発 Issue 案の依存関係を確認した。実データを取得・保存・公開する試験と実運用の検証は未実施。

受入基準の、地域・疾患別ページ、取得から静的配信、監査・復旧、アクセシビリティ・テスト、月0円、段階計画・開発 Issue 案、一次情報と未確認事項を上記に記録した。依頼者の開発判断が出た時点で、採用範囲と承認日を記録して開発 Issue を作成する。
