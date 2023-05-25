# Slack 自動化 アプリ

GUI で Slack の作業を自動化できるアプリ
実行ファイルにして人に配布することも可能

## 環境構築

pyenv のインストール

pyenv で Python のバージョン 3.10.3 をインストールし、適用

```
pyenv install 3.10.3
pyenv local 3.10.3
```

※pyinstaller を使うためには Python を共有ライブラリとしてビルドする必要がある

```
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.3
pyenv local 3.10.3
```

pipenv のインストール

```
pip3 install pipenv
```

pipenv により仮想環境に必要なパッケージをインストール

```
pipenv install
```

## アプリ実行

pipenv 環境でスクリプトを実行

```
pipenv run python3 app.py
```

## アプリの使い方

- まずは操作したい bot などのトークンを設定する
  <image src="images/image1.png">

- トークンを設定すると、機能の選択画面に遷移する
- 機能は以下の 3 つである
  - チャンネルを選択してメッセージを送信する
  - チャンネルとそのチャンネルの中のキーワードを設定してメッセージを検索し、そのメッセージにリアクションしていない人にメンション付きのリマインドを送る
  - チャンネルとそのチャンネルの中のキーワードを設定してメッセージを検索し、そのメッセージに返信していない人にメンション付きのリマインドを送る
    <image src="images/image2.png">
    <image src="images/image3.png">
    <image src="images/image4.png">

## 実行ファイルの作成

app.spec ファイルを元に pyinstaller で実行ファイルを作成

dist ディレクトリに app ファイルが作成される

```
pipenv run pyinstaller app.spec
```
