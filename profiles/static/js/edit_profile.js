let toggleSelect = (selectedContainer, selectOptionsContainer, selectIcon) => {
    selectedContainer.classList.toggle("open");
    selectOptionsContainer.classList.toggle("open");
    selectIcon.classList.toggle("fa-expand");
    selectIcon.classList.toggle("fa-compress");
    selectIcon.classList.toggle("red-text");
}

document.addEventListener("DOMContentLoaded", () => {
    const selectContainers = document.querySelectorAll(".select-container");

    selectContainers.forEach(selectContainer => {

        let hiddenInputContainer = selectContainer.querySelector(".hidden-input-container");

        let hiddenInput = hiddenInputContainer.querySelector("input");

        let selectedContainer = selectContainer.querySelector(".selected-container");

        let selectName = selectedContainer.querySelector(".select-name");
        
        let selectIcon = selectedContainer.querySelector(".fa-solid");

        let selectOptionsContainer = selectContainer.querySelector(".select-options-container");

        selectedContainer.addEventListener("click", () => {
            toggleSelect(selectedContainer, selectOptionsContainer, selectIcon);
        });

        let selectItems = selectOptionsContainer.querySelectorAll(".select-item");

        selectItems.forEach(selectItem => {
            selectItem.addEventListener("click", () => {
                let selectItemName = selectItem.getAttribute("data-name");
                let selectItemFriendlyName = selectItem.getAttribute("data-friendly-name");
                
                hiddenInput.value = selectItemName;
                selectName.innerHTML = selectItemFriendlyName;

                toggleSelect(selectedContainer, selectOptionsContainer, selectIcon);
            });
        });
    });

    const saveButton = document.querySelector(".save-btn");

    saveButton.addEventListener("click", (e) => {
        e.preventDefault();

        let hiddenInputContainers = document.querySelectorAll(".hidden-input-container");

        hiddenInputContainers.forEach(hiddenInputContainer => {
            let hiddenInput = hiddenInputContainer.querySelector("input");

            if (!hiddenInput.value) {
                hiddenInput.value = hiddenInputContainer.getAttribute("data-current-profile");
            }
        });

        let form = document.querySelector(".form");

        form.submit();
    });

    const bioInput = document.querySelector(".bio-input-container textarea");
    let bioCount = document.querySelector(".bio-container .bio-count");
    let maxCountText;

    bioInput.addEventListener("keydown", () => {
        window.setTimeout(() => {
            let value = bioInput.value.normalize('NFC');

            let count = value.length;

            let newLineCount = (value.match(/\n/g) || []).length * 1;

            let total = count + newLineCount;

            bioCount.textContent = `${total}`;

            if (total == 2999) {
                maxCountText = value;
            }

            if (total > 2999) {
                bioInput.value = maxCountText;
                bioCount.textContent = 2999;
            }
        });
    });
});