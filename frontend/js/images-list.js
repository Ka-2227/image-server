async function loadImages() {
    try {
        const response = await fetch('/api/images');
        const images = await response.json();

        const container = document.querySelector('.images');

        container.innerHTML = '';

        images.forEach(img => {
            const el = document.createElement('img');
            el.src = `/uploads/${img.filename}`;
            el.style.width = '200px';
            el.style.margin = '10px';

            container.appendChild(el);
        });

    } catch (error) {
        console.error('Ошибка загрузки изображений:', error);
    }
}

loadImages();