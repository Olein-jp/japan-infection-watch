# R-01 日本学校保健会の公開ビュー・公式資料の棚卸し

- GitHub Issue [#1](https://github.com/Olein-jp/japan-infection-watch/issues/1)
- 調査日 2026-11-24 JST
- 状態 完了（2026-11-24 JST）
- 結論 公式ポータル掲載の98リンクを特定し、市区町村別の閉鎖地図1件を通常閲覧で確認。プログラムによる取得可否は未確認。

## 調査目的・対象外

学校等欠席者・感染症情報システムの一般向けマップビューについて、公式の入口、表示単位、指標、日付指定、施設別公開の範囲を整理した。対象は公式ポータルの掲載欄、公開プロフィールと代表ビュー、下表の文書。自動取得、埋め込み API、規約の適用判定、非公開情報の探索は後続または対象外とした。

## 一次情報

確認日はすべて 2026-11-24 JST。PDF のページ番号は表紙を含めて1から数える。

| ID | 資料 | 公開・改訂の根拠 | 確認箇所 |
|---|---|---|---|
| S01 | [感染症情報マップ](https://www.gakkohoken.jp/system_information/jssh_absence_information_mapping) | 変更欄に 2024-03-25、2023-07-03、2023-06-08、2023-03-15。ページ全体の改訂日は不明 | 変更欄、初期表示フィルター、分類別リンク表 |
| S04 | [システム使用規程](https://www.gakkohoken.jp/files/ccenter/system/20230803/202308mapview.pdf) | 2023年8月改訂（附則 p.6）、関係通知は 2023-08-03 | pp.1–3 の第2項、第8〜11項。入力データと統計化情報の区別、公開範囲の制限 |
| S05 | [マップビュー説明](https://www.gakkohoken.jp/files/ccenter/20220412/mapview-manual.pdf) | S01 の掲載日 2022-04-12 | pp.2–6 の指標と表示例、p.9 の疾患・症状と地域粒度の一覧。当時の仕様 |
| S06 | [マップビューの活用について](https://www.gakkohoken.jp/files/ivent/20240722/program-02.pdf) | [研修開催日 2024-07-22](https://www.gakkohoken.jp/system_information/online_workshop/workshop20240722)。資料の改訂日は不明 | pp.4–6 の分類・計上ルール、pp.8–14 の変更・操作、pp.22–23 の実数表 |
| S07 | [2023年の表示変更](https://www.gakkohoken.jp/files/ccenter/mapview/202303view_change.pdf) | S01 の告知日 2023-03-15。PDF p.2 は変更後の公開を3月下旬予定と記載 | pp.2–9 の疾患・症状の区分、市区町村の一覧・棒グラフ |
| S08 | [Tableau Public 掲載プロフィール](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/vizzes) | 一覧の改訂日は不明 | 掲載者名、公開作品の表示件数、表示された先頭12件の公開パス |
| S32 | [2024年の表示変更](https://www.gakkohoken.jp/files/ccenter/mapview/20240325view_change.pdf) | S01 の告知日 2024-03-25 | pp.3–5 の初期フィルターと実績表、p.6 の閉鎖クラス数の変更 |
| S33 | [登録状況・利用状況の推移](https://www.gakkohoken.jp/files/ccenter/system/registration_status_and_usage_status_2025.pdf) | [システム案内](https://www.gakkohoken.jp/system_information/)から到達。公開・改訂日は不明。2025年度集計の基準日は 2026-03-31 | p.3 の施設種別表、脚注1〜3、p.4 の補足 |
| S34 | [2026年のマップビュー研修資料](https://www.gakkohoken.jp/files/ivent/20260722online/20260722siryo-01.pdf) | [研修開催日 2026-07-22](https://www.gakkohoken.jp/system_information/online_workshop/workshop20260722)。資料の改訂日は不明 | pp.2、4–5 の分類・指標、pp.7–9 の対象日と更新時点、pp.17–18 の実数表示 |

## 指標・日付・フィルター

| 表示 | 読み方 | 対象日・操作と確認範囲 |
|---|---|---|
| 欠席者の急増 | 当日の入力欠席者数が過去7日分の平均を標準偏差の3倍以上上回ったクラスの数。全体と症状別の表示がある | 地図で日付・症状・地域を選ぶ。実数表に日付指定と自治体指定がある。S01、S06 p.5、S34 pp.4–5・7–9 |
| 出席停止 | 入力された出席停止の人数を疾患・理由別に表示。S06・S34 は措置期間にわたり計上すると説明 | 都道府県・市区町村の地図と実数表、掲載対象に応じて施設地図。対象日、疾患名・区分、地域で絞る。S01、S06 pp.4–5、S07 pp.5–8、S34 pp.4–5 |
| 学級閉鎖 | 措置期間中の閉鎖クラス数。2024-03-25 の変更告知以降の表示仕様は、休校と学年閉鎖に含まれるクラスも合算する。閉鎖した施設数、新しく始まった閉鎖件数とは区別する | 都道府県・市区町村の地図と実数表、掲載対象に応じて施設地図。市区町村の代表地図で日付、疾患・症状の区分、疾患名、地方、都道府県の操作欄を確認。S01、S32 p.6、S34 p.5 |
| 全国補足 | 人数・クラス集計の補足ビュー | S01 に1リンク。現行の項目・対象日・分母は未確認 |

- S01 と S32 p.3 では、ポータルの初期表示に八地方区分と都道府県を選べる。表の URL はこの選択による変更前の掲載値を保持した。S07 pp.7–8 と S32 p.4 は、指定日を地域・疾患別に見る一覧と、自治体を選んで月別の情報も見る例を示す。月別表示の算出方法は未確認。
- S34 pp.2・7–9 では、入力内容を2時間間隔で反映し、日単位で過去1年を選択できると説明する。対象日と元データの更新時点は別表示。全ビューでの最古日や履歴の保持期間は R-07 で確認する。
- 施設別の掲載はインフルエンザ、感染性胃腸炎、その他疾患と、2023-06-04 までの旧理由別の出席停止にある。現在の新型コロナウイルス欄には施設別リンクがない。S01 の 2023-07-03 告知には施設名公表の延期が記載されている。S05 p.9 は2022年時点の疾患内訳であり、現行の全フィルター値は未確認。
- S04 第10項は統計化情報の一般開示を原則とし、自治体との協議による公開単位や公開範囲の変更を記載。一般閲覧と自動取得・保存・再公開の条件は R-02 で個別に調べる。

## 参加範囲

S33 p.3 の2025年度の表では、登録率は全国総施設数に占める登録施設、利用率は同年度に入力実績があった施設の割合。利用率は登録施設を分母にした値と、全国総施設を分母にした値が別掲される。登録・利用施設数の基準日は 2026-03-31、学校の全国総施設数は学校基本調査の 2025-05-01 時点。S33 p.3 の脚注1〜3を参照。

| 施設種別 | 全国総施設 | 登録施設 | 利用施設 | 登録率 | 登録施設中の利用率 | 全国総施設中の利用率 |
|---|---:|---:|---:|---:|---:|---:|
| 小学校 | 18,607 | 11,706 | 10,372 | 62.9% | 88.6% | 55.7% |
| 中学校 | 9,827 | 5,968 | 5,146 | 60.7% | 86.2% | 52.4% |
| 高等学校 | 4,761 | 3,857 | 2,656 | 81.0% | 68.9% | 55.8% |
| 全種別合計 | 77,390 | 41,148 | 27,803 | 53.2% | 67.6% | 35.9% |

この表は年度単位で、地域・日・疾患ごとの公開ビューへの寄与施設数や割合は確認できない。中高一貫の行は全国総施設を分母とする比率が100%を超えているため、その行の分母と分類を確認できるまでは網羅率の判断に使わない。未報告地域や未表示施設にはゼロを補わない。

## 再現手順と観測結果

1. S01 を通常の HTTP GET で1回取得（HTTP 200、curl 8.7.1）。一覧表の Tableau Public へのリンクを Python 3.13.5 で抽出し、HTML のリンク出現数と突合した。掲載98件、同じ URL の重複を除いて94件、クエリを除いたパスが58件。URL の日本語クエリと空の `?` は掲載どおり。
2. S08 をブラウザで開くと公開作品数は59件。画面に現れた先頭12件のパスはすべて S01 の一覧と一致した。59件の表示はプロフィールの作品数であり、98件はポータルのリンク掲載数。プロフィール全件とポータルとの差分は未照合。
3. ブラウザで、S01 のインフルエンザ欄にある[市区町村別の学級閉鎖地図](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=3)を1回表示。2026-11-24 13時台（JST）に、画面上の対象日が 2026-11-23、元データが 2026-11-24 11時時点と確認した。凡例は1,000クラスあたりの閉鎖クラス数。表示のアクセシビリティ情報に合計クラス数と閉鎖クラス数があったが、分母の対象範囲・算出式・フィールドの取得可否は未検証。個別施設名・集計値の採取や保存は行っていない。

**リンク名とクエリの食い違い**。インフルエンザの都道府県別実数表の4リンク（出席停止・学級閉鎖の各日付指定・自治体指定）が、新型コロナウイルス欄の同じ4リンクと同一で、掲載 URL の疾患・症状の区分は `10`。代表地図のフィルター凡例では `3` がインフルエンザ、`10` が新型コロナウイルス感染症。実数表での初期表示は未確認のため、名称だけでデータ種別を割り当てず、掲載 URL をそのまま記録した。

## 公開ビュー URL 一覧

列は公式案内の掲載粒度・形式を示す。ダッシュは掲載リンクなし。全国補足の URL は実数欄に掲載されているが、日付指定の有無は未確認。

### 欠席者情報

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 欠席者急増クラス数 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470720370580/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095526808660/1?症状区分=1) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095528266380/1?症状区分=1) |
| 都道府県別 | 欠席者急増クラス数－症状別 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16461344771100/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095526808660/1?症状区分=2) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095528266380/1?症状区分=2) |
| 市区町村別 | 欠席者急増クラス数 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16461342305690/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744382673950/1?症状区分=1) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17431182375550/1?症状区分=1) |
| 市区町村別 | 欠席者急増クラス数－症状別 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470715931070/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744382673950/1?症状区分=2) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17431182375550/1?症状区分=2) |

### 新型コロナウイルス

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470737773270/1) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095531230140/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532174170/1?疾患・症状の区分=10) |
| 都道府県別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470713116370/1?疾患・症状の区分=10) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532851780/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095533629730/1?疾患・症状の区分=10) |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16874096591520/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=10) |
| 市区町村別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=10) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16672034247720/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744492330710/1?疾患・症状の区分=10) |

### インフルエンザ

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470722688130/1) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095531230140/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532174170/1?疾患・症状の区分=10) |
| 都道府県別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470713116370/1?疾患・症状の区分=3) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532851780/1?疾患・症状の区分=10) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095533629730/1?疾患・症状の区分=10) |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470721073550/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=3) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=3) |
| 市区町村別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=3) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16672034247720/1?疾患・症状の区分=3) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744492330710/1?疾患・症状の区分=3) |
| 学校（施設）別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470721871210/1?) | — | — |
| 学校（施設）別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470712448940/1?疾患・症状の区分=3) | — | — |

### 感染性胃腸炎

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470736833650/1) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095531230140/1?疾患・症状の区分=6) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532174170/1?疾患・症状の区分=6) |
| 都道府県別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470713116370/1?疾患・症状の区分=6) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532851780/1?疾患・症状の区分=6) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095533629730/1?疾患・症状の区分=6) |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470735037950/1) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=6) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=6) |
| 市区町村別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=6) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16672034247720/1?疾患・症状の区分=6) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744492330710/1?疾患・症状の区分=6) |
| 学校（施設）別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470735959990/1?) | — | — |
| 学校（施設）別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470712448940/1?疾患・症状の区分=6) | — | — |

### その他疾患

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16469086531330/1) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095531230140/1?疾患・症状の区分=4,5,7) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532174170/1?疾患・症状の区分=4,5,7) |
| 都道府県別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470713116370/1?疾患・症状の区分=4,5,7) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095532851780/1?疾患・症状の区分=4,5,7) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____17095533629730/1?疾患・症状の区分=4,5,7) |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470723915880/1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=4,5,7) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=4,5,7) |
| 市区町村別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470709141460/1?疾患・症状の区分=4,5,7) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16672034247720/1?疾患・症状の区分=4,5,7) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/____16744492330710/1?疾患・症状の区分=4,5,7) |
| 学校（施設）別 | 出席停止・北海道 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470730232390/1?) | — | — |
| 学校（施設）別 | 出席停止・東北 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470729578190/1?) | — | — |
| 学校（施設）別 | 出席停止・関東 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470724809870/1?) | — | — |
| 学校（施設）別 | 出席停止・中部 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470728903930/1?) | — | — |
| 学校（施設）別 | 出席停止・近畿 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470725977580/1?) | — | — |
| 学校（施設）別 | 出席停止・中国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470728305720/1?) | — | — |
| 学校（施設）別 | 出席停止・四国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470727733970/1?) | — | — |
| 学校（施設）別 | 出席停止・九州・沖縄 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470726873590/1?) | — | — |
| 学校（施設）別 | 学級閉鎖 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16470712448940/1?疾患・症状の区分=4,5,7) | — | — |

### 感染症システムの人数、クラス集計情報等

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 全国 | 人数・クラス集計など | — | [全国集計](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/_16475619974150/1) | — |

### 旧・新型コロナ関連（2023-06-04まで） 発熱等による

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765123927900/1_1) | — | — |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765126154010/1_1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=8) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=8) |
| 学校（施設）別 | 出席停止・北海道 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765127637510/1_1?) | — | — |
| 学校（施設）別 | 出席停止・東北 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765129931320/1_1?) | — | — |
| 学校（施設）別 | 出席停止・関東 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765131662580/1_1?) | — | — |
| 学校（施設）別 | 出席停止・中部 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765134112440/1_1?) | — | — |
| 学校（施設）別 | 出席停止・近畿 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765136733240/1_1?) | — | — |
| 学校（施設）別 | 出席停止・中国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765140379020/1_1?) | — | — |
| 学校（施設）別 | 出席停止・四国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765138359200/1_1?) | — | — |
| 学校（施設）別 | 出席停止・九州・沖縄 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765142670080/1_1?) | — | — |

### 旧・新型コロナ関連（2023-06-04まで） 家族等のかぜ症状等による

| 粒度 | 指標 | 地図・割合 | 実数・日付指定 | 実数・自治体指定 |
|---|---|---|---|---|
| 都道府県別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765144198030/1_1) | — | — |
| 市区町村別 | 出席停止 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765146303220/1_1?) | [日付指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744399702560/1?疾患・症状の区分=9) | [自治体指定](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/___16744414821600/1?疾患・症状の区分=9) |
| 学校（施設）別 | 出席停止・北海道 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765147993450/1_1?) | — | — |
| 学校（施設）別 | 出席停止・東北 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765149711050/1_1?) | — | — |
| 学校（施設）別 | 出席停止・関東 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765151407320/1_1?) | — | — |
| 学校（施設）別 | 出席停止・中部 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765153218830/1_1?) | — | — |
| 学校（施設）別 | 出席停止・近畿 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765155139540/1_1?) | — | — |
| 学校（施設）別 | 出席停止・中国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765158376170/1_1?) | — | — |
| 学校（施設）別 | 出席停止・四国 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16765156704190/1_1?) | — | — |
| 学校（施設）別 | 出席停止・九州・沖縄 | [地図・割合](https://public.tableau.com/app/profile/jssh.absence.information.mapping.service/viz/__16775624093440/1_1?) | — | — |

## 未確認事項と後続への引き継ぎ

- R-02 は S04 と Tableau の条件を確認し、公式埋め込み・取得・保存・再公開の範囲を判断する。代表地図は R-02 の検討後、R-03 で埋め込み可否を確認する候補。
- R-04・R-05 は許容された範囲で、表示と取得データの指標・粒度・分母を照合する。インフルエンザ都道府県実数表の掲載値と表示の食い違いも確認対象にする。
- R-06 は施設種別・閉鎖種別の分離の可否を確認する。休校・学年閉鎖込みの集計を分解できるとは扱わない。変更前への遡及適用も未確認。
- R-07 は現行の選択可能期間、未取得期間、日次と月次集計の関係を確認する。年度の利用率から日単位の報告率は推定しない。

## 受入基準

- [x] 公式案内掲載の URL、疾患・理由、粒度、指標、日付指定・自治体指定を一覧化した。
- [x] 公式文書の掲載・改訂時期と該当ページ、確認日、代表ビューの実表示を記録した。
- [x] 閉鎖クラス数の変更内容と適用に関する未確認事項、登録率・利用率とそれぞれの分母を記録した。
- [x] 掲載名と URL の食い違い、未確認の範囲、次の検証先を記録した。
