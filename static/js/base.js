

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