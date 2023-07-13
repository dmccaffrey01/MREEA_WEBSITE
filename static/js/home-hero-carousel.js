const swipeLeft = document.querySelector(".swipe-left");
const swipeRight = document.querySelector(".swipe-right");

const carouselItems = document.querySelectorAll(".carousel-item");

const carouselDots = document.querySelectorAll(".carousel-dot");

const numberOfDots = carouselDots.length;

let userMoved = false;

const moveCarousel = (index) => {
    carouselItems.forEach((item, i) => {
        let num = (numberOfDots - 1)
        let percent = (num * 100) - (((num - i) + index) * 100);
        item.style.transform = `translateX(${percent}%)`;
    })
}

const changeActiveDot = (index) => {
    let dot = carouselDots[index];
    
    for (let i = 0; i < numberOfDots; i++) {
        carouselDots[i].classList.remove("active");
    }

    dot.classList.add("active");
}

carouselDots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
        
        changeActiveDot(index);
        moveCarousel(index);
        userMoved = true;
    })
});

const getIndexOfDot = () => {
    let result;
    carouselDots.forEach((dot, index) => {
        if (dot.classList.contains("active")) {
            result = index;
        }
    });
    return result;
}

swipeLeft.addEventListener("click", () => {
    let dotIndex = getIndexOfDot();
    if (dotIndex === 0) {
        dotIndex = numberOfDots;
    }
    changeActiveDot(dotIndex - 1);
    moveCarousel(dotIndex - 1);
    userMoved = true;
})

swipeRight.addEventListener("click", () => {
    let dotIndex = getIndexOfDot();
    if (dotIndex === numberOfDots - 1) {
        dotIndex = -1;
    }
    changeActiveDot(dotIndex + 1);
    moveCarousel(dotIndex + 1);
    userMoved = true;
})

window.addEventListener("load", () => {
    let changeCarousel = window.setInterval(() => {
        if (userMoved) {
            clearInterval(changeCarousel);
        } else {
            let dotIndex = getIndexOfDot();
            if (dotIndex === numberOfDots - 1) {
                dotIndex = -1;
            }
            changeActiveDot(dotIndex + 1);
            moveCarousel(dotIndex + 1);
        }
    }, 7500);
});



