document.addEventListener("DOMContentLoaded", () => {
    let searchInput = document.querySelector(".search-input");

    let itemContainers = document.querySelectorAll(".user-container");
        
    let itemsContainer = document.querySelector(".users-container");

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
    let userWrappers = document.querySelectorAll(".user-wrapper");

    userWrappers.forEach((wrapper) => {
        let actionMenuBtn = wrapper.querySelector(".user-action-menu-btn");

        if (actionMenuBtn) {
            wrapper.addEventListener("mouseenter", () => {
                actionMenuBtn.classList.add("show");
            });

            wrapper.addEventListener("mouseleave", () => {
                toggleElementShow(wrapper);
            });
        }
    });
});