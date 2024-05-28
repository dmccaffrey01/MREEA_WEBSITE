let noPackageSelectedError = () => {
    const defaultSelectItem = document.querySelector(".default-select-item");

    displayErrorMessage("Please select a package!", defaultSelectItem);
}

document.addEventListener("DOMContentLoaded", () => {
    const singlePackageInfo = document.querySelector(".single-package-info-container");

    let submitBtn = document.querySelector(".submit-btn");

    if (singlePackageInfo) {
        let packageNameInput = document.querySelector("#id_package_name");

        let packageName = document.querySelector(".single-package-select-item").getAttribute("data-name");

        packageNameInput.value = packageName;

        let selectItem = document.querySelector(".single-package-select-item");

        let checkoutUrl = selectItem.getAttribute("data-checkout_url")

        submitBtn.setAttribute("data-checkout_url", checkoutUrl);
    } else {
        const selectContainerItems = document.querySelector(".select-container-items");
        const defaultSelectItem = document.querySelector(".default-select-item");
        const packagePriceText = document.querySelector(".package-price-text");
        const packageDurationText = document.querySelector(".package-duration-text");
        let defaultFriendlyNameText = defaultSelectItem.querySelector(".default-friendly-name-text");
        let selectItems = selectContainerItems.querySelectorAll(".select-item");

        defaultSelectItem.addEventListener("click", () => {
            selectContainerItems.classList.toggle("open");
            defaultSelectItem.classList.toggle("open");
        });

        selectItems.forEach(selectItem => {
            selectItem.addEventListener("click", () => {

                let friendlyNameText = selectItem.querySelector(".friendly-name-text");
                let priceText = selectItem.querySelector(".price-text");

                defaultFriendlyNameText.innerText = friendlyNameText.innerText;

                selectContainerItems.classList.toggle("open");
                defaultSelectItem.classList.toggle("open");

                packagePriceText.innerText = priceText.innerText;

                let packageDuration = selectItem.getAttribute("data-duration");
                packageDurationText.innerText = packageDuration;

                let packageNameInput = document.querySelector("#id_package_name");
                let packageName = selectItem.getAttribute("data-name");
                packageNameInput.value = packageName;

                let checkoutUrl = selectItem.getAttribute("data-checkout_url")

                submitBtn.setAttribute("data-checkout_url", checkoutUrl);
            });
        });
    }

    submitBtn.addEventListener("click", (e) => {
        e.preventDefault();

        let checkoutUrl = submitBtn.getAttribute("data-checkout_url");

        if (!checkoutUrl) {
            noPackageSelectedError();
            return;
        }

        window.open(checkoutUrl, "_blank");

        let form = document.querySelector(".form");
        form.submit();
    });
});
