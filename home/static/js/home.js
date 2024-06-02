const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("observer-show");
        }
    });
}, { threshold: 0.5 });

const observerElements = document.querySelectorAll(".observer");
observerElements.forEach((el) => observer.observe(el));

document.addEventListener("DOMContentLoaded", () => {
    let scroller = document.querySelector(".scroller");
    let scrollerInner = scroller.querySelector(".scroller-inner");

    let scrollerContent = Array.from(scrollerInner.children);

    scrollerContent.forEach(item => {
        let duplicatedItem = item.cloneNode(true);
        duplicatedItem.setAttribute('aria-hidden', 'true');
        scrollerInner.appendChild(duplicatedItem);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let viewAllBtn = document.querySelector(".view-all-btn");
    let benefitCardsWrapper = document.querySelector(".benefit-cards-wrapper");

    viewAllBtn.addEventListener("click", () => {
        benefitCardsWrapper.classList.add("view-all");
    });
});