function addRow() {
    const table2 = document.getElementById('table2');
    const newRow = table2.insertRow(table2.rows.length);
    for (let i = 0; i < 6; i++) {
        const cell = newRow.insertCell(i);
        if (i === 0) {
            const select = document.createElement('select');
            select.innerHTML = `
                <option value="h1">H1</option>
                <option value="h2">H2</option>
                <option value="h3">H3</option>
                <option value="h4">H4</option>
                <option value="h5">H5</option>
                <option value="h6">H6</option>
            `;
            cell.appendChild(select);
        } else {
            const input = document.createElement('input');
            input.type = 'text';
            input.value = '';
            cell.appendChild(input);
        }
    }
}

function removeRow() {
    //ここに間違いがあって変な挙動になってるかも
    const table2 = document.getElementById('table2');
    if (table2.rows.length > 1) {
        table2.deleteRow(table2.rows.length - 1);
    }
}

function submitForm() {
    let result = '';
    const inputs = document.querySelectorAll('.form-container input, .form-container select');
    inputs.forEach((input, index) => {
        //resultに足す必要がある
        result += input
　  });

    document.getElementById('result').textContent = result;
    document.getElementById('submit-message').textContent = '送信されました';
}

// ↓最終的にはこういったデータ形式で送信するようにしたい。

/*
{
  "section1": {
    "keyword": ["サンプルキーワード1", "サンプルキーワード2"],
    "expected_reader": "サンプル読者層",
    "search_intent": "情報提供",
    "goal": "読者の理解向上",
    "title": "サンプルタイトル"
  },
  "section2": {
    "entry": "サンプル項目",
    "headline": "サンプル見出し",
    "outline": "ここに概要が入ります",
    "number_of_words": 500,
    "must_KW": ["キーワード1", "キーワード2"],
    "memo": "ここにメモが入ります"
  }
}
*/