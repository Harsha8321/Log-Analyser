document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const fileInput = document.getElementById("file-input");
    const uploadButton = document.getElementById("upload-btn");

    sendButton.addEventListener("click", function() {
        sendMessage();
    });

    userInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    uploadButton.addEventListener("click", function() {
        fileInput.click();
    });

    fileInput.addEventListener("change", function() {
        const file = fileInput.files[0];
        if (file) {
            uploadFile(file);
        }
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage !== "") {
            appendMessage("You:", userMessage);
            userInput.value = "";
            // Simulate bot response (replace with actual bot logic)
            setTimeout(function() {
                appendMessage("Stealth Bot:", "Generated Insights will be Inserted Here");
            }, 500);
        }
    }

    function uploadFile(file) {
        // You can handle the file upload logic here
        appendMessage("You:", `Uploaded file: ${file.name}`);
    }

    function appendMessage(prompt, response) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container");

        const promptElement = document.createElement("div");
        promptElement.textContent = prompt;
        promptElement.classList.add("prompt");
        messageContainer.appendChild(promptElement);

        const responseElement = document.createElement("div");
        responseElement.textContent = response;
        responseElement.classList.add("response");
        messageContainer.appendChild(responseElement);

        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
