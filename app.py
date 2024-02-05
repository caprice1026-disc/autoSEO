from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import os
import json
from flask import Flask, request, jsonify, render_template, Response


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
    # 実際のアプリケーションでは、ここでデータベースの変更をリッスンするか、
    # 他の方法でリアルタイムデータを取得します。
    # 以下はデモ用の静的なイベントストリームです。
    yield "data: {}\n\n".format(json.dumps({"message": "Event started"}))
    # 例えば、外部APIからのレスポンスやアプリケーションの内部状態の更新など

@app.route('/events')
def events():
    return Response(generate_events(), mimetype='text/event-stream')

def generate_events():
    # 実際のアプリケーションでは、ここでデータベースの変更をリッスンするか、
    # 他の方法でリアルタイムデータを取得します。
    # 以下はデモ用の静的なイベントストリームです。
    yield "data: {}\n\n".format(json.dumps({"message": "Event started"}))
    # 例えば、外部APIからのレスポンスやアプリケーションの内部状態の更新など

@app.route('/events')
def events():
    return Response(generate_events(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)