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

const updateBioHeight = () => {
    let bioContainer = document.querySelector(".bio-container");
    let gridGroupCol = document.querySelector(".grid-group-col-container");

    let gridHeight = gridGroupCol.clientHeight;

    bioContainer.style.height = `${gridHeight}px`;
}

document.addEventListener("DOMContentLoaded", () => {
    window.setTimeout(() => {
        updateBioHeight();
    }, 500);
    
});

document.addEventListener("DOMContentLoaded", () => {
    let newLinkBtn = document.querySelector(".new-link-btn");
    let newLinksContainer = document.querySelector(".new-links-container");

    newLinkBtn.addEventListener("click", () => {
        let profileLinks = document.querySelectorAll(".profile-link-container");
        let numProfileLinks = profileLinks.length;

        let newLink = document.createElement("div");
        newLink.classList.add("contact-btn");
        newLink.classList.add("container-row");
        newLink.classList.add("profile-link-container");
        newLink.innerHTML = `
                            <p class="dark-text red-text container-col"><span class="sr-only">Link Icon</span><i class="fa-solid fa-link"></i></p>
                            <div class="input-group-container container-row justify-start">
                                <div class="input-group container-col align-start">
                                    <label for="id_pl_link_${numProfileLinks + 1}" class="input-label dark-text">Link ${numProfileLinks + 1}</label>
                                    <input type="text" name="id_pl_link_${numProfileLinks + 1}" id="id_pl_link_${numProfileLinks + 1}" class="link-input" required>
                                </div>
                                <div class="input-group container-col align-start">
                                    <label for="id_pl_friendly_name_${numProfileLinks + 1}" class="input-label dark-text">Link Name ${numProfileLinks + 1}</label>
                                    <input type="text" name="id_pl_friendly_name_${numProfileLinks + 1}" id="id_pl_friendly_name_${numProfileLinks + 1}" required>
                                </div>
                                <div class="sr-only input-group container-col align-start">
                                    <label for="id_pl_name_${numProfileLinks + 1}" class="input-label dark-text">Link Name</label>
                                    <input type="text" name="id_pl_name_${numProfileLinks + 1}" id="id_pl_name_${numProfileLinks + 1}">
                                </div>
                            </div>
        `;
        newLinksContainer.appendChild(newLink);
        newLinksContainer.classList.add("show");
        updateBioHeight();
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
        let numOfLinks = 0;
        let numOfLinksInput = document.querySelector("#id_num_of_links");

        linkInputs.forEach(input => {
            if (input.value) {
                numOfLinks++;
            }
        });

        numOfLinksInput.value = numOfLinks;

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

