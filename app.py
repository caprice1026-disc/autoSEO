from flask import Flask, request, render_template, Response, jsonify, session
from flask_cors import CORS
import os
import json
from backend.main import main
from backend.openaiapi import openai_api_call


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)  # CORSを有効にする

@app.route('/')
def index():
    return render_template('index.html')

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
        # ストリーム処理を直接返す
        return response.iter_content()
    except Exception as e:
        # 例外が発生した場合の処理をここで直接実装
        def error_generator():
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        return error_generator()

@app.route('/submit', methods=['POST'])
def submit():
    # リクエストからJSONデータを取得
    json_data = request.get_json()
    # JSONデータを処理して、system_promptを生成
    try:
        session['json_data'] = json_data
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/stream_seo')
def stream_seo():
    json_data = session.get('json_data', None)
    if json_data is None:
        return jsonify(success=False, error="No JSON data found in session")
    # ここでストリーミング処理を実装
    def generate():
        system_prompt = ""
        e = None
        try:
            system_prompt = main(json_data)
            # JSONデータを処理して、user_promptを生成
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
                    f"{level}の部分の記事を作成します。記事の見出しは'{text}'で、文字数は'{charCount}'です。内容は'{summary}'です。"
                    f"記事内に、{', '.join(keywords)}を必ず含めてください。記事を書く際は、'{notes}'を意識してください。"
                    f"これ以前の内容はこのようになっています。'{previous_content}'これに整合性を合わせて書いてください。"
                )
                # OpenAI APIを呼び出して、SEO要点を生成
                seo_content = generate_seo_content(system_prompt, user_prompt)
                for content_chunk in seo_content:
                    content_data = json.loads(content_chunk.decode('utf-8').lstrip('data: '))
                    if 'content' in content_data['choices'][0]['delta']:
                        # コンテンツ値を含む応答チャンクを送信
                        content = content_data['choices'][0]['delta']['content']
                        # 現在のコンテンツをprevious_contentに追加
                        previous_content += content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                    if content_data['choices'][0].get('finish_reason') == "stop":
                        break
        except Exception as ex:
            # 例外が発生した場合の処理をここで直接実装
            e = ex
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    return Response(generate(), content_type='text/event-stream')

if __name__ == "__main__":
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