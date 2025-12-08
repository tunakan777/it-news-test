// 将来的にJSONデータを読み込む処理をここに追加

// 例: JSONからデータを取得して表示する関数
async function loadArticles() {
    try {
        // バックエンドからJSONデータを取得
        const response = await fetch('/api/articles');
        const data = await response.json();
        
        // データを表示する処理
        displayArticles(data);
    } catch (error) {
        console.error('記事の取得に失敗しました:', error);
    }
}

function displayArticles(articles) {
    // 記事データをHTMLに反映する処理
    // 後で実装
    console.log('記事データ:', articles);
}

// ページ読み込み時の処理
document.addEventListener('DOMContentLoaded', function() {
    console.log('ページが読み込まれました');
    // loadArticles(); // JSONデータ取得が実装されたらコメント解除
});