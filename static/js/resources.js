const resourcesCategoryContainers = document.querySelectorAll(".resources-category-container");
const resourcesCategoryDropdownHeading = document.querySelectorAll(".resources-category-dropdown-heading");
const resourcesCategoryItemsContainer = document.querySelectorAll(".resources-category-items-container");

const closeResourceLinkEmbedBtn = document.querySelector(".close-resource-link-embed-btn");
const resourceLinkEmbedSection = document.querySelector(".resource-link-embed-section");
const youtubeIframe = document.querySelector(".youtube-iframe");
const pdfIframe = document.querySelector(".pdf-iframe");
const videoContainer = document.querySelector(".iframe-video-container");

resourcesCategoryDropdownHeading.forEach((heading, index) => {
    heading.addEventListener("click", () => {
        let items = resourcesCategoryItemsContainer[index];
        items.classList.toggle("active");
    });

    let resourcesCategoryContainer = resourcesCategoryContainers[index];
    let subCategoryContainers = resourcesCategoryContainer.querySelectorAll(".resources-subcategory-container");
    let resourcesSubCategoryDropdownHeading = resourcesCategoryContainer.querySelectorAll(".resources-subcategory-dropdown-heading");
    let resourcesSubCategoryItemsContainer = resourcesCategoryContainer.querySelectorAll(".resources-subcategory-items-container");

    resourcesSubCategoryDropdownHeading.forEach((subheading, k) => {
        subheading.addEventListener("click", () => {
            let subItems = resourcesSubCategoryItemsContainer[k];
            subItems.classList.toggle("active");
        });

        let subCategeryContainer = subCategoryContainers[k];
        let resourceLinkItems = subCategeryContainer.querySelectorAll(".resource-link-dropdown-item");
        let resourcesResourceOpenBtn = subCategeryContainer.querySelectorAll(".resources-resource-open-btn");
        let resourcesResourceOpenContainer = subCategeryContainer.querySelectorAll(".resources-resource-open-container");

        resourcesResourceOpenBtn.forEach((btn, j) => {
            btn.addEventListener("click", () => {
                let openContainer = resourcesResourceOpenContainer[j];
                openContainer.classList.toggle("active");
            })

            let resourceLinkItem = resourceLinkItems[j];
            let embedLinkData = resourceLinkItem.querySelector(".resource-embed-link-data").innerText;
            let linkTypeData = resourceLinkItem.querySelector(".resource-link-type-data").innerText;
            let openHereTabBtn = resourceLinkItem.querySelector(".resource-open-here-btn");
            let linkData = resourceLinkItem.querySelector(".resources-resource-link-heading").innerText;
            

            openHereTabBtn.addEventListener("click", () => {
                pdfIframe.style.display = "none";
                youtubeIframe.style.display = "none";
                videoContainer.style.display = "none";
                if (linkTypeData == "PDF" && embedLinkData) {
                    pdfIframe.src = embedLinkData;
                    pdfIframe.style.display = "flex";
                    resourceLinkEmbedSection.style.display = "flex";
                } else if (linkTypeData == "Youtube" && embedLinkData) {
                    youtubeIframe.src = embedLinkData;
                    videoContainer.style.display = "flex";
                    youtubeIframe.style.display = "flex";
                    resourceLinkEmbedSection.style.display = "flex";
                } else {
                    window.open(linkData, '_blank');
                }
            });
        });
    });
});


closeResourceLinkEmbedBtn.addEventListener("click", () => {
    resourceLinkEmbedSection.style.display = "none";
})