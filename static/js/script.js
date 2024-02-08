// DOMが読み込まれた後にイベントリスナーを設定
document.addEventListener('DOMContentLoaded', function() {
    // 行の追加ボタンにイベントリスナーを追加
    document.getElementById('addRowButton').addEventListener('click', addRow);

    // 行の削除ボタンにイベントリスナーを追加
    document.getElementById('removeRowButton').addEventListener('click', removeTableRow);

    // フォーム送信時の検証イベントリスナーを追加
    document.getElementById('seoForm').addEventListener('submit', validateForm);
});

// テーブル行を追加する関数
function addRow() {
    const table = document.getElementById('headerTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>
            <select name="headerLevel[]">
                <option value="h1">H1</option>
                <option value="h2">H2</option>
                <option value="h3">H3</option>
                <option value="h4">H4</option>
                <option value="h5">H5</option>
                <option value="h6">H6</option>
            </select>
        </td>
        <td><textarea name="headerText[]"></textarea></td>
        <td><textarea name="headerCharCount[]" oninput="this.value=this.value.replace(/[^0-9]/g,'');"></textarea></td>
        <td><textarea name="headerSummary[]"></textarea></td>
        <td><textarea name="headerKeywords[]"></textarea></td>
        <td><textarea name="headerNotes[]"></textarea></td>
    `;
}

// テーブル行を削除する関数
function removeTableRow() {
    var table = document.getElementById('headerTable').getElementsByTagName('tbody')[0];
    var rowCount = table.rows.length;
    if (rowCount > 0) { // 少なくとも1行が存在する場合のみ削除
        table.deleteRow(-1);
    }
}

// フォーム検証関数
function validateForm(event) {
    event.preventDefault(); // 実際のフォーム送信を阻止

    var isValid = true; // フォームが有効かどうかを追跡するフラグ
    var inputs = document.querySelectorAll('#seoForm input[type="text"], #seoForm textarea');
    
    // 入力フィールドの検証
    inputs.forEach(function(input) {
        if (input.value.trim() === '') {
            isValid = false;
        }
    });

    // 検証結果に基づいてフィードバックをユーザーに表示
    var messageElement = document.getElementById('message');
    if (isValid) {
        messageElement.textContent = '送信されました。';
        messageElement.className = 'success'; // 成功メッセージのスタイルクラス
    } else {
        messageElement.textContent = '未入力の箇所があります。';
        messageElement.className = 'error'; // エラーメッセージのスタイルクラス
    }
}
