document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addRowButton').addEventListener('click', addRow);
    document.getElementById('removeRowButton').addEventListener('click', removeRow);
    document.getElementById('seoForm').addEventListener('submit', submitForm);
});

function addRow() {
    const table = document.getElementById('headerTable');
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
        <td><textarea name="headerText"></textarea></td>
        <td><textarea name="headerCharCount" oninput="this.value=this.value.replace(/[^0-9]/g,'');"></textarea></td>
        <td><textarea name="headerSummary"></textarea></td>
        <td><textarea name="headerKeywords"></textarea></td>
        <td><textarea name="headerNotes"></textarea></td>
    `;
}

function removeRow() {
    const table = document.getElementById('headerTable');
    const rowCount = table.rows.length;
    if (rowCount > 1) { // 最初の行を除いて削除
        table.deleteRow(-1);
    }
}

function submitForm(event) {
    event.preventDefault();

    const textAreas = document.querySelectorAll('#seoForm textarea');
    const selects = document.querySelectorAll('#seoForm select');
    let isValid = true;
    let message = '';

    textAreas.forEach(textArea => {
        if (!textArea.value.trim()) {
            isValid = false;
        }
    });

    selects.forEach(select => {
        if (!select.value.trim()) {
            isValid = false;
        }
    });

    const messageDiv = document.getElementById('message');
    if (!isValid) {
        message = '未入力の箇所があります';
        messageDiv.style.color = 'red';
        messageDiv.textContent = message;
        return;
    }

    // データ収集と整形
    const jsonData = collectFormData();

    // データ送信
    fetch('/submit', {
        //POSTメソッドで送信
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    // レスポンスのJSONを解析
    .then(response => response.json())
    .then(data => {
        message = '送信されました';
        messageDiv.style.color = 'green';
        console.log('Success:', data);
    })
    // エラーが発見されたとき
    .catch((error) => {
        message = '送信中にエラーが発生しました';
        messageDiv.style.color = 'red';
        console.error('Error:', error);
    });

    messageDiv.textContent = message;
}

// フォームのデータを収集して整形する用の関数
function collectFormData() {
    // section1のデータを収集
    const section1 = {
        inputKeyword: document.getElementById('inputKeyword').value.trim(),
        inputTarget: document.getElementById('inputTarget').value.trim(),
        inputIntent: document.getElementById('inputIntent').value.trim(),
        inputGoal: document.getElementById('inputGoal').value.trim(),
        inputTitle: document.getElementById('inputTitle').value.trim()
    };

    // section2のデータを収集
    const section2 = {};
    const headers = document.querySelectorAll('#headerTable tr');
    headers.forEach((row, index) => {
        if (index > 0) { // 最初のヘッダー行を無視
            const headerData = {
                entry: row.querySelector('select[name="headerLevel"]').value,
                outline: row.querySelector('textarea[name="headerSummary"]').value.trim(),
                number_of_words: parseInt(row.querySelector('textarea[name="headerCharCount"]').value.trim()),
                must_KW: row.querySelector('textarea[name="headerKeywords"]').value.split(',').map(kw => kw.trim()),
                memo: row.querySelector('textarea[name="headerNotes"]').value.trim()
            };
            // 空のフィールドは含めない
            if (!headerData.must_KW.length) delete headerData.must_KW;
            if (!headerData.memo) delete headerData.memo;

            section2[`headline${index}`] = headerData;
        }
    });

    return { section1, section2 };
}
