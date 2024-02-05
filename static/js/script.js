function submitForm(event) {
    event.preventDefault(); // フォームのデフォルト送信を防ぐ

    // フォームデータをJSON形式で準備
    const formData = {
        keywords: document.getElementById('inputKeyword').value.split(',').map(kw => kw.trim()), // キーワードを配列に変換
        targetReader: document.getElementById('inputTarget').value,
        searchIntent: document.getElementById('inputIntent').value,
        goal: document.getElementById('inputGoal').value,
        title: document.getElementById('inputTitle').value,
        description: document.getElementById('inputDescription').value,
        headers: Array.from(document.querySelectorAll('#headerTable tr')).slice(1).map(tr => { // 最初の行はヘッダーなので除外
            return {
                level: tr.querySelector('select[name="headerLevel[]"]').value,
                text: tr.querySelector('textarea[name="headerText"]').value,
                charCount: tr.querySelector('textarea[name="headerCharCount"]').value,
                summary: tr.querySelector('textarea[name="headerSummary"]').value,
                keywords: tr.querySelector('textarea[name="headerKeywords"]').value,
                notes: tr.querySelector('textarea[name="headerNotes"]').value
            };
        })
    };

    // バリデーションチェックなどが必要であればここで行う

    // フォームデータをサーバーに送信
    fetch('/sampleform-post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        // 成功時の処理
        document.getElementById('message').textContent = '送信に成功しました';
        document.getElementById('message').style.color = 'green';
    })
    .catch(error => {
        // エラー処理
        document.getElementById('message').textContent = '送信に失敗しました';
        document.getElementById('message').style.color = 'red';
        console.error('送信エラー:', error);
    });
}
