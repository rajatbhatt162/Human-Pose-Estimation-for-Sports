// Function to handle image upload
document.getElementById('uploadImageBtn').addEventListener('click', function() {
    let imageInput = document.getElementById('imageInput');
    let formData = new FormData();

    if (imageInput.files.length === 0) {
        alert("Please select an image file.");
        return;
    }

    formData.append('image', imageInput.files[0]);

    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            document.getElementById('imageResult').innerHTML = `<img src="${data.image_url}" alt="Processed Image">`;
        } else {
            alert("Error in processing the image.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Function to handle video upload
document.getElementById('uploadVideoBtn').addEventListener('click', function() {
    let videoInput = document.getElementById('videoInput');
    let formData = new FormData();

    if (videoInput.files.length === 0) {
        alert("Please select a video file.");
        return;
    }

    formData.append('video', videoInput.files[0]);

    fetch('/process_video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.video_url) {
            document.getElementById('videoResult').innerHTML = `<video controls><source src="${data.video_url}" type="video/mp4"></video>`;
        } else {
            alert("Error in processing the video.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Function to handle camera stream
document.getElementById('useCameraBtn').addEventListener('click', function() {
    fetch('/process_camera')
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert("Error in accessing the camera.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
