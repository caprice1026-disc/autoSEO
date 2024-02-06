from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import os
import json
from backend.main import main
app = Flask(__name__)
CORS(app)  # CORSを有効にする
from backend.openaiapi import openai_api_call


@app.route('/')
def index():
    return render_template('index.html')

def send_streamed_content(content_stream):
    try:
        for content_chunk in content_stream:
            content_data = json.loads(content_chunk.decode('utf-8').lstrip('data: '))
            yield f"data: {json.dumps({'content': content_data['choices'][0]['delta']['content']})}\n\n"
            if content_data.get('choices')[0].get('finish_reason') == "stop":
                break
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

def generate_seo_content(system_prompt, user_prompt):
    try:
        response = openai_api_call(
            "gpt-4-turbo-preview",
            0,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            4000,  # リード文の最大トークン数を適宜設定
            {"type": "text"},
            stream = True
        )
 # send_streamed_content 関数を呼び出してストリームを処理
        return send_streamed_content(response.iter_content())
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.route('/submit', methods=['POST'])
def submit():
    # リクエストからJSONデータを取得
    json_data = request.get_json()
    def stream_seo_content():
    # JSONデータを処理して、system_promptを生成
        try:
            system_prompt = main(json_data)
            # JSONデータを処理して、user_promptを生成
            section2 = json_data['section2']
            for headline_key, headline_value in section2.items():
                level = headline_value['level']
                text = headline_value['text']
                charCount = headline_value['charCount']
                summary = headline_value['summary']
                keywords = headline_value['keywords']
                notes = headline_value['notes']
                user_prompt = (
                f"{level}の部分の記事を作成します。記事の見出しは'{text}'で、文字数は'{charCount}'です。内容は'{summary}'です。"
                f"記事内に、{', '.join(keywords)}を必ず含めてください。記事を書く際は、'{notes}'を意識してください。"
                f"これ以前の見出しはこのようになっています。ない場合もあります。これに整合性を合わせて書いてください。"
                )
                # 各ヘッドラインの開始を示すタグを送信
                yield f"data: {json.dumps({'content': f'<{level}>{text}</{level}>'})}\n\n"        
                # OpenAI APIを呼び出して、SEO要点を生成
                seo_content = generate_seo_content(system_prompt, user_prompt)
                for content_chunk in seo_content:
                    content_data = json.loads(content_chunk.decode('utf-8').lstrip('data: '))
                    if 'content' in content_data['choices'][0]['delta']:
                        # コンテンツ値を含む応答チャンクを送信
                        content = content_data['choices'][0]['delta']['content']
                        yield f"data: {json.dumps({'content': content})}\n\n"
                    if content_data['choices'][0].get('finish_reason') == "stop":
                        break    
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    # stream_seo_contentジェネレータからのストリーミング出力をクライアントに送信
    return Response(stream_seo_content(), content_type='text/event-stream')  


if __name__ == "__main__":
    app.run(debug=True)

'''app.pyのjson_data = request.get_json()以下を修正すること。具体的には
json_data = request.get_json()をおこなったあと、section1を作成、その後はsection2からユーザープロンプトを生成する
繰り返し処理を行うことで、ユーザープロンプトを生成することができる。
そのように書き換えること。     


'''