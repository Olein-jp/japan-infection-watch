# 進捗

更新日 2026-11-24（JST）

現在は調査段階。[調査・実現可能性評価（R-01〜R-19）（#1）](https://github.com/Olein-jp/japan-infection-watch/milestone/1) に調査 Issue 19件を登録済み。個別調査の結論と実測結果は未取得。開発移行の承認日、採用技術、対象データは承認時に AGENTS.md と本書へ追記する。

## 着手候補

最初は R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1)。独立して開始できるのは R-09 [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9)、R-10 [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10)、R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11)。いずれも依頼者の指定を待つ。

## イシュー別の状態

| 調査 ID | GitHub Issue | 状態 | 未確認の主な事項 | 着手前に確認する依存 Issue |
|---|---|---|---|---|
| R-01 | [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) | 未着手 | 公開ビュー、定義、参加範囲 | なし |
| R-02 | [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) | 未着手 | 閲覧・取得・保存・再公開等の許容範囲 | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1) |
| R-03 | [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) | 未着手 | 公開ビューの公式埋め込み | R-01 [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1)、R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) |
| R-04 | [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) | 未着手 | 集計 API と公式 CSV の取得可否 | R-03 [#3](https://github.com/Olein-jp/japan-infection-watch/issues/3) |
| R-05 | [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5) | 未着手 | 市区町村別のキー・分母・粒度 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-06 | [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6) | 未着手 | 学校コード・学校種別・閉鎖種別 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-07 | [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7) | 未着手 | 取得可能な最古・最新と期間 | R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4) |
| R-08 | [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8) | 未着手 | 学校検索 API の認証・応答・キャッシュ | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2) |
| R-09 | [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9) | 未着手 | JIHS CSV の公式配布経路、対象範囲、速報訂正 | なし |
| R-10 | [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10) | 未着手 | 厚労省 PDF の抽出精度と集計単位 | なし |
| R-11 | [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) | 未着手 | 岐阜県・岐阜市の公表粒度、保健所管轄 | なし |
| R-12 | [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12) | 未着手 | 47都道府県の公式配布形式・粒度 | R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) |
| R-13 | [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13) | 未着手 | 自治体・教育委員会の閉鎖データ | R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) |
| R-14 | [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) | 未着手 | 自治体・学校・地理マスターの照合可否 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-08 [#8](https://github.com/Olein-jp/japan-infection-watch/issues/8)、R-11 [#11](https://github.com/Olein-jp/japan-infection-watch/issues/11) |
| R-15 | [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) | 未着手 | 共通スキーマと品質検証・公開用分割 | R-05 [#5](https://github.com/Olein-jp/japan-infection-watch/issues/5)、R-06 [#6](https://github.com/Olein-jp/japan-infection-watch/issues/6)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-09 [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9)、R-10 [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10)、R-14 [#14](https://github.com/Olein-jp/japan-infection-watch/issues/14) |
| R-16 | [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) | 未着手 | 継続取得・保存・再公開・障害復旧の条件 | R-02 [#2](https://github.com/Olein-jp/japan-infection-watch/issues/2)、R-04 [#4](https://github.com/Olein-jp/japan-infection-watch/issues/4)、R-07 [#7](https://github.com/Olein-jp/japan-infection-watch/issues/7)、R-09 [#9](https://github.com/Olein-jp/japan-infection-watch/issues/9)、R-10 [#10](https://github.com/Olein-jp/japan-infection-watch/issues/10)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15) |
| R-17 | [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) | 未着手 | Pages/Actions の制約・費用と静的構成 | R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16) |
| R-18 | [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) | 未着手 | MVP の提供可能な地域・データ範囲 | R-12 [#12](https://github.com/Olein-jp/japan-infection-watch/issues/12)、R-13 [#13](https://github.com/Olein-jp/japan-infection-watch/issues/13)、R-15 [#15](https://github.com/Olein-jp/japan-infection-watch/issues/15)、R-16 [#16](https://github.com/Olein-jp/japan-infection-watch/issues/16)、R-17 [#17](https://github.com/Olein-jp/japan-infection-watch/issues/17) |
| R-19 | [#19](https://github.com/Olein-jp/japan-infection-watch/issues/19) | 未着手 | 開発仕様案、保留事項、開発 Issue 案 | R-18 [#18](https://github.com/Olein-jp/japan-infection-watch/issues/18) |

## 初期構築で確認した事項

- ローカルは初回コミット前の `main`。GitHub 側の既定ブランチ名は `main` で、ブランチの実体は初回 push 後に作られる。
- GitHub は Public、Issues 有効、Pages 無効。Issue フォームはローカルに配置済みで、GitHub のフォーム選択画面への反映には既定ブランチへの反映が必要。
- 一次情報台帳の31件は候補。情報源、利用条件、対象範囲、設計・費用の調査は各 Issue で行う。
