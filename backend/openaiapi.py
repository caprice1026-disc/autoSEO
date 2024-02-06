from openai import OpenAI
import os

# Openai APIの設定
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# OpenAI API呼び出し関数
def openai_api_call(model, temperature, messages, max_tokens, response_format):
    try:
        # OpenAI API呼び出しを行う
        response = client.chat.completions.create(model=model, temperature=temperature, messages=messages, max_tokens=max_tokens, response_format=response_format)
        return response.choices[0].message.content  # 辞書型アクセスから属性アクセスへ変更
    except Exception as e:
        print(f"OpenAI API呼び出し中にエラーが発生しました: {e}")
        
        
def seo_rival(content):
    try:
        response = openai_api_call(
        "gpt-4-turbo-preview",
        0,
        [
            {"role": "system", "content": "あなたは優秀なSEO分析コンサルタントです。提供された内容から、SEOの要点を抽出してください。"},
            {"role": "user", "content": content}
        ],
        4000,  # リード文の最大トークン数を適宜設定
        {"type": "text"}
        )
        return response
    except Exception as e:
        print(f"SEO要点抽出中にエラーが発生しました: {e}")
        raise e







# assistant APIは一旦保留。現行の実装内容では使いづらいため。
'''
# assistantは先に作成しておくこと。作成済み。
OpenAI_assistant_id = os.environ["assistant_id"]

def feleimport(file_path):
    try:
        # ファイルをOpenAIにアップロードする
        uploaded_file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants",
        )
        file_id = uploaded_file.id
        print(file_id)
        # スレッドを作成する
        try:
            empty_thread = client.beta.threads.create()
            thread_id = empty_thread.id
            print(thread_id)
            # スレッドにファイルをインポートする

        except Exception as e:
            print(f"スレッドの作成中にエラーが発生しました: {e}")
            raise e
    except Exception as e:
        print(f"ファイルのインポート中にエラーが発生しました: {e}")
        raise e
'''     


