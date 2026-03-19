from config import Config
from models import Image
from utils import (
    is_allowed_extension, format_file_size, get_file_extension,
    save_file, delete_file, log_error, log_success
)
from database import Database
from flask import jsonify, request
from werkzeug.utils import secure_filename

def register_routes(app):
    @app.route('/')
    def index():
        return "API работает. Фронтенд обслуживается через Nginx."

    # ←←← НОВЫЙ МАРШРУТ ДЛЯ ПРОВЕРКИ
    @app.route('/api/')
    def api_root():
        return jsonify({
            'status': 'ok',
            'message': 'Image Hosting API работает ✅',
            'version': '1.0',
            'endpoints': {
                'upload': '/api/upload (POST)',
                'delete': '/api/delete/<id> (GET)',
                'frontend': 'http://localhost:8080/upload_form.html'
            }
        })

    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'Файл не выбран'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': "Файл не выбран"}), 400
        
        if not is_allowed_extension(file.filename):
            return jsonify({'error': "Неподдерживаемый формат файла"}), 400
        
        try:
            file_data = file.read()
            file_size = len(file_data)
            if file_size > Config.MAX_CONTENT_LENGTH:
                return jsonify({'error': f"Файл слишком большой. Максимум {format_file_size(Config.MAX_CONTENT_LENGTH)}"}), 400
            
            success, new_filename = save_file(file.filename, file_data)
            if not success:
                return jsonify({'error': f"Ошибка сохранения: {new_filename}"}), 500
            
            file_type = get_file_extension(file.filename).replace('.', '')
            image = Image(
                filename=new_filename,
                original_name=secure_filename(file.filename),
                size=file_size,
                file_type=file_type
            )
            success_db, image_id = Database.save_image(image)
            if not success_db:
                delete_file(new_filename)
                return jsonify({'error': "Ошибка сохранения в БД"}), 500
            
            log_success(f'Изображение сохранено {new_filename}')
            return jsonify({
                'success': True,
                'message': "Файл успешно загружен",
                'image': {
                    'id': image_id,
                    'filename': new_filename,
                    'original_name': file.filename,
                    'size': format_file_size(file_size),
                    'url': f"/images/{new_filename}",
                    'delete_url': f'/api/delete/{image_id}'
                }
            }), 201
        except Exception as e:
            log_error(f'Ошибка загрузки файла: {e}')
            return jsonify({'error': str(e)}), 500

    @app.route('/api/delete/<int:image_id>')
    def delete_image(image_id):
        success_db, filename = Database.delete_image(image_id)
        if not success_db or not filename:
            return jsonify({'error': 'Изображение не найдено'}), 404
        
        if delete_file(filename):
            log_success(f'Файл удалён с диска: {filename}')
            return jsonify({'success': True, 'message': 'Изображение полностью удалено'}), 200
        else:
            return jsonify({'error': 'Ошибка удаления файла с диска'}), 500