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

let listenForBtnClicks = (actionMenu, item) => {

    let parentWrapper = actionMenu.parentNode.closest(".wrapper-menu");

    if (item && actionMenu.parentNode.closest(".wrapper-menu")) {
        item.addEventListener("click", (e) => {
            let actionMenuBtn = actionMenu.parentNode.closest(".action-menu-btn");
            let target = e.target;
            let isActionItem = actionMenuBtn.contains(target);

            if (!isActionItem) {
                let sku = item.getAttribute("data-sku");
                viewNotification(sku);
            }
        });
    }

    let visitUrlBtn = actionMenu.querySelector(".visit-url-notification-btn");
    if (visitUrlBtn) {
        visitUrlBtn.addEventListener("click", () => {
            let sku = visitUrlBtn.getAttribute("data-sku");
            visitUrlNotification(sku);
        });
    }

    let viewBtn = actionMenu.querySelector(".view-notification-btn");
    if (viewBtn) {
        viewBtn.addEventListener("click", () => {
            let sku = viewBtn.getAttribute("data-sku");
            viewNotification(sku);
        });
    }

    let clearBtn = actionMenu.querySelector(".clear-notification-btn");
    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            let sku = clearBtn.getAttribute("data-sku");
            clearNotification(sku, item);
        });
    }

    let unclearBtn = actionMenu.querySelector(".unclear-notification-btn");
    if (unclearBtn) {
        unclearBtn.addEventListener("click", () => {
            let sku = unclearBtn.getAttribute("data-sku");
            unclearNotification(sku, item);
        });
    }

    let clearAllBtn = actionMenu.querySelector(".clear-all-notification-btn");
    if (clearAllBtn) {
        clearAllBtn.addEventListener("click", () => {
            let username = clearAllBtn.getAttribute("data-username");
            clearAllNotifications(username);
            toggleElementShow(parentWrapper);
        });
    }

    let unclearAllBtn = actionMenu.querySelector(".unclear-all-notification-btn");
    if (unclearAllBtn) {
        unclearAllBtn.addEventListener("click", () => {
            let username = unclearAllBtn.getAttribute("data-username");
            unclearAllNotifications(username);
            toggleElementShow(parentWrapper);
        });
    }

    let deleteBtn = actionMenu.querySelector(".confirm-delete-notification-btn");
    if (deleteBtn) {
        deleteBtn.addEventListener("click", () => {
            let sku = deleteBtn.getAttribute("data-sku");
            deleteNotification(sku, item);
        });
    }

    let deleteAllBtn = actionMenu.querySelector(".delete-all-notification-btn");
    if (deleteAllBtn) {
        deleteAllBtn.addEventListener("click", () => {
            let username = deleteAllBtn.getAttribute("data-username");
            deleteAllNotifications(username);
            toggleElementShow(parentWrapper);
        });
    }

}

let updateoriginalContainer = (originalContainer, originalContainerName) => {

    let items = originalContainer.querySelectorAll(".item-wrapper");

    let amountOfItems = items.length

    if (!amountOfItems > 0) {
        originalContainer.innerHTML = `
        <div class="no-item-wrapper item-wrapper container-row space-between">
            <div class="item-container container-row space-between">
                <p class="item-icon container-col">
                    <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                        <path fill-rule="evenodd" d="M20.207 6.793a1 1 0 0 1 0 1.414l-9.5 9.5a1 1 0 0 1-1.414 0l-4.5-4.5a1 1 0 0 1 1.414-1.414L10 15.586l8.793-8.793a1 1 0 0 1 1.414 0" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Check Circle Icon</span>
                </p>    
                <p class="item-heading dark-text small-text gap">No ${originalContainerName.charAt(0).toUpperCase() + originalContainerName.slice(1)} Notifications</p>
            </div>
        </div>
        `;
    }
    let newNotificationsItems = document.querySelector(".new-notifications-container").querySelectorAll(".item-wrapper")
    let amountOfNewItems = newNotificationsItems.length;
    if (amountOfNewItems == 1) {
        if (newNotificationsItems[0].classList.contains("no-item-wrapper")) {
            amountOfNewItems = 0;
        }
    }

    let notificationNumber = document.querySelector('.notification-number');
    notificationNumber.innerHTML = amountOfNewItems;

    let notificationBtnIcon = document.querySelector('.notification-btn-icon');
    if (amountOfNewItems == 0) {
        notificationBtnIcon.classList.add("hide");
    } else {
        if (notificationBtnIcon.classList.contains("hide")) {
            notificationBtnIcon.classList.remove("hide");
        }
    }
}

let moveNotification = (sku, item, originalContainerName, targetContainerName) => {

    let originalContainer = document.querySelector(`.${originalContainerName}-notifications-container`);

    if (targetContainerName == "deleted") {
        item.remove()
        updateoriginalContainer(originalContainer, originalContainerName);
        let newClickedElement = originalContainer.parentNode.closest(".wrapper-menu");
        toggleElementShow(newClickedElement);
        return;
    }
    let targetContainer = document.querySelector(`.${targetContainerName}-notifications-container`);
    let targetContainerNoItemWrapper = targetContainer.querySelector(".no-item-wrapper");
    // Change Item to match container
    let actionMenuContainer = item.querySelector(".action-menu-container");
    let urlName = item.getAttribute("data-url-name");
    if (targetContainerName == "new") {
        actionMenuContainer.innerHTML = `
        <div class="visit-url-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
                    <path d="M6.5 2a.5.5 0 0 0 0 1h5A1.5 1.5 0 0 1 13 4.5v7a1.5 1.5 0 0 1-1.5 1.5h-5a.5.5 0 0 0 0 1h5a2.5 2.5 0 0 0 2.5-2.5v-7A2.5 2.5 0 0 0 11.5 2zm3.354 5.646l-3-3a.5.5 0 1 0-.708.708L8.293 7.5H1.5a.5.5 0 0 0 0 1h6.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708" />
                </svg>
                <span class="sr-only">Visit Link Icon</span>
            </p>
            <p class="item-text dark-text small-text">Visit ${urlName}</p>
        </div>
        <div class="view-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
                    <path d="M2.984 8.625v.003a.5.5 0 0 1-.612.355c-.431-.114-.355-.611-.355-.611l.018-.062s.026-.084.047-.145a6.7 6.7 0 0 1 1.117-1.982C4.096 5.089 5.605 4 8 4s3.904 1.089 4.802 2.183a6.7 6.7 0 0 1 1.117 1.982a4 4 0 0 1 .06.187l.003.013v.004l.001.002a.5.5 0 0 1-.966.258l-.001-.004l-.008-.025l-.035-.109a5.7 5.7 0 0 0-.945-1.674C11.286 5.912 10.045 5 8 5s-3.285.912-4.028 1.817a5.7 5.7 0 0 0-.945 1.674l-.035.109zM8 7a2.5 2.5 0 1 0 0 5a2.5 2.5 0 0 0 0-5M6.5 9.5a1.5 1.5 0 1 1 3 0a1.5 1.5 0 0 1-3 0" />
                </svg>
                <span class="sr-only">View Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">View Notification</p>
        </div>
        <div class="clear-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path d="M12.003 21q-1.866 0-3.51-.708q-1.643-.709-2.859-1.924t-1.925-2.856T3 12.003t.709-3.51Q4.417 6.85 5.63 5.634t2.857-1.925T11.997 3t3.51.709q1.643.708 2.859 1.922t1.925 2.857t.709 3.509t-.708 3.51t-1.924 2.859t-2.856 1.925t-3.509.709M12 20q1.465 0 2.82-.514q1.357-.515 2.465-1.494L6.008 6.716q-.96 1.107-1.484 2.463T4 12q0 3.35 2.325 5.675T12 20m5.992-2.716q.98-1.107 1.493-2.463Q20 13.465 20 12q0-3.35-2.325-5.675T12 4q-1.471 0-2.834.505q-1.362.504-2.45 1.503z" />
                </svg>
                <span class="sr-only">Clear Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">Clear Notification</p>
        </div>
        `;
    } else {
        actionMenuContainer.innerHTML = `
        <div class="visit-url-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
                    <path d="M6.5 2a.5.5 0 0 0 0 1h5A1.5 1.5 0 0 1 13 4.5v7a1.5 1.5 0 0 1-1.5 1.5h-5a.5.5 0 0 0 0 1h5a2.5 2.5 0 0 0 2.5-2.5v-7A2.5 2.5 0 0 0 11.5 2zm3.354 5.646l-3-3a.5.5 0 1 0-.708.708L8.293 7.5H1.5a.5.5 0 0 0 0 1h6.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708" />
                </svg>
                <span class="sr-only">Visit Link Icon</span>
            </p>
            <p class="item-text dark-text small-text">Visit ${urlName}</p>
        </div>
        <div class="view-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
                    <path d="M2.984 8.625v.003a.5.5 0 0 1-.612.355c-.431-.114-.355-.611-.355-.611l.018-.062s.026-.084.047-.145a6.7 6.7 0 0 1 1.117-1.982C4.096 5.089 5.605 4 8 4s3.904 1.089 4.802 2.183a6.7 6.7 0 0 1 1.117 1.982a4 4 0 0 1 .06.187l.003.013v.004l.001.002a.5.5 0 0 1-.966.258l-.001-.004l-.008-.025l-.035-.109a5.7 5.7 0 0 0-.945-1.674C11.286 5.912 10.045 5 8 5s-3.285.912-4.028 1.817a5.7 5.7 0 0 0-.945 1.674l-.035.109zM8 7a2.5 2.5 0 1 0 0 5a2.5 2.5 0 0 0 0-5M6.5 9.5a1.5 1.5 0 1 1 3 0a1.5 1.5 0 0 1-3 0" />
                </svg>
                <span class="sr-only">View Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">View Notification</p>
        </div>
        <div class="unclear-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
                    <path fill-rule="evenodd" d="M55.265 167.072c-.975-1.973-3.388-2.796-5.372-1.847L42 169s22.5 53.5 85.5 56c60-1.5 96.627-48.626 97-96.5c.373-47.874-37-95.5-95.5-96c-57.5-1-79.556 45.004-79.556 45.004c-1.073 1.93-1.944 1.698-1.944-.501V51.997a4 4 0 0 0-4-3.997H37c-2.209 0-4 1.8-4 4.008v48.984A3.998 3.998 0 0 0 36.998 105h50.504a3.995 3.995 0 0 0 3.998-3.993v-6.014c0-2.205-1.79-4.02-4.008-4.053l-25.484-.38c-2.214-.033-3.223-1.679-2.182-3.628C59.826 86.932 78 45 128.5 45.5c49 .5 82.751 41.929 82.5 83.242C208 184 166 211 127.5 210c-54.5 0-72.235-42.928-72.235-42.928" />
                </svg>
                <span class="sr-only">Unclear Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">Unclear Notification</p>
        </div>
        <div class="delete-notification-btn action-item confirm-action-btn relative-pos" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path d="M12 2.75a2.25 2.25 0 0 0-2.122 1.5a.75.75 0 0 1-1.414-.5a3.751 3.751 0 0 1 7.073 0a.75.75 0 0 1-1.415.5A2.251 2.251 0 0 0 12 2.75M2.75 6a.75.75 0 0 1 .75-.75h17a.75.75 0 0 1 0 1.5h-17A.75.75 0 0 1 2.75 6m3.165 2.45a.75.75 0 1 0-1.497.1l.464 6.952c.085 1.282.154 2.318.316 3.132c.169.845.455 1.551 1.047 2.104c.591.554 1.315.793 2.17.904c.822.108 1.86.108 3.146.108h.879c1.285 0 2.324 0 3.146-.108c.854-.111 1.578-.35 2.17-.904c.591-.553.877-1.26 1.046-2.104c.162-.814.23-1.85.316-3.132l.464-6.952a.75.75 0 0 0-1.497-.1l-.46 6.9c-.09 1.347-.154 2.285-.294 2.99c-.137.685-.327 1.047-.6 1.303c-.274.256-.648.422-1.34.512c-.713.093-1.653.095-3.004.095h-.774c-1.35 0-2.29-.002-3.004-.095c-.692-.09-1.066-.256-1.34-.512c-.273-.256-.463-.618-.6-1.303c-.14-.705-.204-1.643-.294-2.99z" />
                    <path d="M9.425 10.254a.75.75 0 0 1 .821.671l.5 5a.75.75 0 0 1-1.492.15l-.5-5a.75.75 0 0 1 .671-.821m5.821.821a.75.75 0 0 0-1.492-.15l-.5 5a.75.75 0 0 0 1.492.15z" />
                </svg>
                <span class="sr-only">Delete Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">Delete Notification</p>
            <div class="confirm-action-container absolute-pos wrapper-menu">
                <p class="dark-text small-text">Confirm Delete</p>
                <div class="confirm-options">
                    <p class="confirm-delete-notification-btn icon-container dark-text gl-1 success" data-sku="${sku}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                            <path fill-rule="evenodd" d="M20.207 6.793a1 1 0 0 1 0 1.414l-9.5 9.5a1 1 0 0 1-1.414 0l-4.5-4.5a1 1 0 0 1 1.414-1.414L10 15.586l8.793-8.793a1 1 0 0 1 1.414 0" clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Check Icon</span>
                    </p>
                    <p class="deny-action-btn icon-container dark-text gl-1 error">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                            <path fill-rule="evenodd" d="M17.707 7.707a1 1 0 0 0-1.414-1.414L12 10.586L7.707 6.293a1 1 0 0 0-1.414 1.414L10.586 12l-4.293 4.293a1 1 0 1 0 1.414 1.414L12 13.414l4.293 4.293a1 1 0 1 0 1.414-1.414L13.414 12z" clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Xmark Icon</span>
                    </p>
                </div>
            </div>
        </div>
        `;
    }

    targetContainer.insertBefore(item, targetContainer.childNodes[0]);
    listenForBtnClicks(actionMenuContainer, item);
    let confirmActionBtn = actionMenuContainer.querySelector(".confirm-action-btn");

    if (confirmActionBtn) {
        listenForConfirmBtn(confirmActionBtn);
    }
    
    if (targetContainerNoItemWrapper) {
        targetContainerNoItemWrapper.remove()
    }
    updateoriginalContainer(originalContainer, originalContainerName);
}

let getContainerType = (item, targetContainerName) => {
    let dataContainer = item.getAttribute("data-container");

    item.setAttribute("data-container", targetContainerName);

    return dataContainer;
}

let visitUrlNotification = async (sku) => {        
    let url = `/notifications/visit_url_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]
            let url = data["url"]

            if (success) {
                if (url) {
                    displayOverlay();
                    window.setTimeout(() => {
                        window.location = url;
                    }, 1500);
                }
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let viewNotification = async (sku) => {        
    let url = `/notifications/view/${sku}`;

    window.location = url;
}

let clearNotification = async (sku, item) => {        
    let url = `/notifications/clear_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                moveNotification(sku, item, "new", "cleared")
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let unclearNotification = async (sku, item) => {        
    let url = `/notifications/unclear_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                moveNotification(sku, item, "cleared", "new")
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let clearAllNotifications = async (username) => {        
    let url = `/notifications/clear_all_notifications/${username}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                let skus = data["skus"]

                skus.forEach(sku => {
                    let item = document.querySelector(`.item-wrapper[data-sku="${sku}"]`);
                    moveNotification(sku, item, "new", "cleared")
                })
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let unclearAllNotifications = async (username) => {        
    let url = `/notifications/unclear_all_notifications/${username}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                let skus = data["skus"]

                skus.forEach(sku => {
                    let item = document.querySelector(`.item-wrapper[data-sku="${sku}"]`);
                    moveNotification(sku, item, "cleared", "new")
                })
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let deleteNotification = async (sku, item) => {        
    let url = `/notifications/delete_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            let containerType = getContainerType(item, "deleted");

            if (success) {
                moveNotification(sku, item, containerType, "deleted")
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }
    let viewNotificationSection = document.querySelector(".view-notification-section");
    if (viewNotificationSection) {
        hideElements();
        notificationDeleted();
    }
    displayMessages();
}

let deleteAllNotifications = async (username) => {        
    let url = `/notifications/delete_all_notifications/${username}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                let skus = data["skus"]

                skus.forEach(sku => {
                    let item = document.querySelector(`.item-wrapper[data-sku="${sku}"]`);
                    moveNotification(sku, item, "cleared", "deleted")
                })
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

let listenForConfirmBtn = (btn) => {
    let confirmContainer = btn.querySelector(".confirm-action-container");

    btn.addEventListener("click", (e) => {
        let target = e.target;
        let isConfirmItem = confirmContainer.contains(target);
        if (!isConfirmItem) {
            toggleElementShow(confirmContainer);
        }
    });

    let confirmParentWrapper = confirmContainer.parentNode.closest(".wrapper-menu");
    let denyBtn = btn.querySelector(".deny-action-btn");

    denyBtn.addEventListener("click", () => {
        toggleElementShow(confirmParentWrapper);
    });
};

let listenForActionBtn = (btn) => {
    btn.addEventListener("click", (e) => {
        let actionMenu = btn.querySelector(".action-menu-container");
        let target = e.target;
        let isActionItem = actionMenu.contains(target);

        if (!isActionItem) {
            toggleElementShow(actionMenu);
        }
    });

    let confirmActionBtns = btn.querySelectorAll(".confirm-action-btn");

    confirmActionBtns.forEach((aBtn) => {
        listenForConfirmBtn(aBtn);
    });
};

document.addEventListener('DOMContentLoaded', () => {
    const actionMenuBtns = document.querySelectorAll(".action-menu-btn");

    actionMenuBtns.forEach(btn => {
        listenForActionBtn(btn);
    });
});

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

        let notificationHeadingActionMenu = document.querySelector(".notification-heading-action-menu");

        listenForBtnClicks(notificationHeadingActionMenu, false);

        let itemWrappers = profileContainer.querySelectorAll(".item-wrapper");

        itemWrappers.forEach((item) => {
            let actionMenuBtn = item.querySelector(".notification-action-menu-btn");
            let actionMenu = item.querySelector(".action-menu-container");

            if (actionMenuBtn) {
                item.addEventListener("mouseenter", () => {
                    actionMenuBtn.classList.add("show");
                });

                item.addEventListener("mouseleave", () => {
                    toggleElementShow(item);
                });

                listenForBtnClicks(actionMenu, item);
            }
        });
    }
});

/**
 * Messages Section
 */

document.addEventListener("DOMContentLoaded", () => {
    displayMessages();
    getFormErrors();

    let messagesCloseBtn = document.querySelector(".messages-close-btn");

    messagesCloseBtn.addEventListener("click", () => {
        hideMessages();
    });
});

let getMessages = async () => {
    return fetch('/notifications/get_messages/')
        .then(response => response.json())
        .then(data => data.messages)
        .catch(error => {
            console.error('Error:', error);
            return []; // Return empty array if there's an error
        });
}

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
        } else if (intervalCounter >= 44) {
            hideMessages();
            clearInterval(hideMessageInterval);
        } else {
            intervalCounter += 1;
        }
    }, 100);
}

let displayMessages = async () => {
    const messagesContainer = document.querySelector(".messages-display-container");

    let messages = await getMessages();

    if (messagesContainer && messages.length > 0) {
        messagesContainer.innerHTML = messages.map(message => `
            <div class="message-container">
                <div class="icon-container color-${message.tags}">
                    ${message.icon}
                    <span class="sr-only">${message.tags.charAt(0).toUpperCase() + message.tags.slice(1)} Icon</span>
                </div>
                <p class="message-text dark-text small-text">${message.message}</p>
            </div>
        `).join('');

        showMessages();
    }
}

let displayOverlay = () => {
    let overlay = document.createElement("div");
    overlay.classList.add("blur-overlay");

    let body = document.querySelector("body");

    body.appendChild(overlay);
}

let displayErrorMessage = (message, element) => {
    if (element) {
        element.classList.add("error-message");
    }

    if (message) {
        const messagesContainer = document.querySelector(".messages-display-container");
    
        messagesContainer.innerHTML = `
        <div class="message-container">
            <div class="icon-container color-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M17.707 7.707a1 1 0 0 0-1.414-1.414L12 10.586L7.707 6.293a1 1 0 0 0-1.414 1.414L10.586 12l-4.293 4.293a1 1 0 1 0 1.414 1.414L12 13.414l4.293 4.293a1 1 0 1 0 1.414-1.414L13.414 12z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only">Error Icon</span>
            </div>
            <p class="message-text dark-text small-text">${message}</p>
        </div>
        `;
    
        showMessages();
    }
}

let getFormErrors = () => {
    let fields = document.querySelectorAll(".data-field-id");

    fields.forEach((field) => {
        let id = field.getAttribute("data-field-id");

        let element = document.getElementById(id);

        element.classList.add("error-message");
    });

    const messagesContainer = document.querySelector(".messages-display-container");

    let errors = document.querySelectorAll(".data-error-message");

    errors.forEach(error => {
        let message = error.getAttribute("data-error-message");
        let messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container");
        messageContainer.innerHTML = `
        <div class="icon-container color-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M17.707 7.707a1 1 0 0 0-1.414-1.414L12 10.586L7.707 6.293a1 1 0 0 0-1.414 1.414L10.586 12l-4.293 4.293a1 1 0 1 0 1.414 1.414L12 13.414l4.293 4.293a1 1 0 1 0 1.414-1.414L13.414 12z" clip-rule="evenodd" />
            </svg>
            <span class="sr-only">Error Icon</span>
        </div>
        <p class="message-text dark-text small-text">${message}</p>
        `;
        messagesContainer.appendChild(messageContainer);
    });

    if (errors.length > 0) {
        showMessages();
    }
}