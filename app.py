from flask import Flask, render_template
import json   

app = Flask(__name__)

@app.route("/")
def home():
    # JSONファイルを読み込む
    try:
        with open('hatena_ranking.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        # 上位3件だけ取得
        top_articles = articles[:3]
    except FileNotFoundError:
        # JSONファイルがない場合は空リスト
        top_articles = []
    
    # HTMLにデータを渡す
    return render_template("index.html", articles=top_articles)
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ranking")
def ranking():
    return render_template("ranking.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)