import json
import flask
import os
import requests
from bs4 import BeautifulSoup

api_key = os.environ.get('GOOGLE_API_KEY')
cse_id = os.environ.get('GOOGLE_CSE_ID')

def process_json(json_data):
    try:
        section1 = json_data['section1']
        section2 = json_data['section2']
        main(section1, section2)
    except Exception as e:
        print(e)
        raise e  # 例外を再度発生させる
    
def google_search(query, api_key, cse_id, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key,
        'num': num_results
    }
    response = requests.get(url, params=params)
    result = response.json()
    # 結果をリスト形式で返す。各要素は検索結果のURL
    return [item['link'] for item in result.get('items', [])]

# URLからコンテンツを取得する関数
def fetch_content_from_url(url):
    try:
        print(f"URLからコンテンツの取得を開始: {url}")

        # ユーザーエージェントを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers, timeout=30)
        content = response.text

        print(f"URLからコンテンツの取得が成功: {url}")
        return content

    except Exception as e:
        print(f"URLからのコンテンツ取得中にエラーが発生しました: {e}")
        return ""
    
def parse_content(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')

        # ヘッダー、フッター、スクリプト、スタイルの削除
        for element in soup(['header', 'footer']):
            element.decompose()

        text = soup.get_text()
        parsed_text = ' '.join(text.split())

        print(f"パースされたテキストの文字数: {len(parsed_text)}")
        return parsed_text

    except Exception as e:
        print(f"コンテンツのパース中にエラーが発生しました: {e}")
        return ""
    
def main(section1, section2):
    keywords = section1['キーワード']
    results = {}

    for keyword in keywords:
        urls = google_search(keyword, api_key, cse_id)
        contents = []

        for url in urls:
            content = fetch_content_from_url(url)
            if content:
                parsed_content = parse_content(content)
                contents.append(parsed_content)

        results[url] = contents
    
    print(results)

    
# JSONデータの例
'''
{
  "section1": {
    "キーワード": ["サンプルキーワード1", "サンプルキーワード2"],
    "想定される読者": "サンプル読者層",
    "検索意図": "情報提供",
    "ゴール": "読者の理解向上",
    "タイトル": "サンプルタイトル"
  },
  "section2": {
    "項目": "サンプル項目",
    "見出し": "サンプル見出し",
    "概要": "ここに概要が入ります",
    "文字数": 500,
    "必須KW": ["キーワード1", "キーワード2"],
    "メモ": "ここにメモが入ります"
  }
}
'''