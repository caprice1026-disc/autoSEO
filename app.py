from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import os
import json
from flask import Flask, request, jsonify, render_template, Response
from backend.main import process_json
app = Flask(__name__)
CORS(app)  # CORSを有効にする

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    json_data = request.get_json()
    return Response(process_json(json_data), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)

'''app.pyのjson_data = request.get_json()以下を修正すること。具体的には
json_data = request.get_json()をおこなったあと、section1を作成、その後はsection2からユーザープロンプトを生成する
繰り返し処理を行うことで、ユーザープロンプトを生成することができる。
そのように書き換えること。     


'''