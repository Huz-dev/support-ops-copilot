const messages = document.getElementById("chatMessages");
const input = document.getElementById("chatInput");
const button = document.getElementById("sendChat");

button.addEventListener("click", sendMessage);

input.addEventListener("keypress", function(e){

    if(e.key==="Enter"){
        sendMessage();
    }

});

async function sendMessage() {

    const message = chatInput.value.trim();

    if (!message) return;

    addBubble(message, "user");

    chatInput.value = "";

    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });

    const data = await response.json();

    addBubble(data.reply, "ai");

}
function addBubble(text, type){

    const bubble = document.createElement("div");

    bubble.className = type;

    bubble.innerHTML = `
        <div class="avatar">
            ${type==="ai" ? "🤖" : "🧑"}
        </div>

        <div class="message">
            ${text.replace(/\n/g,"<br>")}
        </div>
    `;

    chatMessages.appendChild(bubble);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}