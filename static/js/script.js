// テーブル行を追加する関数
function addTableRow() {
    var table = document.getElementById('headerTable'); // テーブルの要素を取得
    var newRow = table.insertRow(-1); // 新しい行をテーブルの最後に追加
    newRow.innerHTML = `
        <td><select name="headerLevel">
            <option value="h1">H1</option>
            <option value="h2">H2</option>
            <option value="h3">H3</option>
            <option value="h4">H4</option>
            <option value="h5">H5</option>
            <option value="h6">H6</option>
        </select></td>
        <td><textarea name="headerText" placeholder="見出しテキスト"></textarea></td>
        <td><textarea name="headerCharCount" placeholder="例: 120" oninput="this.value=this.value.replace(/[^0-9]/g,'');"></textarea></td>
        <td><textarea name="headerSummary" placeholder="記事の簡潔な要約"></textarea></td>
        <td><textarea name="headerKeywords" placeholder="SEOキーワード"></textarea></td>
        <td><textarea name="headerNotes" placeholder="その他のメモ"></textarea></td>
    `;
}

// テーブル行を削除する関数
function removeTableRow() {
    var table = document.getElementById('headerTable'); // テーブルの要素を取得
    var rowCount = table.rows.length; // テーブルの行数を取得
    if (rowCount > 1) { // ヘッダー行以外に行が存在する場合のみ削除
        table.deleteRow(-1); // テーブルの最後の行を削除
    }
}

// イベントリスナーを追加
document.getElementById('addRowButton').addEventListener('click', addTableRow); // `+` ボタンがクリックされたとき
document.getElementById('removeRowButton').addEventListener('click', removeTableRow); // `-` ボタンがクリックされたとき








function validateForm(event) {
    event.preventDefault(); // フォームの実際の送信を阻止

    // 必須フィールドの値を取得
    var inputKeyword = document.getElementById('inputKeyword').value.trim();
    var inputTarget = document.getElementById('inputTarget').value.trim();
    var inputIntent = document.getElementById('inputIntent').value.trim();
    var inputGoal = document.getElementById('inputGoal').value.trim();
    var inputTitle = document.getElementById('inputTitle').value.trim();
    var inputDescription = document.getElementById('inputDescription').value.trim();
    
    // テーブル内の全ての必須入力欄を取得
    var headerInputs = document.querySelectorAll('textarea[name="headerText"]');
    var headerKeywords = document.querySelectorAll('textarea[name="headerKeywords"]');

    var messageElement = document.getElementById('message');
    var isValid = true; // 全てのフィールドが有効かどうかのフラグ

    // 各入力フィールドが空でないか検証
    if (!inputKeyword || !inputTarget || !inputIntent || !inputGoal || !inputTitle || !inputDescription) {
        isValid = false; // いずれかのフィールドが空
    }

    // テーブル内の見出しテキストと必須キーワードが空でないか検証
    headerInputs.forEach(function(input) {
        if (!input.value.trim()) {
            isValid = false; // 見出しテキストが空
        }
    });

    headerKeywords.forEach(function(keyword) {
        if (!keyword.value.trim()) {
            isValid = false; // 必須キーワードが空
        }
    });

    // 検証結果に基づいてメッセージを表示
    if (isValid) {
        messageElement.textContent = '送信されました';
        messageElement.style.color = 'green';
    } else {
        messageElement.textContent = '未入力の箇所があります';
        messageElement.style.color = 'red';
    }
}

// フォーム検証イベントリスナーを追加
document.getElementById('seoForm').addEventListener('submit', validateForm);
