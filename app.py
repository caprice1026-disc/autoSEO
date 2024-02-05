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
def submit():
    try:
        json_data = request.get_json()
        print(json_data)
        main(json_data)  # JSONデータを処理する関数を呼び出す
        return jsonify({"message": "JSON processed successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

def generate_events():
    yield "data: {}\n\n".format(json.dumps({"message": "Event started"}))
    # generate_seo_contentからのレスポンスをイベントストリームとしてクライアントに送信
    for event_data in generate_seo_content("Example system prompt", "Example user prompt"):
        # generate_seo_content関数から受け取ったデータをそのままクライアントに送信
        yield event_data

@app.route('/events')
def events():
    return Response(generate_events(), mimetype='text/event-stream')
if __name__ == "__main__":
    app.run(debug=True)