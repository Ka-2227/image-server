const image1 = document.getElementById('image1');
let index = 0;
let images = [];

function changeImage() {
    if (images.length === 0) return;
    image1.style.opacity = 0;
    setTimeout(() => {
        image1.src = images[index];
        image1.style.opacity = 1;
        index = (index + 1) % images.length;
    }, 800);
}

function startSlideShow() {
    if (images.length === 0) {
        return;
    }
    changeImage();
    setInterval(changeImage, 5000);
}


function loadImages() {
    fetch('images.json')
        .then(response => response.json())
        .then(data => {
            images = data;
            startSlideShow();
        })
        .catch(() => startSlideShow());
}

loadImages();