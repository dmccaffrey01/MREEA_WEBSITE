/**
 * Open and close hamburger menu
 */
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const header = document.getElementsByTagName("header")[0];
const navLinks = document.querySelectorAll(".nav-link")

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
    header.classList.toggle("active");
});

navLinks.forEach((n, i) => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    header.classList.remove("active");
}));

navLinks.forEach((navLink) => {
    navLink.addEventListener("click", () => {
        navLinks.forEach((link) => {
            link.classList.remove("active");
        });
    
        navLink.classList.add("active");
    });
  
    if (navLink.href === window.location.href) {
        navLink.classList.add("active");
    }
});

const navItemDropdownBtns = document.querySelectorAll(".nav-item-dropdown-btn");

navItemDropdownBtns.forEach(dropdownBtn => {
    dropdownBtn.addEventListener("click", () => {
        let dropdownContainer = dropdownBtn.querySelector(".nav-item-dropdown-container");

        dropdownContainer.classList.toggle("active");
        console.log(dropdownContainer)
    });
});