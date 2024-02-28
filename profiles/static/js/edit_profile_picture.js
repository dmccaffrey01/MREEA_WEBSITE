let urlToFile = (url) => {

    let arr = url.split(",")
    let mime = arr[0].match(/:(.*?);/)[1]
    let data = arr[1]

    let dataStr = atob(data)
    let n = dataStr.length
    let dataArr = new Uint8Array(n)

    while(n--)
    {
        dataArr[n] = dataStr.charCodeAt(n)
    }

    let section = document.querySelector(".profile-section");

    let username = section.getAttribute("data-username");

    let file  = new File([dataArr], `${username}_profile_picture.jpg`, {type: mime})

    return file
}

let imageNotMoved = true;
let imageNotScaled = true;

document.addEventListener("DOMContentLoaded", () => {
    let dropZone = document.querySelector(".drop-zone");
    let dropZoneText = document.querySelector(".drop-zone-text");
    let imageInput = document.querySelector("#image_file");

    let cropImgContainer = document.querySelector(".crop-img-container");
    let containerRect = cropImgContainer.getBoundingClientRect();

    let profileImageUrl;

    imageInput.addEventListener("change", (e) => {
        imageNotMoved = true;
        imageNotScaled = true;
        
        let imageFile = e.target.files[0];

        dropZoneText.textContent = imageFile.name;

        let reader = new FileReader();
        reader.readAsDataURL(imageFile);

        reader.onload = (e) => {
            let imageUrl = e.target.result;
            let image = document.createElement("img");
            image.src = imageUrl;

            image.onload = (e) => {
                let canvas = document.createElement("canvas");

                let imageWidth = e.target.width;
                let imageHeight = e.target.height;
                let ratio;

                if (imageWidth < imageHeight) {
                    canvas.width = containerRect.width;
                    ratio = canvas.width / imageWidth;
                    canvas.height = imageHeight * ratio;
                } else {
                    canvas.height = containerRect.height;
                    ratio = canvas.height / imageHeight;
                    canvas.width = imageWidth * ratio;
                }

                const context = canvas.getContext("2d");
                context.drawImage(image, 0, 0, canvas.width, canvas.height);

                let newImageUrl = context.canvas.toDataURL("image/jpeg", 90);

                profileImageUrl = newImageUrl;

                let newImage = document.createElement("img");
                newImage.src = newImageUrl;
                newImage.classList.add("crop-img");

                let oldImage = cropImgContainer.querySelector(".crop-img");

                cropImgContainer.removeChild(oldImage);
                cropImgContainer.appendChild(newImage);
            }
        }

    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        imageInput.files = e.dataTransfer.files;

        const changeEvent = new Event('change');
        imageInput.dispatchEvent(changeEvent);
    });

    let previewBtn = document.querySelector(".preview-btn");

    previewBtn.addEventListener("click", () => {
        let profileContainer = document.querySelector(".preview-img-container");
        let profileImg = profileContainer.querySelector("img");
        let newImage = document.createElement("img");
        newImage.classList.add("img-100a");

        if (profileImageUrl) {
            newImage.src = profileImageUrl;

            newImage.onload = () => {
                profileContainer.removeChild(profileImg);
                profileContainer.appendChild(newImage);
            };
        } else {
            return;
        }

    });

    let saveBtn = document.querySelector(".save-btn");

    saveBtn.addEventListener("click", (e) => {
        e.preventDefault();

        let profileInput = document.querySelector(".profile_picture");

        if (profileImageUrl) {
            let file = urlToFile(profileImageUrl);

            profileInput.value = file;
        }

        let form = document.querySelector(".form");

        form.submit();
    });

});

document.addEventListener("DOMContentLoaded", () => {
    let cropImgContainer = document.querySelector(".crop-img-container");
    let containerRect = cropImgContainer.getBoundingClientRect();

    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let newTranslateX = 0;
    let newTranslateY = 0;
    let translateX = 0;
    let translateY = 0;
    let minTranslateX = 0;
    let maxTranslateX = 0;
    let minTranslateY = 0;
    let maxTranslateY = 0;
    let scale = 1;
    let newScale;
    let minScale = 1;
    let maxScale = 2;

    cropImgContainer.addEventListener("mousedown", (e) => {
        e.preventDefault();
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
    });

    document.addEventListener("mouseup", (e) => {
        e.preventDefault();
        isDragging = false;
        translateX = newTranslateX;
        translateY = newTranslateY;
    });

    document.addEventListener("mousemove", (e) => {

        if (isDragging) {
            let img = cropImgContainer.querySelector(".crop-img");
            let imgRect = img.getBoundingClientRect();

            if (imageNotMoved) {
                translateX = (-imgRect.width / 2);
                translateY = (-imgRect.height / 2);
                minTranslateX = (-containerRect.width / 2);
                maxTranslateX = (-imgRect.width - minTranslateX);
                minTranslateY = (-containerRect.height / 2);
                maxTranslateY = (-imgRect.height - minTranslateY);
                imageNotMoved = false;
            }

            let offsetX = e.clientX - startX;
            let offsetY = e.clientY - startY;

            newTranslateX = translateX + offsetX;
            newTranslateY = translateY + offsetY;

            if (newTranslateX > minTranslateX) {
                newTranslateX = minTranslateX;
            }

            if (newTranslateY > minTranslateY) {
                newTranslateY = minTranslateY;
            }

            if (newTranslateX < maxTranslateX) {
                newTranslateX = maxTranslateX;
            }

            if (newTranslateY < maxTranslateY) {
                newTranslateY = maxTranslateY;
            }

            img.style.translate = `${newTranslateX}px ${newTranslateY}px`;
        }
    });

    cropImgContainer.addEventListener("wheel", (e) => {
        let img = cropImgContainer.querySelector(".crop-img");
        let imgRect = img.getBoundingClientRect();

        if (imageNotScaled) {
            scale = 1;
            imageNotScaled = false;
            
            imgWidth = imgRect.width;
            imgHeight = imgRect.height;
        }

        let delta = e.deltaY;

        if (delta < 0) {
            newScale = scale + 0.05;
            if (newScale > maxScale) {
                newScale = maxScale;
            }
            scale = newScale;
        } else {
            newScale = scale - 0.05;
            if (newScale < minScale) {
                newScale = minScale;
            }
            scale = newScale;
        }

        img.style.width = `${imgWidth * scale}px`;
        img.style.height = `${imgHeight * scale}px`;

    });

});