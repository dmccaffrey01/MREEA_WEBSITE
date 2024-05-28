const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

const hiddenElements = document.querySelectorAll(".hidden");
hiddenElements.forEach((el) => observer.observe(el));

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

let moveCarousel = (num) => {
    let carouselWrapper = document.querySelector(".carousel-wrapper");
    let carouselDots = document.querySelectorAll(".carousel-dots-container");
}

document.addEventListener("DOMContentLoaded", () => {
    let carouselDots = document.querySelectorAll(".carousel-dot");

    carouselDots.forEach(dot => {
        dot.addEventListener("click", () => {
            let carouselNum = dot.getAttribute("data-num");

            if (carouselPos != "current") {
                moveCarousel(carouselNum);
            } else {
                return;
            }
        });
    });
});