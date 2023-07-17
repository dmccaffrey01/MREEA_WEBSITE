const formInputs = document.querySelectorAll("input");

formInputs.forEach((input) => {
    let id = input.getAttribute("id");
    if (id == "id_title") {
        input.placeholder = "Quarterly Meeting";
    } else if (id == "id_start_date") {
        input.placeholder = "Format: YYYY-MM-DD HH:MM:SS (eg. 2023-01-01 12:00:00)";
    } else if (id == "id_end_date") {
        input.placeholder = "Format: YYYY-MM-DD HH:MM:SS (eg. 2023-01-01 12:00:00)";
    } else if (id == "id_location") {
        input.placeholder = "Zoom";
    }
});