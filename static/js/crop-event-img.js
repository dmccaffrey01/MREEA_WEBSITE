document.getElementById('imageInput').addEventListener('change', function() {
    const file = this.files[0];
    const maxSizeInBytes = 1024 * 1024 * 10;
    if (file) {
      if (file.size > maxSizeInBytes) {
        alert('The selected image exceeds the maximum allowed size (10MB). Please choose a smaller image.');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = function(event) {
        const img = document.createElement('img');
        img.src = event.target.result;

        // Remove any previously added cropper instances
        if (window.cropper) {
          window.cropper.destroy();
        }

        // Attach the new image to the DOM
        const imageContainer = document.querySelector('.crop-event-img-container');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(img);

        // Initialize Cropper.js
        window.cropper = new Cropper(img, {
          aspectRatio: 16 / 9, // Set to 1 for square cropping
          viewMode: 1,    // Set to 1 to restrict the crop box to the container
          crop(event) {
            // Update the cropped preview image
            const croppedImage = document.getElementById('croppedImage');
          },
        });
      };
      reader.readAsDataURL(file);
    }
  });

const previewBtn = document.querySelector(".preview-btn");
const previewImg = document.querySelector("#previewImage");
const previewContainer = document.querySelector(".preview-event-img-change-container");

const changeEventImgBtn = document.querySelector(".change-event-img-btn");
const eventImgChangeContainer = document.querySelector(".event-image-change-container");
const editEventImgContainer = document.querySelector(".edit-event-img-input-container");

previewBtn.addEventListener("click", () => {
    if (typeof cropper !== "undefined") {
      let croppedImage = cropper.getCroppedCanvas().toDataURL('image/jpeg', 0.7);
      previewImg.src = croppedImage;
    } 
    
    editEventImgContainer.style.display = "none";
    previewContainer.style.display = "flex";

    const croppedImageData = previewImg.src;
    document.getElementById('croppedImageData').value = croppedImageData;
});

changeEventImgBtn.addEventListener("click", () => {
    eventImgChangeContainer.style.display = "flex";
    editEventImgContainer.style.display = "flex";
    previewContainer.style.display = "none";
});

const cancelBtns = document.querySelectorAll(".cancel-btn");

cancelBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        eventImgChangeContainer.style.display = "none";
        editEventImgContainer.style.display = "none";
        document.getElementById('croppedImageData').value = "";
    });
});

const saveEventImgBtn = document.querySelector(".save-crop-btn");

saveEventImgBtn.addEventListener("click", () => {
    eventImgChangeContainer.style.display = "none";
    editEventImgContainer.style.display = "none";
    document.querySelector(".event-form-img-preview").src = document.getElementById('croppedImageData').value;
});
