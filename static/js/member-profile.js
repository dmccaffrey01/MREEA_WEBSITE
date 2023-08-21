const bioNumberCounter = document.querySelector('.bio-number-counter');
const bioInput = document.querySelector('#id_bio');

const getChars = () => {
    let bioValue = bioInput.value;
    let chars = bioValue.length;

    return chars;
}

const updateBioCounter = (chars) => {
    bioNumberCounter.innerHTML = chars;
}

document.addEventListener('DOMContentLoaded', () => {
    let chars = getChars();
    updateBioCounter(chars);
});

bioInput.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace') {
        let chars = getChars() - 1;
        updateBioCounter(chars);
    }
});

bioInput.addEventListener('input', () => {
    let chars = getChars();
    updateBioCounter(chars);

    if (chars > 2000) {
        let value = bioInput.value;
        let newValue = value.slice(0, 2000);
        bioInput.value = newValue;
        updateBioCounter(2000);
    }
});
