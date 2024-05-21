document.addEventListener("DOMContentLoaded", () => {
    let imageNotMoved = true;
    let imageNotScaled = true;
    
    let dropZone = document.querySelector(".drop-zone");
    let dropZoneText = document.querySelector(".drop-zone-text");
    let imageInput = document.querySelector("#image_file");

    let cropImgContainer = document.querySelector(".crop-img-container");
    let containerRect = cropImgContainer.getBoundingClientRect();

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
    
    let getCropUrl = (img) => {
        let imgRect = img.getBoundingClientRect();

        let x = imgRect.left - containerRect.left;
        let y = imgRect.top - containerRect.top;
        let width = containerRect.width;
        let height = containerRect.height;

        let canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        let ctx = canvas.getContext('2d');
        ctx.drawImage(img, x, y, imgRect.width, imgRect.height);

        let croppedImageUrl = canvas.toDataURL();

        return croppedImageUrl;
    }

    imageInput.addEventListener("change", (e) => {

        let cropContainer = document.querySelector(".crop-container");

        if (cropContainer.classList.contains("hide")) {
            cropContainer.classList.remove("hide");
        }

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
        let profileContainer = document.querySelector(".personal-img-container");
        let profileImg = profileContainer.querySelector("img");
        let newImage = document.createElement("img");
        newImage.classList.add("img-100a");

        let cropImg = document.querySelector(".crop-img");

        let profileImageUrl = getCropUrl(cropImg);

        newImage.src = profileImageUrl;

        newImage.onload = () => {
            profileContainer.removeChild(profileImg);
            profileContainer.appendChild(newImage);
        };
    });

    let saveBtn = document.querySelector(".save-btn");

    saveBtn.addEventListener("click", (e) => {
        e.preventDefault();

        let profileInput = document.querySelector(".profile_picture");

        let cropImg = document.querySelector(".crop-img");

        let profileImageUrl = getCropUrl(cropImg);
        let file = urlToFile(profileImageUrl);

        let fileList = new DataTransfer();
        fileList.items.add(file);

        profileInput.files = fileList.files;

        let form = document.querySelector(".form");

        form.submit();
    });

    let isDragging = false;
    let isScrolling = false;
    let startX = 0;
    let startY = 0;
    let imgX = 0;
    let imgY = 0;
    let minMoveX = 0;
    let minMoveY = 0;
    let maxMoveX = 0;
    let maxMoveY = 0;
    let newImgX = 0;
    let newImgY = 0;

    let scale = 1;
    let newScale;
    let minScale = 1;
    let maxScale = 2;
    let imgWidth = 0;
    let imgHeight = 0;

    cropImgContainer.addEventListener("mousedown", (e) => {
        e.preventDefault();
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        imgX = newImgX;
        imgY = newImgY;
    });

    document.addEventListener("mouseup", (e) => {
        e.preventDefault();
        isDragging = false;
        imgX = newImgX;
        imgY = newImgY;
    });

    let moveImg = (img, imgRect, newX, newY) => {
        minMoveX = 0;
        maxMoveX = -(imgRect.width - containerRect.width);
        minMoveY = 0;
        maxMoveY = -(imgRect.height - containerRect.height);

        let offsetX = newX - startX;
        let offsetY = newY - startY;

        newImgX = imgX + offsetX;
        newImgY = imgY + offsetY;
        
        if (newImgX > minMoveX) {
            newImgX = minMoveX;
        }

        if (newImgY > minMoveY) {
            newImgY = minMoveY;
        }

        if (newImgX < maxMoveX) {
            newImgX = maxMoveX;
        }

        if (newImgY < maxMoveY) {
            newImgY = maxMoveY;
        }

        newImgX = Math.round(newImgX)
        newImgY = Math.round(newImgY)

        img.style.left = `${newImgX}px`;
        img.style.top = `${newImgY}px`;
    }

    document.addEventListener("mousemove", (e) => {

        if (isDragging) {
            let img = cropImgContainer.querySelector(".crop-img");
            let imgRect = img.getBoundingClientRect();

            if (imageNotMoved) {
                imgX = 0;
                imgY = 0;
                imageNotMoved = false;
            }

            let newX = e.clientX;
            let newY = e.clientY;

            moveImg(img, imgRect, newX, newY);
        }
    });

    cropImgContainer.addEventListener("wheel", (e) => {
        e.preventDefault();
        if (!isScrolling) {
            isScrolling = true;

            let img = cropImgContainer.querySelector(".crop-img");
            let imgRect = img.getBoundingClientRect();
    
            if (imageNotScaled) {
                scale = 1;
                imageNotScaled = false;
                imageNotMoved = false;
                
                imgWidth = imgRect.width;
                imgHeight = imgRect.height;
            }
    
            let delta = e.deltaY;
            
            let maxOrMinReached = false;
    
            if (delta < 0) {
    
                newScale = scale + 0.04;
                if (newScale > maxScale) {
                    newScale = maxScale;
                    maxOrMinReached = true;
                }
            } else {
                newScale = scale - 0.04;
                if (newScale < minScale) {
                    newScale = minScale;
                    maxOrMinReached = true;
                }
            }
    
            scale = newScale;

            let oldImgWidth = imgRect.width;
            let oldImgHeight = imgRect.height;
    
            let newImgWidth = imgWidth * scale;
            let newImgHeight = imgHeight * scale;
    
            img.style.width = `${newImgWidth}px`;
            img.style.height = `${newImgHeight}px`;
    
            startX = 0;
            startY = 0;
    
            let newX = -(newImgWidth - oldImgWidth) / 2;
            let newY = -(newImgHeight - oldImgHeight) / 2;

            let newImgRect = img.getBoundingClientRect();

            if (maxOrMinReached) {
                isScrolling = false;
                return;
            }
    
            moveImg(img, newImgRect, newX, newY);

            imgX = newImgX;
            imgY = newImgY;
            isScrolling = false;
        }
    });
});
