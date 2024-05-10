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
                    <g fill="none" fill-rule="evenodd">
                        <path d="M21.546 5.111a1.5 1.5 0 0 1 0 2.121L10.303 18.475a1.6 1.6 0 0 1-2.263 0L2.454 12.89a1.5 1.5 0 1 1 2.121-2.121l4.596 4.596L19.424 5.111a1.5 1.5 0 0 1 2.122 0" />
                    </g>
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
    console.log(newNotificationsItems);

    let notificationNumber = document.querySelector('.notification-number');
    notificationNumber.innerHTML = amountOfNewItems;
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
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M9 3a1 1 0 0 0 0 2h9v13a1 1 0 0 1-1 1H9a1 1 0 0 0 0 2h8a3 3 0 0 0 3-3V4a1 1 0 0 0-1-1zm3.707 5.293A1 1 0 0 0 11 9v2H5a1 1 0 0 0 0 2h6v2a1 1 0 0 0 1.707.707l3-3a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only">Visit Linl Icon</span>
            </p>
            <p class="item-text dark-text small-text">Visit ${urlName}</p>
        </div>
        <div class="view-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 32 32">
                    <circle cx="16" cy="16" r="4" />
                    <path d="M30.94 15.66A16.69 16.69 0 0 0 16 5A16.69 16.69 0 0 0 1.06 15.66a1 1 0 0 0 0 .68A16.69 16.69 0 0 0 16 27a16.69 16.69 0 0 0 14.94-10.66a1 1 0 0 0 0-.68M16 22.5a6.5 6.5 0 1 1 6.5-6.5a6.51 6.51 0 0 1-6.5 6.5" />
                </svg>
                <span class="sr-only">View Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">View Notification</p>
        </div>
        <div class="clear-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path d="M12 22q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22m0-2q1.35 0 2.6-.437t2.3-1.263L5.7 7.1q-.825 1.05-1.263 2.3T4 12q0 3.35 2.325 5.675T12 20m6.3-3.1q.825-1.05 1.263-2.3T20 12q0-3.35-2.325-5.675T12 4q-1.35 0-2.6.437T7.1 5.7z" />
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
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M9 3a1 1 0 0 0 0 2h9v13a1 1 0 0 1-1 1H9a1 1 0 0 0 0 2h8a3 3 0 0 0 3-3V4a1 1 0 0 0-1-1zm3.707 5.293A1 1 0 0 0 11 9v2H5a1 1 0 0 0 0 2h6v2a1 1 0 0 0 1.707.707l3-3a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only">Visit Linl Icon</span>
            </p>
            <p class="item-text dark-text small-text">Visit ${urlName}</p>
        </div>
        <div class="view-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 32 32">
                    <circle cx="16" cy="16" r="4" />
                    <path d="M30.94 15.66A16.69 16.69 0 0 0 16 5A16.69 16.69 0 0 0 1.06 15.66a1 1 0 0 0 0 .68A16.69 16.69 0 0 0 16 27a16.69 16.69 0 0 0 14.94-10.66a1 1 0 0 0 0-.68M16 22.5a6.5 6.5 0 1 1 6.5-6.5a6.51 6.51 0 0 1-6.5 6.5" />
                </svg>
                <span class="sr-only">View Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">View Notification</p>
        </div>
        <div class="unclear-notification-btn action-item" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 16 16">
                    <path d="M1.22 6.28a.75.75 0 0 1 0-1.06l3.5-3.5a.749.749 0 1 1 1.06 1.06L3.561 5h7.188l.001.007L10.749 5q.088 0 .171.019A4.501 4.501 0 0 1 10.5 14H8.796a.75.75 0 0 1 0-1.5H10.5a3 3 0 1 0 0-6H3.561L5.78 8.72a.749.749 0 1 1-1.06 1.06z" />
                </svg>
                <span class="sr-only">Unclear Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">Unclear Notification</p>
        </div>
        <div class="delete-notification-btn action-item confirm-action-btn relative-pos" data-sku="${sku}">
            <p class="icon-container dark-text">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M8.106 2.553A1 1 0 0 1 9 2h6a1 1 0 0 1 .894.553L17.618 6H20a1 1 0 1 1 0 2h-1v11a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V8H4a1 1 0 0 1 0-2h2.382zM14.382 4l1 2H8.618l1-2zM11 11a1 1 0 1 0-2 0v6a1 1 0 1 0 2 0zm4 0a1 1 0 1 0-2 0v6a1 1 0 1 0 2 0z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only">Delete Notification Icon</span>
            </p>
            <p class="item-text dark-text small-text">Delete Notification</p>
            <div class="confirm-action-container absolute-pos wrapper-menu">
                <p class="dark-text small-text">Confirm Delete</p>
                <div class="confirm-options">
                    <p class="confirm-delete-notification-btn icon-container dark-text gl-1 success" data-sku="${sku}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 24 24">
                            <g fill-rule="evenodd">
                                <path fill="black" d="M21.546 5.111a1.5 1.5 0 0 1 0 2.121L10.303 18.475a1.6 1.6 0 0 1-2.263 0L2.454 12.89a1.5 1.5 0 1 1 2.121-2.121l4.596 4.596L19.424 5.111a1.5 1.5 0 0 1 2.122 0" />
                            </g>
                        </svg>
                        <span class="sr-only">Check Icon</span>
                    </p>
                    <p class="deny-action-btn icon-container dark-text gl-1 error">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 15 15">
                            <path d="M3.64 2.27L7.5 6.13l3.84-3.84A.92.92 0 0 1 12 2a1 1 0 0 1 1 1a.9.9 0 0 1-.27.66L8.84 7.5l3.89 3.89A.9.9 0 0 1 13 12a1 1 0 0 1-1 1a.92.92 0 0 1-.69-.27L7.5 8.87l-3.85 3.85A.92.92 0 0 1 3 13a1 1 0 0 1-1-1a.9.9 0 0 1 .27-.66L6.16 7.5L2.27 3.61A.9.9 0 0 1 2 3a1 1 0 0 1 1-1c.24.003.47.1.64.27" />
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
                    actionMenuBtn.classList.remove("show");
                    actionMenu.classList.remove("show");
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
                <div class="icon-container">
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