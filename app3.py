from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from backend.openaiapi import openai_api_call
from backend.main import main

app = Flask(__name__)
socketio = SocketIO(app)

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
                "text",
                True
            )

            # 応答をクライアントに送信
            for message in response:
                if 'choices' in message and message['choices']:
                    chunk = message['choices'][0].message.content
                    emit('response', {'data': chunk})

    except Exception as e:
        emit('error', {'error': str(e)})
        print(e)
if __name__ == '__main__':
    socketio.run(app, debug=True)