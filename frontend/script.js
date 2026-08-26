async function sendMessage() {

    const input = document.querySelector(".chat-input input");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Show user's message
    addMessage(message, "user");

    // Clear input
    input.value = "";

    // Show loading message
    addMessage("Thinking...", "bot");

    try {

        const response = await fetch("http://127.0.0.1:8000/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        if (!response.ok) {
            throw new Error("API request failed");
        }


        const data = await response.json();


        // Remove "Thinking..."
        removeThinkingMessage();


        // Show AI response
        addMessage(data.response, "bot");


    } catch (error) {

        console.error(error);

        removeThinkingMessage();

        addMessage(
            "Sorry, I couldn't connect to the AI assistant.",
            "bot"
        );
    }
}


function addMessage(text, sender) {

    const messages = document.querySelector(".messages");

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", sender);


    if (sender === "bot") {

        messageDiv.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="bubble">
                <p>${text}</p>
            </div>
        `;

    } else {

        messageDiv.innerHTML = `
            <div class="bubble">
                <p>${text}</p>
            </div>
        `;
    }


    messages.appendChild(messageDiv);


    // Scroll to latest message
    messages.scrollTop = messages.scrollHeight;
}


function removeThinkingMessage() {

    const messages = document.querySelector(".messages");

    const lastMessage = messages.lastElementChild;


    if (
        lastMessage &&
        lastMessage.textContent.includes("Thinking...")
    ) {

        lastMessage.remove();
    }
}
const input = document.querySelector(".chat-input input");

input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});