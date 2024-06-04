document.addEventListener("DOMContentLoaded", () => {
    let input = document.querySelector("#id_message");
    let previewTextContainer = document.querySelector(".preview-text");

    input.addEventListener("input", () => {
        let inputValue = input.value;
        
        // Replace new lines with <br> tags
        let formattedText = inputValue.replace(/\n/g, '<br>');
        
        previewTextContainer.innerHTML = formattedText;
    });
});