from openai import OpenAI
import os

# Openai APIの設定
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI()
# assistantは先に作成しておくこと。
OpenAI_assistant_id = os.environ["assistant_id"]

def feleimport(file_path):
    try:
        uploaded_file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants",
        )
        file_id = uploaded_file.id
        print(file_id)
        return file_id
    except Exception as e:
        print(f"ファイルのインポート中にエラーが発生しました: {e}")
        return ""


assistant_file = client.beta.assistants.files.create(
  assistant_id=OpenAI_assistant_id,
  file_id="file-abc123"
)
print(assistant_file)

