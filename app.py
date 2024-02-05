from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import os
import json
from flask import Flask, request, jsonify, render_template, Response
from backend.main import main, generate_seo_content

app = Flask(__name__)
CORS(app)  # CORSを有効にする

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def events():
    json_data = request.get_json()
    system_prompt, user_prompts, _ = main(json_data)  # mainからプロンプトを取得

    def generate():
        # generate_seo_content関数からストリーミングされるコンテンツを送信
        content_stream = generate_seo_content(system_prompt, user_prompts)
        for content_chunk in content_stream:
            yield f"data: {json.dumps({'content': content_chunk})}\n\n"

    return Response(generate(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)

'''app.pyのjson_data = request.get_json()以下を修正すること。具体的には
json_data = request.get_json()をおこなったあと、section1を作成、その後はsection2からユーザープロンプトを生成する
繰り返し処理を行うことで、ユーザープロンプトを生成することができる。
そのように書き換えること。     


'''