const ctaBtns = document.querySelectorAll('.cta-btn');

const expandBtnArrow = (btnArrow, btn) => {
    let maxWidth = btn.offsetWidth;
    let arrowWidth = btnArrow.offsetWidth;
    let duration = 200;
    let intervalDelay = 10;
    let expandTimes = duration / intervalDelay;
    let widthToExpand = maxWidth - arrowWidth;
    let expandAmount = widthToExpand / expandTimes;

    let i = 1;

    let expandInterval = window.setInterval(() => {
        if (i > Math.ceil(expandTimes)) {
            btnArrow.style.width = maxWidth + 'px';
            clearInterval(expandInterval);
        } else {
            btnArrow.style.width = arrowWidth + (expandAmount * i) + 'px';
            i++;
        }
    }, intervalDelay);
}

const collapseBtnArrow = (btnArrow, btn) => {
    let maxWidth = 80;
    let arrowWidth = btnArrow.offsetWidth;
    let duration = 200;
    let intervalDelay = 10;
    let expandTimes = duration / intervalDelay;
    let widthToExpand = arrowWidth - maxWidth;
    let expandAmount = widthToExpand / expandTimes;

    let i = 1;

    let expandInterval = window.setInterval(() => {
        if (i > Math.ceil(expandTimes)) {
            btnArrow.style.width = maxWidth + 'px';
            clearInterval(expandInterval);
        } else {
            btnArrow.style.width = arrowWidth - (expandAmount * i) + 'px';
            i++;
        }
    }, intervalDelay);
}

ctaBtns.forEach((btn, i) => {
    btn.addEventListener('mouseenter', () => {
        let btnArrow = btn.querySelector('.cta-btn-arrow-container');
        expandBtnArrow(btnArrow, btn);
    });

    btn.addEventListener('mouseleave', () => {
        let btnArrow = btn.querySelector('.cta-btn-arrow-container');
        collapseBtnArrow(btnArrow, btn);
    });
});