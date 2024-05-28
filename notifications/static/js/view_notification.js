document.addEventListener("DOMContentLoaded", () => {
    let actionMenu = document.querySelector(".view-notification-action-menu-btn");
    let sku = actionMenu.getAttribute("data-sku");
    let item = document.querySelector(`.item-wrapper[data-sku="${sku}"]`);
    listenForBtnClicks(actionMenu, item);
});

let notificationDeleted = () => {
    let container = document.querySelector(".view-notification-container");

    let notificationOverlay = document.createElement("div");

    notificationOverlay.classList.add("notification-deleted-overlay");

    notificationOverlay.innerHTML = `
        <p class="dark-text subheading">Notification Deleted!</p>
        <a class="visit-link" href="/">
            <p class="dark-text-2">Return Home</p>
            <span class="icon-container btn-icon-right">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text-2" viewBox="0 0 16 16">
                    <path d="M1.22 6.28a.75.75 0 0 1 0-1.06l3.5-3.5a.749.749 0 1 1 1.06 1.06L3.561 5h7.188l.001.007L10.749 5q.088 0 .171.019A4.501 4.501 0 0 1 10.5 14H8.796a.75.75 0 0 1 0-1.5H10.5a3 3 0 1 0 0-6H3.561L5.78 8.72a.749.749 0 1 1-1.06 1.06z" />
                </svg>
            </span>
        </a>
    `;

    container.classList.add('deleted');

    container.appendChild(notificationOverlay);
}