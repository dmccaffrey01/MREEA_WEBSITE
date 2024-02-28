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