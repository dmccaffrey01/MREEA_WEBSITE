document.addEventListener("DOMContentLoaded", () => {
    const bioInput = document.querySelector(".bio-text textarea");
    let bioCount = document.querySelector(".bio-container .bio-count");
    let maxCountText;

    bioInput.addEventListener("keydown", () => {
        window.setTimeout(() => {
            let value = bioInput.value.normalize('NFC');

            let count = value.length;

            let newLineCount = (value.match(/\n/g) || []).length * 1;

            let total = count + newLineCount;

            bioCount.textContent = `${total}`;

            if (total == 500) {
                maxCountText = value;
            }

            if (total > 500) {
                bioInput.value = maxCountText;
                bioCount.textContent = 500;
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let newLinkBtn = document.querySelector(".new-link-btn");
    let infoItemTextContainer = document.querySelector(".info-item-text-container");

    newLinkBtn.addEventListener("click", () => {
        let links = document.querySelectorAll(".link-input");
        let numProfileLinks = links.length;

        let newLink = document.createElement("div");
        newLink.classList.add("input-wrapper");
        newLink.innerHTML = `
        <div class="info-visit-link visit-link">
            <div class="icon-container btn-icon-left">
                <svg xmlns="http://www.w3.org/2000/svg" class="dark-text" viewBox="0 0 256 256">
                    <path d="M128 24a104 104 0 1 0 104 104A104.12 104.12 0 0 0 128 24m87.62 96h-39.83c-1.79-36.51-15.85-62.33-27.38-77.6a88.19 88.19 0 0 1 67.22 77.6ZM96.23 136h63.54c-2.31 41.61-22.23 67.11-31.77 77c-9.55-9.9-29.46-35.4-31.77-77m0-16c2.31-41.61 22.23-67.11 31.77-77c9.55 9.93 29.46 35.43 31.77 77Zm11.36-77.6C96.06 57.67 82 83.49 80.21 120H40.37a88.19 88.19 0 0 1 67.22-77.6M40.37 136h39.84c1.82 36.51 15.85 62.33 27.38 77.6A88.19 88.19 0 0 1 40.37 136m108 77.6c11.53-15.27 25.56-41.09 27.38-77.6h39.84a88.19 88.19 0 0 1-67.18 77.6Z" />
                </svg>
                <span class="sr-only">Globe Icon</span>
            </div>
            <p class="dark-text-2 small-text">Profile Link ${numProfileLinks + 1}</p>
        </div>
        <div class="input-container col-2">
            <label for="id_pl_url_${numProfileLinks + 1}" class="sr-only">Profile Link Url ${numProfileLinks + 1}</label>
            <input type="text" name="id_pl_url_${numProfileLinks + 1}" id="id_pl_url_${numProfileLinks + 1}" class="link-input" value="">
        </div>
        `;
        infoItemTextContainer.insertBefore(newLink, newLinkBtn);

        listenForInfoLinkHover(newLink);
    });
});

let handleDeleteLinkBtn = (infoLink) => {
    let inputWrapper = infoLink.closest(".input-wrapper");
    let input = inputWrapper.querySelector("input");

    let inputId = input.getAttribute("id");

    if (inputId == "id_email" || inputId == "id_phone_number") {
        input.value = "";
    } else {
        inputWrapper.remove();
    }
}

let listenForInfoLinkHover = (infoLink) => {
    let deleteBtn = document.createElement("div");
    deleteBtn.classList.add("icon-container");
    deleteBtn.classList.add("color-error");
    deleteBtn.classList.add("hide");
    deleteBtn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" class="white-text" viewBox="0 0 24 24">
        <path fill-rule="evenodd" d="M17.707 7.707a1 1 0 0 0-1.414-1.414L12 10.586L7.707 6.293a1 1 0 0 0-1.414 1.414L10.586 12l-4.293 4.293a1 1 0 1 0 1.414 1.414L12 13.414l4.293 4.293a1 1 0 1 0 1.414-1.414L13.414 12z" clip-rule="evenodd" />
    </svg>
    <span class="sr-only">XMark Icon</span>
    `;

    let icon = infoLink.querySelector(".icon-container");

    infoLink.insertBefore(deleteBtn, icon);

    icon.addEventListener("mouseenter", () => {
        icon.classList.add("hide");
        deleteBtn.classList.remove("hide");
    });

    deleteBtn.addEventListener("mouseleave", () => {
        icon.classList.remove("hide");
        deleteBtn.classList.add("hide");
    });

    deleteBtn.addEventListener("click", () => {
        handleDeleteLinkBtn(infoLink);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    let infoVisitLinks = document.querySelectorAll(".info-visit-link");

    infoVisitLinks.forEach(infoLink => {
        if (!infoLink.classList.contains("new-link-btn")) {
            listenForInfoLinkHover(infoLink);
        }
    });
});

function getFirstInvalidElement(form) {
    // Loop through each element in the form
    for (let i = 0; i < form.elements.length; i++) {
      // Check if the element is invalid
      if (!form.elements[i].checkValidity()) {
        // Return the first invalid element
        return form.elements[i];
      }
    }
    // If all elements are valid, return null
    return null;
  }

document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.querySelector(".save-btn");

    saveButton.addEventListener("click", (e) => {
        e.preventDefault();

        let linkInputs = document.querySelectorAll(".link-input");
        let arrOfLinks = [];
        let arrOfLinksInput = document.querySelector("#id_arr_of_links");

        linkInputs.forEach(input => {
            if (input.value) {
                let id = input.getAttribute("id");
                arrOfLinks.push(id);
            }
        });
        
        arrOfLinksInput.value = JSON.stringify(arrOfLinks); 

        let form = document.querySelector(".form");

        if (form.checkValidity()) { // Check if the form is valid
            form.submit(); // Submit the form
        } else {
            let  firstInvalidElement = getFirstInvalidElement(form);
            if (firstInvalidElement) {
                firstInvalidElement.focus();
            }
        }
    });
});

