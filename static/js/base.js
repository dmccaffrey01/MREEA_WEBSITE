let firstClick = true;
var clickedElement;

let toggleElementShow = (element) => {
    if (!(clickedElement == element && !firstClick)) {
        hideElements();
        addShowClass(element);
        firstClick = true;
        clickedElement = element;
        document.addEventListener("click", clickOutsideElementListener);
    }
}

let addShowClass = (element) => {
    element.classList.add("show");

    let parentWrapper = element.parentNode.closest(".wrapper-menu");
    if (parentWrapper) {
        addShowClass(parentWrapper);
    }
}

let clickOutsideElementListener = (e) => {
    let target = e.target;
    let targetWrapper = target.closest(".wrapper-menu");
    let clickedElementWrapper;
    let closeMessagesBtn = target.closest(".messages-close-btn-wrapper");

    if (clickedElement) {
        clickedElementWrapper = clickedElement.closest(".wrapper-menu");
    }
    
    let executeHide = () => {
        hideElements();
        document.removeEventListener("click", clickOutsideElementListener);
        
        let parentWrapper = getParentWrapper(targetWrapper, clickedElement);
        if (parentWrapper) {
            toggleElementShow(parentWrapper);
            firstClick = false;
        } else {
            clickedElement = null;
            firstClick = true;
        }
    }

    if (firstClick) {
        firstClick = false;
        return;
    }

    let targetBtn = target.closest(".wrapper-btn");

    if (targetBtn && !firstClick) {
        executeHide();
    }

    if (targetWrapper != clickedElementWrapper && !closeMessagesBtn) {
        executeHide();
    }
}

let getParentWrapper = (targetWrapper, clickedElement) => {

    let clickedElementWrapper = clickedElement.closest(".wrapper-menu");
    let clickedParentWrapper = clickedElementWrapper.parentNode.closest(".wrapper-menu");

    if (!clickedParentWrapper) {
        return false;
    }

    if (clickedParentWrapper == targetWrapper) {
        return clickedParentWrapper;
    }

    return getParentWrapper(targetWrapper, clickedParentWrapper);
}

let hideElements = () => {
    let showElements = document.querySelectorAll(".show");
    showElements.forEach(element => {
        element.classList.remove("show");
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const profileContainer = document.querySelector(".profile-container");

    if (profileContainer) {
        let profileBtn = profileContainer.querySelector(".profile-btn-container");
        let profileWrapper = profileContainer.querySelector(".profile-wrapper");

        let notificationBtn = profileContainer.querySelector(".notification-btn-container");
        let notificationWrapper = profileContainer.querySelector(".notification-wrapper");

        profileBtn.addEventListener("click", () => {
            toggleElementShow(profileWrapper);
        });

        notificationBtn.addEventListener("click", () => {
            toggleElementShow(notificationWrapper);
        });

        let notificationTypeBtns = document.querySelectorAll(".type-heading-container");

        notificationTypeBtns.forEach((btn) => {
            btn.addEventListener("click", () => {
                let classAtt = btn.getAttribute("data-class");
                if (classAtt == "new") {
                    notificationWrapper.classList.remove("show-cleared");
                    notificationWrapper.classList.add("show-new");
                } else {
                    notificationWrapper.classList.remove("show-new");
                    notificationWrapper.classList.add("show-cleared");
                }
            });
        });

        let notificationActionMenu = document.querySelector(".notification-action-menu-btn");

        let menuContainer = notificationActionMenu.querySelector(".action-menu-container");

        notificationActionMenu.addEventListener("click", () => {
            toggleElementShow(menuContainer);
        });
    }
});