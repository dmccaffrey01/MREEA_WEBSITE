document.addEventListener("DOMContentLoaded", () => {
    const checkoutOverlay = document.querySelector(".checkout-overlay");
    if (checkoutOverlay) {
        const cancelBtn = document.querySelector(".cancel-btn");
        const checkoutPopups = document.querySelectorAll(".checkout-popup");
        const returnBtn = document.querySelector(".return-btn");
        const completeBtn = document.querySelector(".complete-btn");
        
        cancelBtn.addEventListener("click", () => {
            checkoutPopups.forEach(checkoutPopup => {
                checkoutPopup.classList.toggle("show");
            });
            
        });

        returnBtn.addEventListener("click", () => {
            checkoutPopups.forEach(checkoutPopup => {
                checkoutPopup.classList.toggle("show");
            });
        });

        completeBtn.addEventListener("click", () => {
            checkoutOverlay.style.display = "none";
        });
    }
});