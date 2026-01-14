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
    import os
    try:
        # 現在のディレクトリを確認
        current_dir = os.getcwd()
        print(f"現在のディレクトリ: {current_dir}")
        
        # main.pyの存在確認
        main_py_exists = os.path.exists('main.py')
        print(f"main.py存在: {main_py_exists}")
        
        if not main_py_exists:
            return jsonify({
                'status': 'error',
                'error': f'main.pyが見つかりません。現在のディレクトリ: {current_dir}'
            }), 500
        
        # main.pyを実行
        result = subprocess.run(
            [sys.executable, 'main.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("=== main.py 実行結果 ===")
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        print("return code:", result.returncode)
        
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': result.stdout})
        else:
            return jsonify({
                'status': 'error',
                'error': result.stderr or 'Unknown error',
                'stdout': result.stdout
            }), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("エラー詳細:", error_detail)
        return jsonify({
            'status': 'error',
            'error': str(e),
            'detail': error_detail
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