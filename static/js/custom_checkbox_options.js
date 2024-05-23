let updateNumberSelected = (checkboxes, numberSelected) => {
    let num = 0;

    checkboxes.forEach(checkbox => {
        if (checkbox.checked && (!checkbox.classList.contains("select-all-checkbox"))) {
            num++;
        }
    });

    numberSelected.innerText = num;
}

let checkAllBoxes = (checkboxes, selectAll, isChecked) => {
    checkboxes.forEach(checkbox => {
        selectAllTarget = checkbox.getAttribute("data-select-all-target");
        let isSelectAll = (selectAllTarget == selectAll) || (selectAll == "all");
        if (isSelectAll) {
            checkbox.checked = isChecked;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    let customCheckboxOptionsInputContainer = document.querySelectorAll(".custom-checkbox-options-input-container");

    customCheckboxOptionsInputContainer.forEach(inputContainer => {
        let btn = inputContainer.querySelector(".custom-checkbox-options-btn");

        btn.addEventListener("click", () => {
            toggleElementShow(inputContainer);
        });

        let numberSelected = btn.querySelector(".number-selected");

        let checkboxes = inputContainer.querySelectorAll(".checkbox-input");

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener("click", () => {
                let selectAll = checkbox.getAttribute("data-select-all");
                if (selectAll) {
                    checkAllBoxes(checkboxes, selectAll, checkbox.checked);
                }
                updateNumberSelected(checkboxes, numberSelected);
            });
        });
    });
});