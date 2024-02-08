const rememberLabel = document.querySelector(".remember-label");
const rememberBox = document.querySelector("#id_remember");

rememberLabel.addEventListener("click", () => {
    rememberBox.checked = !rememberBox.checked;
});