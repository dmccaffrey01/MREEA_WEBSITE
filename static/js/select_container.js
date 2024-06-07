document.addEventListener("DOMContentLoaded", () => {
    let selectContainers = document.querySelectorAll(".select-container");

    selectContainers.forEach(selectContainer => {
        const selectContainerItems = selectContainer.querySelector(".select-container-items");
        const defaultSelectItem = selectContainer.querySelector(".default-select-item");
        let defaultFriendlyNameText = defaultSelectItem.querySelector(".default-friendly-name-text");
        let defaultItemIcon = defaultSelectItem.querySelector(".item-icon");
        let selectItems = selectContainerItems.querySelectorAll(".select-item");
        let type = selectContainer.getAttribute("data-type");

        defaultSelectItem.addEventListener("click", () => {
            selectContainerItems.classList.toggle("open");
        });

        selectItems.forEach(selectItem => {
            selectItem.addEventListener("click", () => {

                let friendlyNameText = selectItem.querySelector(".friendly-name-text");

                defaultFriendlyNameText.innerText = friendlyNameText.innerText;

                selectContainerItems.classList.toggle("open");

                let typeNameInput = document.querySelector(`#id_${type}_name`);
                let typeName = selectItem.getAttribute("data-name");
                typeNameInput.value = typeName;

                if (defaultItemIcon) {
                    let selectItemIcon = selectItem.querySelector(".item-icon");
                    defaultItemIcon.innerHTML = selectItemIcon.innerHTML;
                }

            });
        });
    });
});