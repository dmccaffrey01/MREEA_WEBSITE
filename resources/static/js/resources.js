document.addEventListener("DOMContentLoaded", () => {
    let searchInput = document.querySelector(".search-input");

    let itemContainers = document.querySelectorAll(".resource-container");
    let itemsContainer = document.querySelector(".resources-container");
        
    let searchResults = true;

    searchInput.addEventListener("keydown", () => {
        window.setTimeout(() => {
            let searchVal = searchInput.value.toLowerCase();
            searchResults = false;

            itemContainers.forEach(item => {
                let itemName = item.getAttribute("data-name").toLowerCase();

                if (itemName.includes(searchVal)) {
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

            let noSearchResults = document.querySelector(".no-results");
            if (noSearchResults) {
                noSearchResults.remove();
            }

            if (!searchResults) {
                let noSearchResults = document.createElement("p");
                noSearchResults.innerHTML = `No results found for '${searchVal}'`;
                noSearchResults.classList.add("dark-text");
                noSearchResults.classList.add("no-results");

                itemsContainer.appendChild(noSearchResults);
            }
        });
    });
});
