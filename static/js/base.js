document.addEventListener("DOMContentLoaded", () => {
    const profileContainer = document.querySelector(".profile-container");

    if (profileContainer) {
        let notificationBtn = profileContainer.querySelector(".notification-btn-container");
        let notificationBtnIcon = profileContainer.querySelector(".notification-btn-icon");
        let notificationMenu = profileContainer.querySelector(".notification-menu-container");

        notificationBtn.addEventListener("click", () => {
            notificationMenu.classList.toggle("show");

            notificationBtnIcon.classList.toggle("rotate");
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const profileContainer = document.querySelector(".profile-container");

    if (profileContainer) {
        let profileBtn = profileContainer.querySelector(".profile-btn-container");
        let profileBtnIcon = profileContainer.querySelector(".profile-btn-icon");
        let profileMenu = profileContainer.querySelector(".profile-menu-container");

        profileBtn.addEventListener("click", () => {
            profileMenu.classList.toggle("show");

            profileBtnIcon.classList.toggle("rotate");
        });
    }
});