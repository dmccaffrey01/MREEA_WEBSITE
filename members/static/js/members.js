document.addEventListener("DOMContentLoaded", () => {
    let selectContainer = document.querySelector(".custom-select-container");
    let selectOptions = document.querySelector(".custom-select-options-container");
    let closeSelectBtn = document.querySelector(".close-select-btn");
    let classCheckboxes = document.querySelectorAll(".class-checkbox-input");
    let numSelected = document.querySelector(".number-selected");
    let selectAllCheckboxes = document.querySelectorAll(".select-all-checkbox");
    let allCheckboxes = document.querySelectorAll(".checkbox-input");
    let selectAllCheckbox = document.querySelector(".select-all-checkbox-mega");

    selectContainer.addEventListener("click", () => {
        selectOptions.classList.add("show");
    });

    selectAllCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("click", () => {
            let categoryName = checkbox.getAttribute("data-category-name");
            if (checkbox.checked) {
                if (categoryName == "all_categories") {
                    allCheckboxes.forEach(cb => {
                        cb.checked = true;
                    });
                } else {
                    newCheckboxes = document.querySelectorAll(`.${categoryName}-class`);
                    newCheckboxes.forEach(cb => {
                        cb.checked = true;
                    });
                }
            } else {
                if (categoryName == "all_categories") {
                    allCheckboxes.forEach(cb => {
                        cb.checked = false;
                    });
                } else {
                    newCheckboxes = document.querySelectorAll(`.${categoryName}-class`);
                    newCheckboxes.forEach(cb => {
                        cb.checked = false;
                    });
                }
                if (selectAllCheckbox.checked) {
                    selectAllCheckbox.checked = false;
                }
            }
        });
    });

    allCheckboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            if (!cb.checked && selectAllCheckbox.checked) {
                selectAllCheckbox.checked = false;
            }
        });
    });

    closeSelectBtn.addEventListener("click", () => {
        let numChecked = 0;
        classCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                numChecked += 1;
            }
        });
        numSelected.innerHTML = numChecked;
        selectOptions.classList.remove("show");
    });

    let searchBtn = document.querySelector(".search-btn");

    searchBtn.addEventListener("click", (e) => {
        e.preventDefault();

        let selectedClassesArray = [];

        classCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                let className = checkbox.getAttribute("data-class-name");
                selectedClassesArray.push(className);
            }
        });

        let selectedClassesString = selectedClassesArray.join(", ");

        let classesInput = document.querySelector("#id_classes");
        classesInput.value = selectedClassesString;
        
        let form = document.querySelector(".form");

        form.submit();
    });
});