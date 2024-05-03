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
            }, 800);
        }, 4800);
    }
}

let updateNewNotifications = () => {
    let newNotificationsContainer = document.querySelector(".new-notifications-container");

    let items = newNotificationsContainer.querySelectorAll(".item-wrapper");

    let amountOfItems = items.length

    if (!amountOfItems > 0) {
        newNotificationsContainer.innerHTML = `
        <div class="item-wrapper container-row space-between">
            <div class="item-container container-row space-between">
                <p class="item-icon container-col">
                    <i class="fa-solid fa-circle-check"></i>
                    <span class="sr-only">Check Circle Icon</span>
                </p>    
                <p class="item-heading dark-text small-text">No New Notifications</p>
            </div>
        </div>
        `;
    }

    let notificationNumber = document.querySelector('.notification-number');
    notificationNumber.innerHTML = amountOfItems;
}

let clearNotification = async (sku, item) => {        
    let url = `/notifications/clear_notification/${sku}`;

    try {
        let response = await fetch(url);
        if (response.ok) {
            let data = await response.json(); // Parse response as JSON
            
            let success = data["success"]

            if (success) {
                // Remove the item from the DOM
                item.remove();

                // Check if there are no more items
                updateNewNotifications();
            }
        } 
    } catch (error) {
        console.error('Error:', error);
    }

    displayMessages();
}

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
            let clearBtn = item.querySelector(".clear-notification-btn");
            let confirmClearContainer = item.querySelector(".confirm-clear-container");

            if (clearBtn) {
                item.addEventListener("mouseenter", () => {
                    clearBtn.classList.add("show");
                });

                item.addEventListener("mouseleave", () => {
                    clearBtn.classList.remove("show");
                    confirmClearContainer.classList.remove("show");
                });

                clearBtn.addEventListener("click", () => {
                    clearBtn.classList.remove("show");
                    confirmClearContainer.classList.add("show");

                    let confirmBtn = confirmClearContainer.querySelector(".confirm-clear-btn");
                    let cancelBtn = confirmClearContainer.querySelector(".cancel-clear-btn");
                    confirmBtn.addEventListener("click", () => {
                        let sku = confirmBtn.getAttribute("data-sku");
                        console.log(sku);
                        clearNotification(sku, item);
                    });

                    cancelBtn.addEventListener("click", () => {
                        confirmClearContainer.classList.remove("show");
                        clearBtn.classList.add("show");
                    });
                });
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    displayMessages();
});