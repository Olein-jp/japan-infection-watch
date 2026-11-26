# R-16　JIHS と厚労省の取得・保存・再公開の運用検証

- 対象は [Issue #16](https://github.com/Olein-jp/japan-infection-watch/issues/16)。確認日 2026-11-24（JST）。JIHS IDWR の週次定点 CSV と厚労省の学校欠席者数 PDF を対象とした。日本学校保健会の集計・学校検索 API は #2 の利用条件と #7 の取得範囲の確認待ち。
- 既存の [JIHS CSV の検証](R-09-jihs-csv.md)・[厚労省 PDF の検証](R-10-mhlw-absence-pdf.md)と同じ URL で、変更検知に使える応答を少数観測した。更新・訂正・復旧の手順は[取得・公開の運用案](../operations/collection-and-recovery.md)に記録した。

## 公表周期と訂正経路

| 対象 | 公表の確認 | 訂正の確認 |
|---|---|---|
| JIHS IDWR 週次定点速報 CSV | 2026年第45週は11月17日、第46週は11月24日に掲載。いずれも火曜日。第46週の対象は11月9〜15日。公式案内の「更新」と週別掲載を参照する。11月30日予定の第46号は週報 PDF の別日程。[速報年別一覧](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/index.html)・[速報第45週の更新欄](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/45/index.html)・[週報の発行予定](https://id-info.jihs.go.jp/surveillance/idwr/idwr/2026/index.html) | 速報は週報・年報で修正される場合がある。週別ページの更新欄、週報の訂正告知、年報の訂正一覧を確認する。年報は定義が一致する範囲で照合し、週の速報ファイルの上書きと推定しない。同一 URL の CSV 差し替え前後は未観測。[週報訂正例](https://id-info.jihs.go.jp/niid/ja/allarticles/surveillance/4755-teisei-owabi.html)・[年報訂正一覧](https://id-info.jihs.go.jp/surveillance/idwr/annual/correction/index.html) |
| 厚労省の学校欠席者数 PDF | 2026/27シーズン第10報は11月13日、第11報は11月20日、後者の表紙は次回を11月27日予定と記載。いずれも金曜日。シーズン一覧には9月29日（火曜日）の例もあるため、個別号の次回予告を優先する。[シーズン掲載一覧](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/kenkou/kekkaku-kansenshou01/houdou_00025.html)・[第11報 p.1、pp.4–5](https://www.mhlw.go.jp/content/001770872.pdf) | シーズン掲載一覧の更新、掲載先 URL の変更、PDF の差し替えを確認する。p.4 脚注によれば初発年月日と累計には前報までの修正を含む。前報累計＋当週の合計を次報累計に置き換える計算は行わない。学校欠席表専用の訂正フィードと、同一号の差し替え前後は確認できていない。[第10報](https://www.mhlw.go.jp/content/001768730.pdf)・[第11報](https://www.mhlw.go.jp/content/001770872.pdf) |

公表曜日は確認した号の実績と予定。提供元が許容する自動取得の頻度や回数はここから判断できない。許容頻度と再取得・訂正追跡の経路は運用開始前に提供元に確認する。

## 利用条件の判断

「条件付き」は該当資料を利用できる一般条件を文書で確認した段階。実際に扱う版、項目、第三者の権利、出典表示、プロジェクトの承認を揃えて公開可否を記録する。

| 対象 | 通常閲覧・少量試験取得 | 一時保存・加工 | 長期保存 | 再公開・商用利用 | 定期取得 |
|---|---|---|---|---|---|
| JIHS の週次定点速報 CSV | 確認済み。公式週別ページのリンクを使用 | 条件付き。原本はそのまま保存し、抽出・正規化した結果に出典と加工を表示 | 条件付きの候補。一般利用規約で複製の条件を確認。個別制限と保持方法は運用前に確認 | 独自グラフは出典と別に加工を明示する条件で利用可能（S102）。各週の注記・第三者権利と描画用 JSON の配布条件は公開前に確認。商用利用は一般規約を参照。[回答の要旨](O-001-release-readiness.md#jihs-の回答と数値版への反映) | 未確認。許容頻度、定期実行と同一週の再確認の可否を問い合わせ候補とする |
| JIHS の週報 PDF | 公式の閲覧・比較に使用済み | 掲載された週報を内部の照合に使用。配布用の加工・保持は個別注記を確認 | 条件未確認。検証後の継続保存は保留 | 第45号 p.37 に個別の転載制限。PDF・その表をそのまま再配布する候補は保留 | 未確認。今回の定期取得候補は速報 CSV |
| 厚労省 PDF pp.4–5 の学校欠席表 | 確認済み。シーズンの公式報道発表から取得 | 条件付き。該当表の数値の抽出・正規化を候補とし、原資料と加工主体を表示する | 条件付きの候補。一般規約は複製可。保持・削除の方針と版別の制限を確認 | 表の数値の再公開と商用利用を条件付き候補とする。確認した pp.4–5 は適用除外別紙への掲載や固有の権利注記を確認できなかった。PDF 全体・ロゴ・第三者の素材はこの判定の範囲外 | 未確認。利用規約は定期アクセス頻度や補正の再照会条件を示していない |
| 日本学校保健会・Tableau 上の集計と学校検索 API | [R-02](R-02-reuse-terms.md)の範囲に従う | 個別適用条件は回答待ち | 回答待ち | 回答待ち | 回答待ち |

- **JIHS**。サイト規約の冒頭と第1・2・5・7・8項を確認。複製・公衆送信・加工・商用利用に関する一般条件、出典・加工の明示、第三者権利、転載指定・改変への条件を適用する。週報 PDF と速報 CSV は資料ごとに判定する。[サイト規約](https://id-info.jihs.go.jp/usage-contract.html)・[第45号 PDF p.37](https://id-info.jihs.go.jp/surveillance/idwr/idwr/2026/idwr2026-45.pdf#page=37)
- **厚労省**。重要情報 §1.1・§1.4 と適用除外の別紙、PDL1.0 §1・§1.1〜1.4 を確認。PDL1.0 は数値・簡単な表等を適用範囲外と説明している。出典・加工主体の表示を運用上残し、第三者権利と個別注記を版ごとに確認する。[厚労省規約](https://www.mhlw.go.jp/chosakuken/index.html)・[適用除外の別紙](https://www.mhlw.go.jp/chosakuken/exhibit.html)・[PDL1.0](https://www.digital.go.jp/resources/open_data/public_data_license_v1.0)

両サイトとも、個別注記がある場合を除き、提供元が分かる形で公式ページにリンクできる旨を案内している。配信の可否が未確定の資料は、週別ページやシーズン掲載一覧へのリンクを案内候補とする。[JIHS 規約の第6項](https://id-info.jihs.go.jp/usage-contract.html)・[厚労省のリンク案内](https://www.mhlw.go.jp/chosakuken/index.html)

照会を行う場合は、JIHS には対象 CSV の定期取得と再確認の頻度、保存条件、訂正版の通知経路を確認する。厚労省には該当ページの PDF 確認の頻度、数値抽出の再公開条件、訂正 URL の案内の有無を確認する。いずれも運用の前提が決まった段階で照会の要否をレビューする。

## 少量の再取得と変更判定

2026-11-24 19:34:42 JST に、許容範囲にある公開 URL を1件ずつ通常取得し、取得時の HTTP ヘッダーで同じファイルを条件付き取得した。上限は各2回、合計4回。curl 8.7.1、各リクエスト20秒・1,500,000バイト・リダイレクト上限2。再試行はせず、ローカルの一時領域で SHA-256 を比較した。

| 対象 | 当日先に取得した版と通常 GET | 直後の条件付き GET | 判定 |
|---|---|---|---|
| [JIHS 第46週定点 CSV](https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/2026-46-teiten.csv) | #9 で14:20 JST に取得済み。再取得は HTTP 200、11,269バイト、`text/csv`。 `Last-Modified: Tue, 24 Nov 2026 01:31:47 GMT`。ETag は応答になかった | `If-Modified-Since` で同じ日時を送り、HTTP 304・本文0バイト | 通常 GET の SHA-256 は #9 と一致。304 は参照した手元版の確認として処理できる |
| [厚労省第11報 PDF](https://www.mhlw.go.jp/content/001770872.pdf) | #10 で14:29 JST に取得済み。再取得は HTTP 200、233,115バイト、`application/pdf`。 `Last-Modified: Fri, 20 Nov 2026 04:55:41 GMT`、`ETag: "38e9b-660ae0e5997ec"` | 同じタグを `If-None-Match` で送り、HTTP 200・233,115バイト | 3回とも SHA-256 一致。200 で本文を受け取っても同じハッシュなら新しい版を作らない |

SHA-256 は JIHS CSV が `ae5642911f0c702ba2ab4035fb3ca6e7516f4f9cd4799e78bed51908fac6e310`、厚労省 PDF が `516bdbe2d733563ba072cf190a42e9a6c14d76186ac8c968652f1396fb4ad950`。同一日の少数応答であり、将来のヘッダーの提供や訂正時の応答は未検証。[HTTP の条件付き要求 RFC 9110 §13.1.2・§13.1.3・§15.4.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-13)

再現時は利用条件と対象 URL を確認し、同じ保存先を上書きせず、別ファイルに取得する。

```sh
scratch=$(mktemp -d)
url='https://id-info.jihs.go.jp/surveillance/idwr/provisional/2026/46/2026-46-teiten.csv'
curl -fsSL --max-time 20 --max-redirs 2 --max-filesize 1500000 \
  -D "$scratch/first.headers" -o "$scratch/first" \
  -w '%{http_code} %{size_download}\n' "$url"
shasum -a 256 "$scratch/first"
# 通常 GET が 200 の場合に限り、同じ URL の Last-Modified を使用する
modified=$(awk 'tolower($1) == "last-modified:" {
  sub(/^[^:]+:[[:space:]]*/, ""); sub(/\r$/, ""); print
}' "$scratch/first.headers" | tail -1)
if [ -n "$modified" ]; then
  curl -fsSL --max-time 20 --max-redirs 2 --max-filesize 1500000 \
    -H "If-Modified-Since: $modified" \
    -D "$scratch/conditional.headers" -o "$scratch/conditional" \
    -w '%{http_code} %{size_download}\n' "$url"
fi
```

## 受入基準と引き継ぎ

- JIHS と厚労省について、利用条件に沿った反復観測、版の変更を判断する方法、公表周期と訂正経路、保存と再公開の条件を記録した。条件付き取得の有効性は資料別に評価する。
- [取得・公開の運用案](../operations/collection-and-recovery.md)に取得制限、再試行、旧版保持、部分更新、ロールバック、保持と削除を記録した。常時実行や本番公開を開始する時期はプロジェクトの承認で決める。
- 日本学校保健会の条件、提供元が許容する定期取得、長期保管先と期間、Pages 上での復旧は未確定。後二者は #17 の構成検証とあわせて評価する。#16 は継続中。
