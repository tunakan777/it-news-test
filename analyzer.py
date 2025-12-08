# Janomeをインポート
from janome.tokenizer import Tokenizer

# ワードリスト
KAMI_WORDS = [
    'AWS', 'Azure', 'Google', 'Python', 'JavaScript', 'Java', 'React', 'Docker',
    'API', 'サーバー', 'セキュリティ', 'データベース', 'リリース', '障害',
    'エンジニア', 'プログラミング', 'GitHub', 'Apple', 'Microsoft', 'Windows'
]

tokenizer = Tokenizer()

# --- ここが、うちらの最強の「お弁当箱（関数）」！ ---
def calculate_it_score(title):
    """
    記事のタイトルを受け取り、IT関連度をスコアリングして返す関数。
    """
    score = 0
    # Janomeでタイトルを単語に分解！
    for token in tokenizer.tokenize(title):
        # もし、分解した単語が「神ワードリスト」の中にあったら…
        if token.surface in KAMI_WORDS:
            score += 1 # スコアを１点プラス！
    return score