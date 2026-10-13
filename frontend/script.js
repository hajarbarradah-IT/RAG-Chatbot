const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
    const question = input.value.trim();
    if (!question) return;

    // Message utilisateur
    chatBox.innerHTML += `<div class="user-msg">Toi : ${question}</div>`;

    // 🔹 VIDER LE CHAMP TEXTE
    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    // Appel backend
    const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    // Message bot
    chatBox.innerHTML += `<div class="bot-msg">Chatbot : ${data.answer}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
