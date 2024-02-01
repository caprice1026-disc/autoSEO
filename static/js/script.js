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
    if (isValid) {
        message = '送信されました';
        messageDiv.style.color = 'green';
    } else {
        message = '未入力の箇所があります';
        messageDiv.style.color = 'red';
    }

    messageDiv.textContent = message;
}