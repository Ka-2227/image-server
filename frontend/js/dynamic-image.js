function getLocalImages() {
    const data = localStorage.getItem('uploadedImages');
    return data ? JSON.parse(data) : [];
}

async function getDefaultImages() {
    try {
        const res = await fetch('images.json');
        return await res.json();
    } catch (e) {
        return []; // если json нет — просто пусто
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const img = document.getElementById("image1");

    let images = getLocalImages();

    // Если в localStorage пусто → используем images.json
    if (images.length === 0) {
        const defaults = await getDefaultImages();
        images = defaults.map(d => ({ url: d.url }));
    }

    // Если и там пусто — fallback
    if (images.length === 0) {
        return;
    }

    let index = 0;

    function fadeToNext() {
        const next = images[index];

        const preloader = new Image();
        preloader.src = next.url;

        preloader.onload = () => {
            img.style.opacity = 0;

            setTimeout(() => {
                img.src = next.url;
                img.style.opacity = 1;

                index = (index + 1) % images.length;
            }, 500);
        };
    }

    img.src = images[0].url;
    img.style.opacity = 1;

    setInterval(fadeToNext, 4000);
});