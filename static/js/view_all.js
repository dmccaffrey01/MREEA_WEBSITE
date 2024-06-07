document.addEventListener("DOMContentLoaded", () => {
    let viewAllBtns = document.querySelectorAll(".view-all-btn");
    let form = document.querySelector(".view-all-form");
    let input = document.querySelector("#id_view_all");

    viewAllBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            let viewAllAttr = btn.getAttribute("data-view-all");

            input.value = viewAllAttr;

            form.submit();
        });
    });
});