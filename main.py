# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
import time
from file_handler import save_to_json

# はてなブックマークのURL
URL = "https://b.hatena.ne.jp/hotentry/it"

# 訪問の連絡呪文
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("はてなブックマークにアクセス中...")
response = requests.get(URL, headers=headers)

# タグを見やすい形に
soup = BeautifulSoup(response.content, "html.parser")

# 記事１個ずつの箱を、全部見つけ出す
entries = soup.find_all("li", class_="cat-it")

# ぜんぶの情報を貯めておくための、空っぽのリストを用意
ranking_data = [] 

print(f"\n{len(entries)}件の記事を取得しました。処理開始！\n")

# forループで、箱を一個ずつ見ていく
for idx, entry in enumerate(entries, 1):
    
    # h3タグを探す
    h3_tag = entry.find("h3", class_="entrylist-contents-title")
    
    # もし、h3タグが見つかったら…
    if h3_tag:
        # h3タグの中から、aタグを探す！
        a_tag = h3_tag.find("a")
        
        # もし、aタグが見つかったら…
        if a_tag:
            # <a>タグから、「title（記事のタイトル）」を引っこ抜く
            title = a_tag.get("title")
            
            # <a>タグから、「href（記事のリンク）」を引っこ抜く
            link = a_tag.get("href")
            
            # ブックマーク数を抜いてくる
            users_span = entry.find("span", class_="entrylist-contents-users")
            
            # エラーを起こさないように
            if users_span:
                users_text = users_span.find("a").find("span").text
                hatebu_count = int(users_text.replace(" users", ""))
            else:
                hatebu_count = 0
            
            # 投稿日時を抜いてくる
            data_li = entry.find("li", class_="entrylist-contents-date")
            
            if data_li:
                published_date = data_li.text.strip()
            else:
                published_date = ""
            
            # データを辞書にまとめる
            article_data = {
                "title": title,
                "link": link,
                "hatebu_count": hatebu_count,
                "published_date": published_date
            }
            
            # 🔥 ここが重要！ ranking_dataに追加する
            ranking_data.append(article_data)
            
            # 画面表示
            print(f"[{idx}] タイトル: {title}")
            print(f"    リンク: {link}")
            print(f"    ブックマーク数: {hatebu_count}")
            print(f"    公開日: {published_date}")
            print("--------------------")

# 最終チェック！
print("\n--- 🔥🔥🔥最終チェック！ranking_dataの中身はこれだ！🔥🔥🔥 ---")
print(f"取得した記事数: {len(ranking_data)}件")
print(ranking_data)

# 最後に、一回だけ、ファイル操作のプロを呼び出す！
print("\nJSONファイルに保存中...")
save_to_json(ranking_data)
print("✅ 完了！")