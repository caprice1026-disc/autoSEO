from flask import Flask, request, jsonify, render_template, Response, session
from flask_session import Session  # Flask-Sessionをインポート
from backend.openaiapi import openai_api_call
from backend.main import main
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)  # 24バイトのランダムなキーを生成
app.config["SESSION_PERMANENT"] = False  # セッションをブラウザを閉じたら破棄
app.config["SESSION_TYPE"] = "filesystem"  # セッションをファイルシステムに保存
Session(app)  # セッションをアプリケーションに登録

@app.route('/')
def index():
    session["responses"] = []  # セッションでresponsesリストを初期化
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    json_data = request.json  # POSTリクエストのボディを取得
    try:
        system_prompt = main(json_data)
        section2 = json_data['section2']
        previous_content = ""

        responses = []  # 応答を格納するためのリスト

        for headline_key, headline_value in section2.items():
            level = headline_value['level']
            text = headline_value['text']
            charCount = headline_value['charCount']
            summary = headline_value['summary']
            keywords = headline_value['keywords']
            notes = headline_value['notes']
            user_prompt = (
                f"{level}の部分の記事を作成します。記事の見出しは'{text}'で、文字数は'{charCount}'です。"
                f"内容は'{summary}'です。記事内に、{', '.join(keywords)}を必ず含めてください。"
                f"記事を書く際は、'{notes}'を意識してください。これ以前の内容はこのようになっています。'{previous_content}'"
                f"これに整合性を合わせて書いてください。"
                f"'''HTML記法やMD記法を使わず、プレーンテキストで書いてください'''"
            )
            responses.append({'midashi': text, 'prompt': user_prompt})
        session["responses"] = responses  # セッションにresponsesリストを保存
        session["system_prompt"] = system_prompt
        return jsonify({"message": "データを受け取り、処理が開始されました。"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# サーバーサイドイベントを送信するエンドポイント
@app.route('/events')
def events():
    responses = session.get("responses", [])
    system_prompt = session.get("system_prompt", "")
    return Response(generate(responses, system_prompt), mimetype='text/event-stream')

def generate(responses, system_prompt):
    model = "gpt-4-turbo-preview"
    temperature = 0.5
    max_tokens = 4000
    response_format = {"type": "text"}
    stream = True  # ストリーミング応答を有効化

    for response in responses:
        yield f"data: {json.dumps({'midashi': response['midashi'], 'content': '見出し: ' + response['midashi']})}\n\n"
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": response['prompt']}]
        completion = openai_api_call(model, temperature, messages, max_tokens, response_format, stream)
        for chunk in completion:  # ストリーミング応答をイテレート
            yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"


            

if __name__ == '__main__':
    app.run(debug=True)

'''openai_api_call関数を呼び出しているが、これらはストリームのオンオフについての違いがある。
ストリームのオンオフを定義するためには、openai_api_call関数にstream引数を追加し、他の引数と同様にデフォルト値を設定する。
デフォルト値はFalseに設定する。この引数を呼び出し元の関数に渡すことで、ストリームのオンオフを制御することができる。
値の入力がない場合は、デフォルト値が適用されるようにすること。

現在のフロントエンドからの出力はこれ

{
  "section1": {
    "keywords": ["キーワード1", "キーワード2"],
    "targetReader": "ターゲットリーダーの値",
    "searchIntent": "検索意図の値",
    "goal": "目標の値",
    "title": "タイトルの値",
    "description": "説明の値"
  },
  "section2": {
    "headline1": {
      "level": "h1",
      "text": "ヘッダーテキスト1",
      "charCount": "文字数1",
      "summary": "要約1",
      "keywords": ["キーワードA", "キーワードB"],
      "notes": "ノート1"
    },
    "headline2": {
      "level": "h2",
      "text": "ヘッダーテキスト2",
      "charCount": "文字数2",
      "summary": "要約2",
      "keywords": ["キーワードC", "キーワードD"],
      "notes": "ノート2"
    }
  }
}


'''