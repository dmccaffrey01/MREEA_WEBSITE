/**
 * Messages Section
 */

let hideMessages = () => {
    let messagesContainer = document.querySelector(".messages-container");
    
    messagesContainer.classList.remove("fade");
    window.setTimeout(() => {
        messagesContainer.classList.remove("show");
    }, 600);
}

let showMessages = () => {
    let messagesContainer = document.querySelector(".messages-container");

    messagesContainer.classList.add("show");
    window.setTimeout(() => {
        messagesContainer.classList.add("fade");
    }, 10);

    let intervalCounter = 0;

    let hideMessageInterval = window.setInterval(() => {
        if (!messagesContainer.classList.contains("show")) {
            clearInterval(hideMessageInterval);
        } else if (intervalCounter >= 10) {
            hideMessages();
            clearInterval(hideMessageInterval);
        } else {
            intervalCounter += 0.1;
        }
    }, 100);
}


document.addEventListener("DOMContentLoaded", () => {
    let messagesDisplayContainer = document.querySelector(".messages-display-container");

    let allMessages = messagesDisplayContainer.querySelectorAll(".message-container");

    if (allMessages.length > 0) {
        showMessages();

        let messagesCloseBtn = document.querySelector(".messages-close-btn");

        messagesCloseBtn.addEventListener("click", () => {
            hideMessages();
        });
    }
});