document.addEventListener("DOMContentLoaded", () => {
    window.setTimeout(() => {
        let bioContainer = document.querySelector(".bio-container");
        let gridGroupCol = document.querySelector(".grid-group-col-container");

        let gridHeight = gridGroupCol.offsetHeight;

        bioContainer.style.height = `${gridHeight}px`;
    }, 500);
});

document.addEventListener("DOMContentLoaded", () => {
    let copyBtns = document.querySelectorAll(".copy-btn");

    copyBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            let copyData = btn.getAttribute("data-copy");

            navigator.clipboard.writeText(copyData);
        });
    });
});