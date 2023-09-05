const swipeLeftUpcoming = document.querySelector(".upcoming-swipe-left");
const swipeRightUpcoming = document.querySelector(".upcoming-swipe-right");

const carouselItemsUpcoming = document.querySelectorAll(".upcoming-events-carousel-item");
const carouselContainerUpcoming = document.querySelector(".upcoming-events-carousel-container");
const loadingOverlayUpcoming = document.querySelector(".upcoming-loading-icon-overlay");

const swipeLeftPast = document.querySelector(".past-swipe-left");
const swipeRightPast = document.querySelector(".past-swipe-right");


const carouselItemsPast = document.querySelectorAll(".past-events-carousel-item");
const carouselContainerPast = document.querySelector(".past-events-carousel-container");
const loadingOverlayPast = document.querySelector(".past-loading-icon-overlay");


const findWindowWidth = () => {
    let windowWidth = window.innerWidth;

    if (windowWidth > 1500) {
        return 3;
    } else {
        return 1;
    }
}


const findCurrentItem = (carouselItems) => {
    let currentNum = 0;
    carouselItems.forEach((item, i) => {
        if (item.classList.contains("current")) {
            currentNum = i;
        }
    });
    return currentNum;
}

const checkSwipes = (carouselIems, swipeLeft, swipeRight, windowWidth) => {
    let numOfItems = carouselIems.length;

    if (windowWidth == 3) {
        if (numOfItems == 0 || numOfItems == 1 || numOfItems == 2 || numOfItems == 3) {
            swipeLeft.style.display = "none";
            swipeRight.style.display = "none";
        } else {
            let currentNum = findCurrentItem(carouselIems);
            
            if (currentNum == 0) {
                swipeLeft.style.display = "none";
                swipeRight.style.display = "flex";
            } else if (currentNum == numOfItems - 3) {
                swipeRight.style.display = "none";
                swipeLeft.style.display = "flex";
            } else {
                swipeRight.style.display = "flex";
                swipeLeft.style.display = "flex";
            }
        }
    } else {
        if (numOfItems == 0 || numOfItems == 1) {
            swipeLeft.style.display = "none";
            swipeRight.style.display = "none";
        } else {
            let currentNum = findCurrentItem(carouselIems);
            if (currentNum == 0) {
                swipeLeft.style.display = "none";
                swipeRight.style.display = "flex";
            } else if (currentNum == numOfItems - 1) {
                swipeRight.style.display = "none";
                swipeLeft.style.display = "flex";
            } else {
                swipeRight.style.display = "flex";
                swipeLeft.style.display = "flex";
            }
        }
    }
}

const addClassNextItem = (num, carouselItems) => {
    carouselItems[num].classList.add("current");
}

const removeClassCurrentItem = (num, carouselItems) => {
    carouselItems[num].classList.remove("current");
}

const moveCarouseItems = (move, carouselItems, windowWidth) => {
    
    let n = findCurrentItem(carouselItems);
    let nextItem = n + move;
    if ((nextItem == carouselItems.length - 2) && (carouselItems.length != 2) && (windowWidth == 3) || nextItem < 0 || carouselItems.length == 0) {
        return;
    } else if (carouselItems.length == 1 && windowWidth == 3) {
        carouselItems[0].style.left = "50%";
        carouselItems[0].style.transform = "translate(-50%, -50%)";
    } else if (carouselItems.length == 2 && windowWidth == 3) {
        carouselItems[0].style.left = "33%";
        carouselItems[0].style.transform = "translate(-50%, -50%)";
        carouselItems[1].style.left = "66%";
        carouselItems[1].style.transform = "translate(-50%, -50%)";
    } else {
        addClassNextItem(nextItem, carouselItems);
        removeClassCurrentItem(n, carouselItems);

        n = nextItem;

        if (windowWidth == 3) {
        
            carouselItems.forEach((item, i) => {
                let itemWidth = item.offsetWidth;
                let percent1 = (70 / itemWidth) * 100;
                let percent2 = 100;
                let percent3 = (30 / itemWidth) * 100;

                let diff = i - n;
                
                let x, y, z;

                if (diff < 0) {
                    x = -1;
                    y = -1;
                    z = -1;
                } else if (diff >= 3) {
                    x = 3;
                    y = 3;
                    z = 3;
                } else {
                    x = 1;
                    y = diff;
                    z = diff;
                }

                let translateX = (percent1 * x) + (percent2 * y) + (percent3 * z);

                item.style.transform = `translate(${translateX}%, -50%)`;
            });
        } else {
            carouselItems.forEach((item, i) => {

                let diff = i - n;
                if (diff < 0) {
                    item.style.left = "-110%";
                    item.style.transform = "translate(0%, -50%)";
                } else if (diff > 0) {
                    item.style.left = "110%";
                    item.style.transform = "translate(0%, -50%)";
                } else {
                    item.style.left = "50%";
                    item.style.transform = "translate(-50%, -50%)";
                }
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let windowWidth = findWindowWidth();
    moveCarouseItems(0, carouselItemsUpcoming, windowWidth);
    moveCarouseItems(0, carouselItemsPast, windowWidth);
    checkSwipes(carouselItemsUpcoming, swipeLeftUpcoming, swipeRightUpcoming, windowWidth);
    checkSwipes(carouselItemsPast, swipeLeftPast, swipeRightPast, windowWidth);
    window.setTimeout(() => {
        loadingOverlayUpcoming.style.display = 'none';
        loadingOverlayPast.style.display = 'none';
    }, 1000);
});

swipeRightUpcoming.addEventListener("click", () => {
    let windowWidth = findWindowWidth();
    moveCarouseItems(1, carouselItemsUpcoming, windowWidth);
    checkSwipes(carouselItemsUpcoming, swipeLeftUpcoming, swipeRightUpcoming, windowWidth);
});

swipeLeftUpcoming.addEventListener("click", () => {
    let windowWidth = findWindowWidth();
    moveCarouseItems(-1, carouselItemsUpcoming, windowWidth);
    checkSwipes(carouselItemsUpcoming, swipeLeftUpcoming, swipeRightUpcoming, windowWidth);
});

swipeRightPast.addEventListener("click", () => {
    let windowWidth = findWindowWidth();
    moveCarouseItems(1, carouselItemsPast, windowWidth);
    checkSwipes(carouselItemsPast, swipeLeftPast, swipeRightPast, windowWidth);
});

swipeLeftPast.addEventListener("click", () => {
    let windowWidth = findWindowWidth();
    moveCarouseItems(-1, carouselItemsPast, windowWidth);
    checkSwipes(carouselItemsPast, swipeLeftPast, swipeRightPast, windowWidth);
});




