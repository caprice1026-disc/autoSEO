# Pythonの公式イメージをベースとして使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonパッケージをインストールするためのrequirements.txtファイルをコピー
COPY requirements.txt /app/

# requirements.txtにリストされたパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# 現在のディレクトリの内容をコンテナの作業ディレクトリにコピー
COPY . /app

# コンテナがリッスンするポート番号を環境変数から取得するように設定
ENV PORT 8080
EXPOSE $PORT

# コンテナ起動時にFlaskアプリケーションを実行
CMD ["python", "app.py"]