const box = document.getElementById('box');
const mes = document.getElementById('message');
const btn = document.getElementById('button');
const data = { goal: "", level: "" };

window.onload = function () {
    addBox("目標を入力してください", "bot");
};

function addBox(text, type = "bot") {
    const div = document.createElement('div');
    div.className = 'message ' + type;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

function removeBtns() {
    document.querySelectorAll('.level-btn').forEach(btn => btn.remove());
}

function addBtn() {
    removeBtns();
    const levels = [
        { label: 'やさしい', value: 'easy' },
        { label: 'ふつう', value: 'normal' },
        { label: 'むずかしい', value: 'difficult' },
        { label: 'ランダム', value: '' }
    ];
    levels[3].value = randomValue()
    levels.forEach(level => {
        const button = document.createElement('button');
        button.textContent = level.label;
        button.className = 'level-btn';
        button.onclick = function () {
            data.level = level.value;
            removeBtns();
            addBox(level.label, "user");
            toServer(data);
        };
        box.appendChild(button);
    });
    box.scrollTop = box.scrollHeight;
}

function toServer(data) {
    addBox("これが今日の日課はこれです！！");

    fetch('./index', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(res => {
            addBox(res.sentence1, "bot");
            addBox(res.sentence2, "bot");
            addBox(res.sentence3, "bot");
        })
        .catch(error => {
            console.error('Error:', error);
            addBox("エラーが発生しました。サーバーと通信できません。", "bot");
        });
}

function randomValue() {
    const values = ["easy", "normal", "difficult"];
    const idx = Math.floor(Math.random() * values.length);
    return values[idx];
}

btn.onclick = function () {
    const message = mes.value.trim();
    if (!message) return;
    addBox(message, "user");
    data.goal = message;
    mes.value = '';
    addBox("難易度を選択してください", "bot");
    addBtn();
};