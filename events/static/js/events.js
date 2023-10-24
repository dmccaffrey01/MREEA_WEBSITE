document.addEventListener("DOMContentLoaded", () => {
    const heroImg = document.querySelector(".hero-img-container");

    heroImg.classList.add("active");
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

const hiddenElements = document.querySelectorAll(".hidden");
hiddenElements.forEach((el) => observer.observe(el));