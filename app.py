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
        # main.pyを実行
        result = subprocess.run(
            [sys.executable, 'main.py'],  # sys.executableで現在のPythonパスを使用
            capture_output=True,
            text=True,
            timeout=60  # 60秒でタイムアウト
        )
        
        # 実行結果をログ出力
        print("=== main.py 実行結果 ===")
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        print("return code:", result.returncode)
        
        if result.returncode == 0:
            return jsonify({'status': 'success'})
        else:
            return jsonify({
                'status': 'error',
                'error': f'main.py実行エラー: {result.stderr}'
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'error': 'タイムアウト: main.pyの実行に60秒以上かかりました'
        }), 500
    except FileNotFoundError:
        return jsonify({
            'status': 'error',
            'error': 'main.pyが見つかりません'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

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