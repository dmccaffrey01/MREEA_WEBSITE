const formInputs = document.querySelectorAll("input");

formInputs.forEach((input) => {
    let id = input.getAttribute("id");
    if (id == "id_title") {
        input.placeholder = "Quarterly Meeting";
    } else if (id == "id_start_date") {
        input.placeholder = "Format: YYYY-MM-DD HH:MM:SS (eg. 2023-01-01 12:00:00)";
    } else if (id == "id_end_date") {
        input.placeholder = "Format: YYYY-MM-DD HH:MM:SS (eg. 2023-01-01 12:00:00)";
    } else if (id == "id_location") {
        input.placeholder = "Zoom";
    }
});

const selectResourcesFormBtn = document.querySelector(".event-form-select-resources-btn");
const selectResourcesOverlay = document.querySelector(".event-form-select-overlay");
const selectResourcesWrapper = document.querySelector(".event-form-select-resources-wrapper");
const selectResourceCloseBtn = document.querySelector(".select-resource-close-btn");
const selectResourceConfirmBtn = document.querySelector(".select-resource-confirm-btn");
const selectResourceCount = document.querySelector(".select-resource-count");
const selectResourceItems = document.querySelectorAll(".select-resource-item");
const selectResourceInput = document.querySelector("#selectedResources");
const eventFormResourceCount = document.querySelector(".event-form-resource-count");


const openSelectResource = () => {
    selectResourcesOverlay.style.display = "flex";
    selectResourcesWrapper.style.display = "flex";
}

const closeSelectResource = () => {
    selectResourcesOverlay.style.display = "none";
    selectResourcesWrapper.style.display = "none";
}

selectResourcesFormBtn.addEventListener("click", () => {
    openSelectResource();
});

selectResourceCloseBtn.addEventListener("click", () => {
    closeSelectResource();
})

const updateResourceCount = () => {
    let selectedCount = 0;

    selectResourceItems.forEach(item => {
        if (item.classList.contains("selected")) {
            selectedCount++;
        }
    });

    selectResourceCount.innerHTML = selectedCount;

    return selectedCount;
}

selectResourceItems.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("selected");
        updateResourceCount();
    });
    
});

const updateResourceInput = () => {
    let selectedItems = [];

    selectResourceItems.forEach(item => {
        if (item.classList.contains("selected")) {
            
            let linkName = item.textContent;
            let link = linkName.split(" - ")[2];
            selectedItems.push(link);
        }
    });

    let selectedItemsJson = JSON.stringify(selectedItems);

    selectResourceInput.value = selectedItemsJson;
}

const updateEventFormResourceCount = (selectedCount) => {
    eventFormResourceCount.innerHTML = selectedCount;
}

selectResourceConfirmBtn.addEventListener("click", () => {
    updateResourceInput();

    closeSelectResource();

    let selectedCount = updateResourceCount();

    updateEventFormResourceCount(selectedCount);
});


const selectImgFormBtn = document.querySelector(".event-form-select-image-btn");
const selectImgOverlay = document.querySelector(".event-form-select-overlay");
const selectImgWrapper = document.querySelector(".event-form-select-image-wrapper");
const selectImgCloseBtn = document.querySelector(".select-image-close-btn");
const selectImgConfirmBtn = document.querySelector(".select-image-confirm-btn");
const selectImgItems = document.querySelectorAll(".select-image-item");
const selectImgInput = document.querySelector("#selectedImage");

const openSelectImage = () => {
    selectImgOverlay.style.display = "flex";
    selectImgWrapper.style.display = "flex";
}

const closeSelectImage = () => {
    selectImgOverlay.style.display = "none";
    selectImgWrapper.style.display = "none";
}

selectImgFormBtn.addEventListener("click", () => {
    openSelectImage();
});

selectImgCloseBtn.addEventListener("click", () => {
    closeSelectImage();
})

const unselectOtherItems = (i) => {
    selectImgItems.forEach((item, index) => {
        if (index != i) {
            item.classList.remove("selected");
        }
    });
}

selectImgItems.forEach((item, i) => {
    item.addEventListener("click", () => {
        item.classList.toggle("selected");
        unselectOtherItems(i);
    });
    
});

const updateImageInput = () => {
    let url;
    
    selectImgItems.forEach(item => {
        if (item.classList.contains("selected")) {
            url = item.querySelector(".hidden-select-image-src-data").innerText;
            uuid = item.querySelector(".hidden-select-image-uuid-data").innerText;
        }
    });
    document.querySelector(".event-form-img-preview").src = url;

    selectImgInput.value = uuid;
}

selectImgConfirmBtn.addEventListener("click", () => {
    updateImageInput();

    closeSelectImage();
});

const deleteEventBtn = document.querySelector(".delete-event-btn");
const cancelDeleteBtn = document.querySelector(".cancel-delete-btn");
const confirmDeleteContainer = document.querySelector(".confirm-delete-container");

deleteEventBtn.addEventListener("click", () => {
    confirmDeleteContainer.style.display = "flex";

    cancelDeleteBtn.addEventListener("click", () => {
        confirmDeleteContainer.style.display = "none";
    });
});