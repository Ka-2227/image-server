async function loadImages() {
    try {
        const response = await fetch('/api/images');
        const images = await response.json();

        const container = document.getElementById('images-list');
        const emptyState = document.getElementById('empty-state');

        container.innerHTML = '';

        if (!images.length) {
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';

        images.forEach(img => {
            const row = document.createElement('div');
            row.className = 'image-row';

            row.innerHTML = `
                <div class="image-name">${img.original_name}</div>
                <div class="image-url">
                    <a href="/images/${img.filename}" target="_blank">
                        /images/${img.filename}
                    </a>
                </div>
                <div class="image-delete">
                    <button onclick="deleteImage(${img.id})">Delete</button>
                </div>
            `;

            container.appendChild(row);
        });

    } catch (error) {
        console.error('Ошибка загрузки:', error);
    }
}

async function deleteImage(id) {
    if (!confirm('Удалить изображение?')) return;

    try {
        const response = await fetch(`/api/images/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadImages();
        } else {
            alert('Ошибка удаления');
        }
    } catch (error) {
        console.error(error);
    }
}

loadImages();