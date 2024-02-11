from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from backend.openaiapi import openai_api_call
from backend.main import main

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_data')
def handle_send_data(json_data):
    try:
        system_prompt = main(json_data)
        section2 = json_data['section2']
        previous_content = ""

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
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            # OpenAI APIを呼び出し（この部分は適宜書き換える）
            response = openai_api_call(
                "gpt-4-turbo-preview",
                0,
                messages,
                4000,  # リード文の最大トークン数を適宜設定
                {"type": "text"},
                True
            )

            # 応答をクライアントに送信
            for message in response:
                if 'choices' in message and message['choices']:
                    chunk = message['choices'][0].message.content
                    emit('response', {'data': chunk}, broadcast=True)

    except Exception as e:
        emit('error', {'error': str(e)})
        print(e)
if __name__ == '__main__':
    socketio.run(app, debug=True)

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