# Slack 自動集計 BOT

created by kn5suzuki

## 環境構築

pyenv のインストール

pipenv のインストール

```
pip3 install pipenv
```

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

pipenv により仮想環境に必要なパッケージをインストール

```
pipenv install
```

## アプリ実行

pipenv 環境でスクリプトを実行

```
pipenv run python3 app.py
```

## 実行ファイルの作成

app.spec ファイルを元に pyinstaller で実行ファイルを作成

dist ディレクトリに app ファイルが作成される

```
pipenv run pyinstaller app.spec
```
