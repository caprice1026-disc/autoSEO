from flask_cors import CORS
import os
import json
from flask import Flask, request, jsonify, render_template
from markupsafe import escape
from backend.main import main
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)


