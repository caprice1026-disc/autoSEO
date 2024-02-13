import json
import os
import requests
from bs4 import BeautifulSoup
from backend.openaiapi import seo_rival
from googleapiclient.discovery import build

api_key = os.environ.get('GOOGLE_API_KEY')
cse_id = os.environ.get('GOOGLE_CSE_ID')

def update_system_prompt(system_prompt, previous_content):
    updated_prompt = f"{system_prompt}\n\n{previous_content}"
    return updated_prompt
    
def google_search(query, api_key=api_key, cse_id=cse_id, num_results=3):
    try:
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
    except requests.RequestException as e:
        print(f"検索中にエラーが発生しました: {e}")
        return []

# URLからコンテンツを取得する関数
def fetch_content_from_url(url):
    try:
        print(f"URLからコンテンツの取得を開始: {url}")

        # ユーザーエージェントを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers, timeout=10)
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
        for element in soup(['header', 'footer', 'style']):
            element.decompose()

        # HTMLからテキストを取得し、余分な空白を削除
        text = soup.get_text()
        parsed_text = ' '.join(text.split())

        # パースされたテキストの文字数を出力
        print(f"パースされたテキストの文字数: {len(parsed_text)}")
        return parsed_text

    except Exception as e:
        print(f"コンテンツのパース中にエラーが発生しました: {e}")
        return ""
    
def main(json_data):
    try:
        # section1の各内容を取得
        section1 = json_data['section1']
        keywords = section1['keywords']
        results = {}

        for keyword in keywords:
            urls = google_search(keyword)
            for url in urls:
                if url not in results:
                    content = fetch_content_from_url(url)
                    if content:
                        parsed_content = parse_content(content)  # コンテンツをパース
                        results[url] = [parsed_content]  # 新しいURLの場合、リストを初期化して追加
        # 既存のURLの場合、コンテンツを再度フェッチしてパースする必要はないため、この部分は削除します。


        # 結果を文字列として組み立て
        results_content = ""
        for url, content_list in results.items():
            results_content += f"URL: {url}\n"
            for content in content_list:
                results_content += f"{content}\n\n"
            results_content += "\n\n"

        # system_promptの生成
        seo_essense = seo_rival(results_content)
        expected_reader = section1['targetReader']
        search_intent = section1['searchIntent']
        goal = section1['goal']
        title = section1['title']
        system_prompt = (
        "あなたは優秀なSEOライター兼、コンテンツマーケターです。さらに、あなたはSEOの専門家であり、"
        f"すべてのSEOに関する知識を持っています。'{seo_essense}'を参考に、'{expected_reader}'向けの"
        f"'{search_intent}'の検索意図に適したコンテンツを作成してください。コンテンツの目的は'{goal}'で、"
        f"タイトルは'{title}'です。"
        )
        return system_prompt
        # ここまで問題なく動くのは確認済み
    except Exception as e:
        print(e)
        return "エラーが発生しました。"


            


    
# JSONデータの例。headline2のように、省略されている項目もある。headlineは各項目の見出しを表す。
'''
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