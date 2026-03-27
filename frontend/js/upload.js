const input = document.querySelector('input[type="file"]');
const button = document.querySelector('.send_file button');

button.addEventListener('click', async () => {
    if (!input.files.length) {
        alert('Выберите файл');
        return;
    }

    const formData = new FormData();
    formData.append('file', input.files[0]);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Ошибка загрузки');
        }

        const data = await response.json();
        console.log('Загружено:', data);

        alert('Файл успешно загружен');

    } catch (error) {
        console.error(error);
        alert('Ошибка при загрузке');
    }
});