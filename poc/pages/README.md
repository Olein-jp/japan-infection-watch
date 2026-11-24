# 架空データでの静的配信の試験

[調査結果](../../docs/findings/R-17-pages-architecture.md)と[構成候補](../../docs/architecture/pages-layout.md)を参照。リポジトリルートから実行する。ビルドと容量の試算は Python 3 の標準ライブラリのみで動く。ブラウザ確認には Node.js と Chrome が必要。

```sh
work=$(mktemp -d)
python3 poc/pages/build.py "$work" release-01
python3 poc/pages/serve.py "$work"
```

サーバーが表示するループバック URL に `/japan-infection-watch/` を付けて開く。独自ドメイン相当の試験は、別の作業ディレクトリでビルドとサーバーに `--base /` を付ける。出力の通常ファイル一式は `$work/archive/release-01/` にあり、`active` はローカルサーバーが切り替えに使う。

macOS で配布用ファイルの一覧を tar.gz で確認する場合は、拡張属性が追加されないようにして、版のディレクトリだけをまとめる。

```sh
COPYFILE_DISABLE=1 tar -czf "$work/artifact.tar.gz" -C "$work/archive/release-01" .
tar -tzf "$work/artifact.tar.gz"
```

```sh
deps=$(mktemp -d)
npm install --prefix "$deps" --ignore-scripts --no-audit --no-fund playwright@1.58.2
NODE_PATH="$deps/node_modules" node poc/pages/check.cjs
python3 poc/pages/measure.py
```

ブラウザ試験は、その場で作成した一時ディレクトリを使う。ループバック外の通信を遮断し、正常版と破損候補を試す。容量試算は47都道府県分をローカルの一時ファイルとして生成し、市区町村の値は各12地域分の計測を基に推計する。施設や境界は架空。
