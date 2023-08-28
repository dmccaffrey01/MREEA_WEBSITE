const linkTypeDropdownBtn = document.querySelector(".link-type-dropdown");
const linkTypeDropdownOptions = document.querySelector(".link-type-dropdown-container");
const linkTypeIcon = document.querySelector(".link-type-icon");

const linkTypeDropdownItems = document.querySelectorAll(".link-type-dropdown-item");
const linkTypeDropdownSelectedText = document.querySelector(".link-type-dropdown-selected-text");

const linkTypeInput = document.querySelector("#id_link_type_input");

linkTypeDropdownBtn.addEventListener("click", () => {
    linkTypeDropdownOptions.classList.toggle("active");
    if (linkTypeDropdownOptions.classList.contains("active")) {
        linkTypeIcon.style.transform = "rotate(-180deg)";
    } else {
        linkTypeIcon.style.transform = "rotate(0deg)";
    }
});


linkTypeDropdownItems.forEach(item => {
    item.addEventListener("click", () => {
        linkTypeDropdownOptions.classList.toggle("active");
        if (linkTypeDropdownOptions.classList.contains("active")) {
            linkTypeIcon.style.transform = "rotate(-180deg)";
        } else {
            linkTypeIcon.style.transform = "rotate(0deg)";
        }

        let newText = item.innerText.trim();
        
        linkTypeDropdownSelectedText.innerText = newText;

        linkTypeInput.value = newText;
    })
});



const categoryDropdownBtn = document.querySelector(".category-dropdown");
const categoryDropdownOptions = document.querySelector(".category-dropdown-container");
const categoryIcon = document.querySelector(".category-icon");

const categoryDropdownItems = document.querySelectorAll(".category-dropdown-item");
const categoryDropdownSelectedText = document.querySelector(".category-dropdown-selected-text");

const categoryInput = document.querySelector("#id_category_input");

categoryDropdownBtn.addEventListener("click", () => {
    categoryDropdownOptions.classList.toggle("active");
    if (categoryDropdownOptions.classList.contains("active")) {
        categoryIcon.style.transform = "rotate(-180deg)";
    } else {
        categoryIcon.style.transform = "rotate(0deg)";
    }
});


categoryDropdownItems.forEach(item => {
    item.addEventListener("click", () => {
        categoryDropdownOptions.classList.toggle("active");
        if (categoryDropdownOptions.classList.contains("active")) {
            categoryIcon.style.transform = "rotate(-180deg)";
        } else {
            categoryIcon.style.transform = "rotate(0deg)";
        }

        let newText = item.innerText.trim();
        
        categoryDropdownSelectedText.innerText = newText;

        categoryInput.value = newText;
    })
});


const subcategoryDropdownBtn = document.querySelector(".subcategory-dropdown");
const subcategoryDropdownOptions = document.querySelector(".subcategory-dropdown-container");
const subcategoryIcon = document.querySelector(".subcategory-icon");

const subcategoryDropdownItems = document.querySelectorAll(".subcategory-dropdown-item");
const subcategoryDropdownSelectedText = document.querySelector(".subcategory-dropdown-selected-text");

const subcategoryInput = document.querySelector("#id_subcategory_input");

subcategoryDropdownBtn.addEventListener("click", () => {
    subcategoryDropdownOptions.classList.toggle("active");
    if (subcategoryDropdownOptions.classList.contains("active")) {
        subcategoryIcon.style.transform = "rotate(-180deg)";
    } else {
        subcategoryIcon.style.transform = "rotate(0deg)";
    }
});


subcategoryDropdownItems.forEach(item => {
    item.addEventListener("click", () => {
        subcategoryDropdownOptions.classList.toggle("active");
        if (subcategoryDropdownOptions.classList.contains("active")) {
            subcategoryIcon.style.transform = "rotate(-180deg)";
        } else {
            subcategoryIcon.style.transform = "rotate(0deg)";
        }

        let newText = item.innerText.trim();
        
        subcategoryDropdownSelectedText.innerText = newText;

        subcategoryInput.value = newText;
    })
});



document.addEventListener("DOMContentLoaded", () => {
    categoryInput.value = "Other";
    linkTypeInput.value = "Other";
    subcategoryInput.value = "None";
});