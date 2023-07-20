
const selectElements = document.querySelectorAll("select");

selectElements.forEach((selectElement) => {
    
    let selectOptions = selectElement.querySelectorAll("option");

    let numOptions = selectOptions.length;

    let rect = selectElement.getBoundingClientRect();
    let parentElement = selectElement.parentElement;
    let parentHeight = parentElement.offsetHeight;
    let grandParentElement = parentElement.parentElement;
    let parentElementRect = grandParentElement.getBoundingClientRect();
    let x = rect.left - parentElementRect.left;
    let y = rect.top - parentElementRect.top;
    if (numOptions > 5) {

        selectElement.addEventListener("click", () => { 
            selectElement.blur();
        });

        selectElement.addEventListener("focus", () => { 
            selectElement.size = 5;
            selectElement.style.position = "absolute";
            selectElement.style.left = x + "px";
            selectElement.style.top = y + "px";
            parentElement.style.height = parentHeight + "px";
        });

        selectElement.addEventListener("blur", () => { 
            selectElement.size = 1;
            selectElement.style.position = "static";
        });
    }
});





  
