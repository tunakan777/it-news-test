from flask import Flask, render_template, jsonify
import json
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open('hatena_ranking.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        top_articles = articles[:3]
    except FileNotFoundError:
        top_articles = []
    
    return render_template("index.html", articles=top_articles)

@app.route('/update', methods=['POST'])
def update_data():
    try:
        # バックグラウンドで実行（待たずに即座に成功を返す）
        subprocess.Popen([sys.executable, 'main.py'])
        return jsonify({'status': 'success', 'message': 'バックグラウンドで更新開始'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

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