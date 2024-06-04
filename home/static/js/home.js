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

document.addEventListener("DOMContentLoaded", () => {
    let carouselWrapper = document.querySelector(".carousel-wrapper");
    let carouselContainer = document.querySelector(".carousel-container");
    let carouselWrapperWidth = carouselWrapper.offsetWidth; 

    let numberOfCarouselItems = carouselContainer.querySelectorAll(".carousel-item").length;
    let maxCarouselNum = numberOfCarouselItems - 1;

    let carouselDirectionBtns = document.querySelectorAll(".carousel-direction-btn");

    carouselDirectionBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            let carouselNum = Number(carouselContainer.getAttribute("data-num"));
            let increment = Number(btn.getAttribute("data-increment"));

            let newCarouselNum = carouselNum + increment;

            if (newCarouselNum < 0 || newCarouselNum > maxCarouselNum) {
                return;
            } else {
                carouselContainer.setAttribute("data-num", `${newCarouselNum}`)

                carouselTranslate = carouselWrapperWidth * newCarouselNum * -1;

                carouselContainer.style.translate = `${carouselTranslate}px`;

                carouselDirectionBtns.forEach(cBtn => {
                    if (cBtn.classList.contains("no-move")) {
                        cBtn.classList.remove("no-move");
                    }
                });

                if (newCarouselNum == 0 && increment < 0) {
                    btn.classList.add("no-move");
                } else if (newCarouselNum == maxCarouselNum &&  increment > 0) {
                    btn.classList.add("no-move");
                }
            }
        });
    });
});