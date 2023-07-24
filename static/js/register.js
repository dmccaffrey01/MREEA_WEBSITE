const emailInput = document.getElementById('id_email');
const firstNameInput = document.getElementById('id_first_name');
const lastNameInput = document.getElementById('id_last_name');
const phoneNumberInput = document.getElementById('id_phone_number');
const password1Input = document.getElementById('id_password1');
const password2Input = document.getElementById('id_password2');
const form = document.querySelector('form');

const addIcons = (inputs) => {
    
    for (let i = 0; i < inputs.length; i++) {
        let input = inputs[i];
        let iconContainer = document.createElement('div');
        iconContainer.classList.add('account-input-icon-container');

        input.classList.add('form-input');
        
        let inputContainer = input.parentNode;
        inputContainer.classList.add('account-input-container');

        id = input.getAttribute('id');

        let icon;
        if (id == 'id_first_name') {
            icon = `<i class="fa-solid fa-user form-input-icon"></i>`;
            input.placeholder = 'First Name';
        } else if (id == 'id_last_name') {
            icon = `<i class="fa-solid fa-lock form-input-icon"></i>`;
            input.placeholder = 'Last Name';
        } else if (id == 'id_email') {
            icon = `<i class="fa-solid fa-envelope form-input-icon"></i>`;
        } else if (id == 'id_phone_number') {
            icon = `<i class="fa-solid fa-envelope form-input-icon"></i>`;
            input.placeholder = 'Phone Number';
        } else if (id == 'id_password1') {
            icon = `<i class="fa-solid fa-lock form-input-icon"></i>`;
        } else if (id == 'id_password2') {
            icon = `<i class="fa-solid fa-user-lock form-input-icon"></i>`;
        }
        iconContainer.innerHTML = icon;
        inputContainer.appendChild(iconContainer);
        inputContainer.appendChild(input);
    }
}

const getIconArray = () => {
    return [firstNameInput, lastNameInput, emailInput, phoneNumberInput, password1Input, password2Input];
}

document.addEventListener('DOMContentLoaded', () => {
    let inputs = getIconArray();
    console.log(inputs);
    addIcons(inputs);
});