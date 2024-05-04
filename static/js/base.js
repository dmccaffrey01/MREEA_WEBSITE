let getMessages = async () => {
    return fetch('/notifications/get_messages/')
        .then(response => response.json())
        .then(data => data.messages)
        .catch(error => {
            console.error('Error:', error);
            return []; // Return empty array if there's an error
        });
}

let displayMessages = async () => {
    const messagesContainer = document.querySelector(".messages-container");

    let messages = await getMessages();

    if (messagesContainer && messages.length > 0) {
        messagesContainer.innerHTML = messages.map(message => `
            <div class="messages-display-container container-col align-start">
                <h3 class="dark-text subheading">${message.tags.charAt(0).toUpperCase() + message.tags.slice(1)}</h3>
                <div class="message-container container-row align-start">
                    <p class="message-icon color-${message.tags} dark-text small-text">
                        <i class="fa-solid fa-circle-${message.tags === 'success' ? 'check' : message.tags === 'error' ? 'xmark' : message.tags === 'warning' ? 'exclamation' : 'info'}"></i>
                        <span class="sr-only">${message.tags.charAt(0).toUpperCase() + message.tags.slice(1)} Icon</span>
                    </p>
                    <p class="message-text dark-text small-text">${message.message}</p>
                </div>
            </div>
        `).join('');

        messagesContainer.classList.add("show");
        window.setTimeout(() => {
            messagesContainer.classList.add("fade");
        }, 100);

        window.setTimeout(() => {
            messagesContainer.classList.remove("fade");
            window.setTimeout(() => {
                messagesContainer.classList.remove("show");
            }, 600);
        }, 4400);
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
                    <i class="fa-solid fa-circle-check"></i>
                    <span class="sr-only">Check Circle Icon</span>
                </p>    
                <p class="item-heading dark-text small-text">No ${originalContainerName.charAt(0).toUpperCase() + originalContainerName.slice(1)} Notifications</p>
                <div class="item-gap"></div>
            </div>
        </div>
        `;
    }

    let notificationNumber = document.querySelector('.notification-number');
    notificationNumber.innerHTML = amountOfItems;
}

let moveNotification = (item, originalContainerName, targetContainerName) => {
    console.log(originalContainerName, targetContainerName);
    let originalContainer = document.querySelector(`.${originalContainerName}-notifications-container`);
    let targetContainer = document.querySelector(`.${targetContainerName}-notifications-container`);

    console.log(originalContainer, targetContainer)
   
    let targetContainerNoItemWrapper = targetContainer.querySelector(".no-item-wrapper");

    if (targetContainerName) {
        targetContainer.insertBefore(item, targetContainerNoItemWrapper);
        updateoriginalContainer(originalContainer, originalContainerName);
    } else {
        item.remove()
    }

    if (targetContainerNoItemWrapper) {
        targetContainerNoItemWrapper.remove()
    }
}

let clearNotification = async (sku, item) => {        
    let url = `/notifications/clear_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                moveNotification(item, "new", "cleared")
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

            if (success) {
                moveNotification(item, "cleared", "new")
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

document.addEventListener('DOMContentLoaded', () => {
    const actionMenuBtns = document.querySelectorAll(".action-menu-btn");
    let actionClick = false;

    actionMenuBtns.forEach(btn => {
        let actionMenu = btn.querySelector(".action-menu-container");

        btn.addEventListener("click", () => {
            window.setTimeout(() => {
                if (!actionClick) {
                    actionMenu.classList.toggle("show");
                }
            }, 100);
        });

        let confirmActionBtns = document.querySelectorAll(".confirm-action-btn");

        confirmActionBtns.forEach(aBtn => {
            let confirmContainer = aBtn.querySelector(".confirm-action-container");

            aBtn.addEventListener("click", () => {
                actionClick = true;
                confirmContainer.classList.toggle("show");
                window.setTimeout(() => {
                    actionClick = false;
                }, 150);
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const profileContainer = document.querySelector(".profile-container");

    if (profileContainer) {
        let profileBtn = profileContainer.querySelector(".profile-btn-container");
        let profileBtnIcon = profileContainer.querySelector(".profile-btn-icon");
        let profileMenu = profileContainer.querySelector(".profile-menu-container");

        let notificationBtn = profileContainer.querySelector(".notification-btn-container");
        let notificationMenu = profileContainer.querySelector(".notification-menu-container");

        profileBtn.addEventListener("click", () => {
            profileMenu.classList.toggle("show");
            notificationMenu.classList.remove("show");

            profileBtnIcon.classList.toggle("rotate");
        });

        notificationBtn.addEventListener("click", () => {
            notificationMenu.classList.toggle("show");
            profileMenu.classList.remove("show");
        });

        let notificationTypeBtns = document.querySelectorAll(".type-heading-container");
        let itemContainers = document.querySelectorAll(".items-display-container");

        notificationTypeBtns.forEach((btn, i) => {
            btn.addEventListener("click", () => {
                if (!btn.classList.contains("selected")) {
                    btn.classList.add("selected");
                    let icon = btn.querySelector("svg");
                    icon.classList.add("red-text");

                    notificationTypeBtns.forEach((otherBtn, k) => {
                        if (k != i) {
                            otherBtn.classList.remove("selected");
                            let icon = otherBtn.querySelector("svg");
                            icon.classList.remove("red-text");
                        }
                    });

                    itemContainers.forEach((container, k) => {
                        if (k == i) {
                            container.classList.add("selected");
                        } else {
                            container.classList.remove("selected");
                        }
                    });
                }
            });
        });

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

                let clearBtn = actionMenu.querySelector(".clear-notification-btn");
                if (clearBtn) {
                    clearBtn.addEventListener("click", () => {
                        let sku = clearBtn.getAttribute("data-sku");
                        console.log(item);
                        clearNotification(sku, item);
                    });
                }

                let deleteBtn = actionMenu.querySelector(".delete-notification-btn");
                if (deleteBtn) {
                    deleteBtn.addEventListener("click", () => {
                        let sku = deleteBtn.getAttribute("data-sku");
                        deleteNotification(sku, item);
                    });
                }
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    displayMessages();
});