# 全国感染症・学校閉鎖情報サービス

日本全国の感染症発生動向と学校の閉鎖状況を、保護者を含む一般利用者が地域・疾患・期間ごとに確認できるサービスを構想しています。対象施設、出典、集計期間、更新日時、欠損と公開範囲を表示する方針です。

現在は調査段階です。調査、技術検証、設計、開発、公開、運用を同じリポジトリで管理します。公開先は GitHub Pages を第一候補とし、GitHub Actions で許容範囲内の取得、正規化、品質検証、静的生成を行い、公開専用成果物だけを配信する構想です。定期取得と公開設定は、調査と承認の後に進めます。

`docs/` は調査・設計資料の保管先です。サイトには再配布できる集計のみを含め、欠損と明示的なゼロを区別します。取得・公開に失敗した場合に、直前の成功版を維持する構成を検証します。

調査を開始する場合は、[作業ルール](AGENTS.md)、[進捗](docs/status.md)、[ロードマップ](docs/issue-roadmap.md)を確認し、指定された Issue の依存関係と利用条件を読んでください。最初の候補は R-01 です。

- [プロジェクト範囲と Pages の要件](docs/project-scope.md)
- [調査方針](docs/research-policy.md)と[一次情報台帳](docs/source-register.md)
- [調査結果の書き方](docs/findings/README.md)と[判断記録](docs/decisions.md)
- [データ辞書](docs/schemas/README.md)、[構成設計](docs/architecture/README.md)、[仕様案](docs/specifications/README.md)
- [実現可能性評価](docs/final-report/README.md)と[運用設計](docs/operations/README.md)
