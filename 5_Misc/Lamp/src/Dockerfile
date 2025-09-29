FROM python:3.11-slim

# 作業ディレクトリ作成
WORKDIR /app

# 依存ファイルとアプリのコピー
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ポート公開
EXPOSE 5000

# アプリ起動
CMD ["python", "app.py"]