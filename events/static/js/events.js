eventContainers = document.querySelectorAll(".event-container");

eventContainers.forEach(event => {
    event.addEventListener("click", () => {
        let id = event.getAttribute("data-event-id");

        let currentUrl = new URL(window.location);

        currentUrl.pathname = `events/event/${id}`;

        window.location.replace(currentUrl);
    });
});