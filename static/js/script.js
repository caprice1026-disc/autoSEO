function submitForm(event) {)
    event.preventDefault(); // デフォルトのフォーム送信を防止

    const form = event.target;
    const formData = new FormData(form);

    // FormDataオブジェクトからJSONオブジェクトを作成
    const formJSON = Object.fromEntries(formData.entries());

    // 入力検証
    let isValid = true; // 検証結果のフラグ
    const messageElement = document.getElementById('message');

    // URLが必須であり、かつ有効な形式であることを検証
    const urlPattern = /^https?:\/\/[^\s$.?#].[^\s]*$/i; // 簡単なURL形式のチェック
    if (!formJSON.websiteUrl || !urlPattern.test(formJSON.websiteUrl)) {
        isValid = false;
        messageElement.textContent = '有効なウェブサイトのURLを入力してください。';
        messageElement.style.color = 'red';
        form.querySelector('[name="websiteUrl"]').focus(); // 不正な入力にフォーカス
    }

    if (isValid) {
        // すべての入力が有効な場合、サーバーに送信
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formJSON),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('サーバーからの応答が不正です。');
            }
            return response.json();
        })
        .then(data => {
            messageElement.textContent = '送信に成功しました。ありがとうございます！';
            messageElement.style.color = 'green';
            form.reset(); // フォームをリセット
        })
        .catch(error => {
            messageElement.textContent = `送信に失敗しました: ${error.message}`;
            messageElement.style.color = 'red';
        });
    } else {
        // 入力検証に失敗した場合、ユーザーにフィードバックを提供し、修正を促す
        messageElement.textContent = '入力に問題があります。赤色のメッセージを確認してください。';
        messageElement.style.color = 'red';
    }
}
