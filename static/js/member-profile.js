const expandBioBtn = document.querySelector(".expand-bio-btn");
const expandClosedBioBtn = document.querySelector(".close-expand-bio-btn");

expandBioBtn.addEventListener("click", () => {
    if (!(expandBioBtn.classList.contains("active"))) {
        expandBioBtn.classList.add("active");
        expandClosedBioBtn.classList.add("active");
    }
});

expandClosedBioBtn.addEventListener("click", () => {
    expandBioBtn.classList.remove("active");
    expandClosedBioBtn.classList.remove("active");
});