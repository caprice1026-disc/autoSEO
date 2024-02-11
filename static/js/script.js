// Socket.IOのインスタンスを作成
const socket = io();

// DOMが読み込まれた後にイベントリスナーを設定
document.addEventListener('DOMContentLoaded', function() {
    // 行の追加ボタンにイベントリスナーを追加
    document.getElementById('addRowButton').addEventListener('click', addRow);

    // 行の削除ボタンにイベントリスナーを追加
    document.getElementById('removeRowButton').addEventListener('click', removeTableRow);

    // フォーム送信時にsubmitForm関数を呼び出すイベントリスナーを追加
    document.getElementById('seoForm').addEventListener('submit', submitForm);
    // WebSocketの接続を初期化


    // サーバーからの応答をリッスン
    socket.on('response', function(data) {
        var outputFrame = document.getElementById('outputFrame');
        // 受け取ったデータ（チャンク）を含む新しいテキストノードを作成
        var newText = document.createTextNode(data.data);
        // テキストノードをoutput-frameに追加
        outputFrame.appendChild(newText);
    });

    // サーバーからのエラー応答をリッスン
    socket.on('error', function(data) {
        var outputFrame = document.getElementById('outputFrame');
        outputFrame.textContent = 'エラーが発生しました: ' + data.error;
        outputFrame.className = 'error';
    });
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
    
    inputs.forEach(function(input) {
        if (input.value.trim() === '') {
            isValid = false;
        }
    });

    var messageElement = document.getElementById('message');
    if (isValid) {
        messageElement.textContent = '送信されました。';
        messageElement.className = 'success'; // 成功メッセージのスタイルクラス
    } else {
        messageElement.textContent = '未入力の箇所があります。';
        messageElement.className = 'error'; // エラーメッセージのスタイルクラス
    }
    return isValid;
}

function submitForm(event) {
    event.preventDefault(); // 実際のフォーム送信を阻止
    if (validateForm(event)) { // フォームの検証が成功した場合にのみ送信を進める
        const keywords = document.getElementById('inputKeyword').value.split(',').map(keyword => keyword.trim());
        const targetReader = document.getElementById('inputTarget').value.trim();
        const searchIntent = document.getElementById('inputIntent').value.trim();
        const goal = document.getElementById('inputGoal').value.trim();
        const title = document.getElementById('inputTitle').value.trim();
        const description = document.getElementById('inputDescription').value.trim();
        
        // ヘッダー情報の収集...
        const headers = Array.from(document.getElementsByName('headerLevel[]'));
        const texts = Array.from(document.getElementsByName('headerText[]'));
        const charCounts = Array.from(document.getElementsByName('headerCharCount[]'));
        const summaries = Array.from(document.getElementsByName('headerSummary[]'));
        const keywordsInputs = Array.from(document.getElementsByName('headerKeywords[]'));
        const notes = Array.from(document.getElementsByName('headerNotes[]'));

        // セクションデータの構築...
        const section2 = headers.reduce((acc, header, index) => {
            const headlineKey = `headline${index + 1}`; // headline1, headline2, ...
            acc[headlineKey] = {
                level: header.value,
                text: texts[index].value.trim(),
                charCount: charCounts[index].value.trim(),
                summary: summaries[index].value.trim(),
                keywords: keywordsInputs[index].value.split(',').map(keyword => keyword.trim()),
                notes: notes[index].value.trim()
            };
            return acc;
        }, {});
        

        // JSONデータの構築
        const jsonData = {
            section1: {
                keywords,
                targetReader,
                searchIntent,
                goal,
                title,
                description
            },
            section2
        };

        // WebSocketを使用してサーバーにデータを送信
        socket.emit('send_data', jsonData);

        // 送信成功メッセージの表示
        document.getElementById('message').textContent = 'データが正常に送信されました。';
        document.getElementById('message').className = 'success';
    }
}