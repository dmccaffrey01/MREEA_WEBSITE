const resourceLinkItems = document.querySelectorAll(".resource-link-dropdown-item");
const resourcesResourceOpenBtn = document.querySelectorAll(".resources-resource-open-btn");
const resourcesResourceOpenContainer = document.querySelectorAll(".resources-resource-open-container");

const closeResourceLinkEmbedBtn = document.querySelector(".close-resource-link-embed-btn");
const resourceLinkEmbedSection = document.querySelector(".resource-link-embed-section");
const youtubeIframe = document.querySelector(".youtube-iframe");
const pdfIframe = document.querySelector(".pdf-iframe");



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
        if (linkTypeData == "PDF" && embedLinkData) {
            pdfIframe.src = embedLinkData;
            pdfIframe.style.display = "flex";
            resourceLinkEmbedSection.style.display = "flex";
        } else if (linkTypeData == "Youtube" && embedLinkData) {
            youtubeIframe.src = embedLinkData;
            youtubeIframe.style.display = "flex";
            resourceLinkEmbedSection.style.display = "flex";
        } else {
            window.open(linkData, '_blank');
        }
    });
});

    