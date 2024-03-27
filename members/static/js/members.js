document.addEventListener("DOMContentLoaded", () => {
    let selectContainer = document.querySelector(".custom-select-container");
    let selectOptions = document.querySelector(".custom-select-options-container");
    let closeSelectBtn = document.querySelector(".close-select-btn");
    let classCheckboxes = document.querySelectorAll(".class-checkbox-input");
    let numSelected = document.querySelector(".number-selected");
    let selectAllCheckboxes = document.querySelectorAll(".select-all-checkbox");
    let allCheckboxes = document.querySelectorAll(".checkbox-input");
    let selectAllCheckbox = document.querySelector(".select-all-checkbox-mega");

    let updateSelectedNumber = () => {
        let numChecked = 0;
        classCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                numChecked += 1;
            }
        });
        numSelected.innerHTML = numChecked;
    }

    updateSelectedNumber();

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
        updateSelectedNumber();
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

const getClassesData = async (username) => {
    try {
        const response = await fetch(`get_member_classes/${username}/`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching member classes:', error);
        return null;
    }
};

document.addEventListener("DOMContentLoaded", async () => {
    let searchResultsSection = document.querySelector(".search-results-section");

    if (searchResultsSection) {
        let classesTexts = document.querySelectorAll(".classes-text");

        for (const text of classesTexts) {
            let username = text.getAttribute("data-username");

            let classesData = await getClassesData(username);

            if (classesData) {
                let hoverContainer = document.querySelector(`#id_${username}_classes_hover`);

                let categoryAndClasses = classesData.category_and_classes;

                for (const category of categoryAndClasses) {
                    let categoryContainerDiv = document.createElement("div");
                    categoryContainerDiv.classList.add("category-container");
                    categoryContainerDiv.classList.add("container-col");
                    categoryContainerDiv.classList.add("align-start");
                    categoryContainerDiv.classList.add("justify-start");

                    categoryContainerDiv.innerHTML = `
                        <p class="category-hover-text dark-text small-text">${category.category_name}</p>
                    `;

                    let classContainerDiv = document.createElement("div");
                    classContainerDiv.classList.add("class-container");
                    classContainerDiv.classList.add("container-col");
                    classContainerDiv.classList.add("align-start");
                    classContainerDiv.classList.add("justify-start");

                    for (const cls of category.classes) {

                        let classTextP = document.createElement("p");
                        classTextP.classList.add("class-hover-text");
                        classTextP.classList.add("dark-text");
                        classTextP.classList.add("small-text");
                        classTextP.innerHTML = `
                            <span class="fa-icon-left red-text"><i class="fa-regular fa-circle-check"></i></span> ${cls}
                        `;
                        classContainerDiv.appendChild(classTextP);
                    }

                    categoryContainerDiv.appendChild(classContainerDiv);

                    hoverContainer.appendChild(categoryContainerDiv);
                }

                text.addEventListener("mouseenter", () => {
                    hoverContainer.classList.add("show");
                });

                text.addEventListener("mouseleave", () => {
                    hoverContainer.classList.remove("show");
                });

                text.addEventListener("click", () => {
                    hoverContainer.classList.toggle("show");
                });
            }
        }
    }
});
