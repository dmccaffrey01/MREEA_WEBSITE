document.addEventListener("DOMContentLoaded", () => {
    let eventBtnsContainer = document.querySelector(".management-btns-container");
    let deleteBtnWrapper = eventBtnsContainer.querySelector(".delete-btn-wrapper");

    if (deleteBtnWrapper) {
        let deleteBtn = deleteBtnWrapper.querySelector(".delete-btn");
        let confirmDeleteBtn = deleteBtnWrapper.querySelector(".confirm-delete-btn");
        let denyDeleteBtn = deleteBtnWrapper.querySelector(".deny-delete-btn");

        deleteBtn.addEventListener("click", () => {
            if (confirmDeleteBtn.classList.contains("hide")) {
                confirmDeleteBtn.classList.remove("hide");
                deleteBtnWrapper.classList.toggle("clicked");
            }
        });

        confirmDeleteBtn.addEventListener("click", () => {
            deleteBtnWrapper.classList.toggle("clicked");
        });

        deleteBtnWrapper.addEventListener("mouseleave", () => {
            if (!confirmDeleteBtn.classList.contains("hide")) {
                confirmDeleteBtn.classList.add("hide");
            }
        });

        denyDeleteBtn.addEventListener("click", () => {
            if (!confirmDeleteBtn.classList.contains("hide")) {
                confirmDeleteBtn.classList.add("hide");
            }
        });
    }
});