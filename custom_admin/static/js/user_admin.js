document.addEventListener("DOMContentLoaded", () => {
    let searchInput = document.querySelector(".search-input");

    let itemContainers = document.querySelectorAll(".item-container");
        
    let itemsContainer = document.querySelector(".items-container");

    let searchResults = true;

    searchInput.addEventListener("keydown", () => {
        let isNoSearchResults = document.querySelector(".no-search-results");
        if (isNoSearchResults) {
            itemsContainer.removeChild(isNoSearchResults);
        }

        window.setTimeout(() => {
            let searchVal = searchInput.value.toLowerCase();
            searchResults = false;

            itemContainers.forEach(item => {
                let itemFirstName = item.getAttribute("data-first-name").toLowerCase();
                let itemLastName = item.getAttribute("data-last-name").toLowerCase();
                let itemEmail = item.getAttribute("data-email").toLowerCase();
                let itemStatus = item.getAttribute("data-status").toLowerCase();
                let itemEndDate = item.getAttribute("data-end-date").toLowerCase();

                if (itemFirstName.includes(searchVal) || itemLastName.includes(searchVal) || itemEmail.includes(searchVal) || itemStatus.includes(searchVal) || itemEndDate.includes(searchVal)) {
                    if (item.classList.contains("hide")) {
                        item.classList.remove("hide");
                    }
                    searchResults = true;
                    
                } else {
                    if (!item.classList.contains("hide")) {
                        item.classList.add("hide");
                    }
                }
            });

            if (!searchResults) {
                let noSearchResults = document.createElement("div");
                noSearchResults.classList.add("no-search-results");
                noSearchResults.innerHTML = `<p class="dark-text small-text">No results found for '${searchVal}'</p>`;
                itemsContainer.appendChild(noSearchResults);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let itemsContainer = document.querySelector(".items-container");
    let itemContainers = document.querySelectorAll(".item-container");
    let sortBtns = document.querySelectorAll(".sort-btn");

    let updateStatusSortIcon = (color) => {
        let statusBtn = document.querySelector(".status-sort-btn");

        let icon = statusBtn.querySelector(".fa-solid");

        if (icon.classList.contains("fa-sort")) {
            icon.classList.remove("fa-sort")
        }
        if (icon.classList.contains("fa-circle-exclamation")) {
            icon.classList.remove("fa-circle-exclamation")
        }
        if (icon.classList.contains("fa-circle-check")) {
            icon.classList.remove("fa-circle-check")
        }
        if (icon.classList.contains("fa-circle-xmark")) {
            icon.classList.remove("fa-circle-xmark")
        }
        if (icon.classList.contains("fa-circle-question")) {
            icon.classList.remove("fa-circle-question")
        }

        if (icon.classList.contains("color-success")) {
            icon.classList.remove("color-success")
        }
        if (icon.classList.contains("color-warning")) {
            icon.classList.remove("color-warning")
        }
        if (icon.classList.contains("color-danger")) {
            icon.classList.remove("color-danger")
        }
        if (icon.classList.contains("color-info")) {
            icon.classList.remove("color-info")
        }

        if (color == "warning") {
            icon.classList.add("fa-circle-exclamation")
        }
        if (color == "success") {
            icon.classList.add("fa-circle-check")
        }
        if (color == "danger") {
            icon.classList.add("fa-circle-xmark")
        }
        if (color == "info") {
            icon.classList.add("fa-circle-question")
        }

        icon.classList.add(`color-${color}`);
    }

    sortBtns.forEach((btn, i) => {
        btn.addEventListener("click", () => {
            let sort = btn.getAttribute("data-sort");
            let direction = btn.getAttribute("data-direction");

            if (sort == "status") {
                let statusColors = btn.getAttribute("data-status-colors");
                let statusColorsArr = statusColors.split(",");

                let currentIndex = statusColorsArr.indexOf(direction);
                if (direction === "default") {
                    direction = statusColorsArr[0];
                } else {
                    let nextIndex = (currentIndex + 1) % statusColorsArr.length;
                    direction = statusColorsArr[nextIndex];
                }

                updateStatusSortIcon(direction);

            } else {
                if (direction === "default" || direction === "asc") {
                    direction = "desc";
                    let icon = btn.querySelector(".fa-solid");
                    if (icon.classList.contains("fa-sort")) {
                        icon.classList.remove("fa-sort")
                    }
                    if (icon.classList.contains("fa-sort-up")) {
                        icon.classList.remove("fa-sort-up")
                    }
                    icon.classList.add("fa-sort-down")
                    icon.classList.add("red-text")
                } else {
                    direction = "asc";
                    let icon = btn.querySelector(".fa-solid");
                    if (icon.classList.contains("fa-sort")) {
                        icon.classList.remove("fa-sort")
                    }
                    if (icon.classList.contains("fa-sort-down")) {
                        icon.classList.remove("fa-sort-down")
                    }
                    icon.classList.add("fa-sort-up")
                    icon.classList.add("red-text")
                }
            }

            btn.setAttribute("data-direction", direction);

            sortBtns.forEach((otherBtn, k) => {
                if (k != i) {
                    otherBtn.setAttribute("data-direction", "default");

                    let icon = otherBtn.querySelector(".fa-solid");

                    if (icon.classList.contains("fa-sort-down")) {
                        icon.classList.remove("fa-sort-down")
                    }
                    if (icon.classList.contains("red-text")) {
                        icon.classList.remove("red-text")
                    }
                    if (icon.classList.contains("fa-sort-up")) {
                        icon.classList.remove("fa-sort-up")
                    }
                    icon.classList.add("fa-sort")
                }
            });


            if (sort === "first-name" || sort === "last-name" || sort === "email") {
                let sortedItems = Array.from(itemContainers).sort((a, b) => {
                    let aData = a.getAttribute(`data-${sort}`).toLowerCase();
                    let bData = b.getAttribute(`data-${sort}`).toLowerCase();
                    if (direction === "asc") {
                        return aData.localeCompare(bData);
                    } else {
                        return bData.localeCompare(aData);
                    }
                });

                // Rearrange items based on sorted order
                itemsContainer.innerHTML = "";
                sortedItems.forEach(item => itemsContainer.appendChild(item));
            } else if (sort === "end-date" || sort === "purchase-date") {
                // Sorting by date
                let sortedItems = Array.from(itemContainers).sort((a, b) => {
                    let aDate = new Date(a.getAttribute(`data-${sort}`));
                    let bDate = new Date(b.getAttribute(`data-${sort}`));
                    if (direction === "asc") {
                        return aDate - bDate;
                    } else {
                        return bDate - aDate;
                    }
                });
            
                // Replace itemsContainer content with sorted items
                itemsContainer.innerHTML = "";
                sortedItems.forEach(item => itemsContainer.appendChild(item));
            } else if (sort === "status") {
                // Sorting by color
                let sortedItems = Array.from(itemContainers).sort((a, b) => {
                    let aColor = a.getAttribute(`data-color`);
                    let bColor = b.getAttribute(`data-color`);
                    let firstColor = direction; // Set the first color for sorting
            
                    // If both items have the first color, maintain the original order
                    if (aColor === firstColor && bColor === firstColor) return 0;
                    
                    // If only the first item has the first color, it should come before the second item
                    if (aColor === firstColor) return -1;
            
                    // If only the second item has the first color, it should come after the first item
                    if (bColor === firstColor) return 1;
            
                    // If neither item has the first color, compare their colors alphabetically
                    return aColor.localeCompare(bColor);
                });
                
                // Replace itemsContainer content with sorted items
                itemsContainer.innerHTML = "";
                sortedItems.forEach(item => itemsContainer.appendChild(item));
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let itemContainers = document.querySelectorAll(".item-container");

    itemContainers.forEach((item, i) => {
        item.addEventListener("click", () => {
            let actionContainer = item.querySelector(".quick-actions-container");

            item.classList.add("selected")
            actionContainer.classList.add("show");

            itemContainers.forEach((otherItem, k) => {
                if (otherItem.classList.contains("selected") && k != i) {
                    let otherActionContainer = otherItem.querySelector(".quick-actions-container");

                    otherItem.classList.remove("selected")
                    otherActionContainer.classList.remove("show");
                }
            });
        });

        let membershipBtns = item.querySelectorAll(".membership-btn");

        if (membershipBtns.length > 0) {

            membershipBtns.forEach((btn) => {
                btn.addEventListener("click", async () => {
                    let approve = btn.getAttribute("data-approve");

                    let username = item.getAttribute("data-username");

                    let url = `change_membership_status/${username}/${approve}/`;

                    try {
                        let response = await fetch(url);
                        if (response.ok) {
                            let data = await response.json(); // Parse response as JSON
                            
                            let name = data["membership_status"];
                            let color = data["membership_status_color"];
                            let endDate = data["membership_end_date"];

                            let statusText = document.querySelector(".status-text");

                            let icon = statusText.querySelector(".fa-solid");

                            if (icon.classList.contains("fa-sort")) {
                                icon.classList.remove("fa-sort")
                            }
                            if (icon.classList.contains("fa-circle-exclamation")) {
                                icon.classList.remove("fa-circle-exclamation")
                            }
                            if (icon.classList.contains("fa-circle-check")) {
                                icon.classList.remove("fa-circle-check")
                            }
                            if (icon.classList.contains("fa-circle-xmark")) {
                                icon.classList.remove("fa-circle-xmark")
                            }
                            if (icon.classList.contains("fa-circle-question")) {
                                icon.classList.remove("fa-circle-question")
                            }

                            if (color == "warning") {
                                icon.classList.add("fa-circle-exclamation")
                            }
                            if (color == "success") {
                                icon.classList.add("fa-circle-check")
                            }
                            if (color == "danger") {
                                icon.classList.add("fa-circle-xmark")
                            }
                            if (color == "info") {
                                icon.classList.add("fa-circle-question")
                            }

                            if (statusText.classList.contains("color-success")) {
                                statusText.classList.remove("color-success")
                            }
                            if (statusText.classList.contains("color-warning")) {
                                statusText.classList.remove("color-warning")
                            }
                            if (statusText.classList.contains("color-danger")) {
                                statusText.classList.remove("color-danger")
                            }
                            if (statusText.classList.contains("color-info")) {
                                statusText.classList.remove("color-info")
                            }

                            statusText.classList.add(`color-${color}`);

                            let statusName = statusText.querySelector(".status-text-name");

                            statusName.innerHTML = name;

                            let endDateText = document.querySelector(".end-date-text");

                            if (endDateText.classList.contains("null") && endDate) {
                                endDateText.classList.remove("null");
                            }

                            if (endDate) {
                                endDateText.innerHTML = endDate;
                            }
                        } 
                    } catch (error) {
                        
                    }
                });
            });
        }
    });
});