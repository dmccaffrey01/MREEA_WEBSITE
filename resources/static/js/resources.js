document.addEventListener("DOMContentLoaded", () => {
    let itemContainers = document.querySelectorAll(".item-container");

    itemContainers.forEach(item => {
        let btns = item.querySelectorAll(".info-container");

        item.addEventListener("click", () => {
            let url = item.getAttribute("data-url");
            let newTab = item.getAttribute("data-new-tab");
            if (url) {
                if (newTab) {
                    window.open(url, "_blank"); 
                } else {
                    window.location.replace(url);
                }
                
            }
        });

    });
});

document.addEventListener("DOMContentLoaded", () => {
    let searchInput = document.querySelector(".search-input");

    let itemContainers = document.querySelectorAll(".item-container");
        
    let itemsContainer = document.querySelector(".items-container");

    let searchResults = true;

    let noSearchResults = document.querySelector(".no-search-results");

    searchInput.addEventListener("keydown", () => {
        window.setTimeout(() => {
            let searchVal = searchInput.value.toLowerCase();
            searchResults = false;

            itemContainers.forEach(item => {
                let itemName = item.getAttribute("data-name").toLowerCase();
                console.log(searchVal, itemName);
                console.log(itemName.includes(searchVal));

                if (itemName.includes(searchVal)) {
                    if (item.classList.contains("hide")) {
                        item.classList.remove("hide");
                        console.log("show");
                    }
                    searchResults = true;
                    
                } else {
                    if (!item.classList.contains("hide")) {
                        item.classList.add("hide");
                        console.log("hide");
                    }
                }
            });

            if (!searchResults) {
                noSearchResults.innerHTML = `No results found for '${searchVal}'`;
                noSearchResults.classList.remove("hide");
            } else {
                noSearchResults.classList.add("hide");
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let itemsContainer = document.querySelector(".items-container");
    let itemContainers = document.querySelectorAll(".item-container");
    let sortBtns = document.querySelectorAll(".sort-btn");

    sortBtns.forEach((btn, i) => {
        btn.addEventListener("click", () => {
            let sort = btn.getAttribute("data-sort");
            let direction = btn.getAttribute("data-direction");

            if (direction === "default" || direction === "asc") {
                direction = "desc";
            } else {
                direction = "asc";
            }

            btn.setAttribute("data-direction", direction);

            let btnImg = btn.querySelector(".img-100a");

            let imgSrc = btnImg.src;

            let splitSrc = imgSrc.split("sort");

            let newSrc = splitSrc[0] + `sort-${direction}-icon.png`;

            btnImg.src = newSrc;

            sortBtns.forEach((otherBtn, k) => {
                if (k != i) {
                    otherBtn.setAttribute("data-direction", "default");

                    let otherBtnImg = otherBtn.querySelector(".img-100a");

                    let otherBtnImgSrc = otherBtnImg.src;

                    let split = otherBtnImgSrc.split("sort");

                    let newSrc = split[0] + "sort-icon.png";

                    otherBtnImg.src = newSrc;
                }
            });

            if (sort === "name" || sort === "type") {
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
            } else if (sort === "date") {
                itemContainers.forEach(item => {
                    let sortData = item.getAttribute(`data-${sort}`);
                    let currentDate = new Date().getTime();
                    let itemDate = new Date(sortData).getTime();
                    let difference = Math.abs(currentDate - itemDate);
                    item.style.order = direction === "asc" ? -difference : difference; // Setting order based on time from present
                });
            }
        });
    });
});