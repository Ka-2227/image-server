const MAX_SIZE = 5 * 1024 * 1024;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
let currentUrl = '';

function showStatus(message, type) {
    const status = document.getElementById('upload-status');
    if (!status) return;
    status.textContent = message;
    status.className = `upload-status ${type}`;
    status.style.display = 'block';
    if (type === 'success') setTimeout(() => status.style.display = 'none', 5000);
}

function validateFile(file) {
    if (!ALLOWED_TYPES.includes(file.type)) {
        showStatus('Only .jpg, .png, .gif allowed', 'error');
        return false;
    }
    if (file.size > MAX_SIZE) {
        showStatus('File too large! Max 5 MB', 'error');
        return false;
    }
    return true;
}

async function handleFile(file) {
    if (!file || !validateFile(file)) return;
    showStatus('Uploading...', 'info');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/api/upload', {   // ←←← ВАЖНО: слеш в начале!
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            currentUrl = result.image.url;
            document.getElementById('current-upload-input').value = currentUrl;
            showStatus('Upload successful!', 'success');
            alert(`✅ Загружено!\nID: ${result.image.id}\nСсылка: ${currentUrl}`);
        } else {
            showStatus(result.error || 'Ошибка сервера', 'error');
        }
    } catch (error) {
        showStatus('Upload failed: ' + error.message, 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area')
    const fileInput = document.getElementById('fileInput')
    const browseBtn = document.querySelector('.send_file button')
    
    const copyBtn = document.getElementById('copy-button')
    if (copyBtn) {
        copyBtn.addEventListener('click', copyUrl);
    }
});

async function copyUrl() {
    if (!currentUrl) return;
    await navigator.clipboard.writeText(currentUrl);
    showStatus('URL copied!', 'success');
}





async function copyUrl() {
    if (!currentUrl) return;
    try {
        await navigator.clipboard.writeText(currentUrl);
        showStatus('URL copied!', 'success');
    } catch {
        showStatus('Failed to copy URL', 'error');
    }
}