import psycopg2
from typing import List, Tuple, Optional
from config import Config
from models import Image
from utils import log_info, log_error, log_success
import time

class Database:
    @staticmethod
    def get_connection():
        for i in range(10):
            try:
                conn = psycopg2.connect(Config.DATABASE_URL)
                print("✅ DB connected")
                return conn
            except Exception as e:
                print(f"⏳ DB not ready ({i+1}/10): {e}")
                time.sleep(2)
        raise Exception("❌ Database connection failed")

    @staticmethod
    def init_db():
        conn = Database.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS images(
                        id SERIAL PRIMARY KEY,
                        filename TEXT NOT NULL UNIQUE,
                        original_name TEXT NOT NULL,
                        size INTEGER NOT NULL,
                        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_type TEXT NOT NULL
                    )
                ''')
                conn.commit()
                log_info('База данных инициализирована')
        except Exception as e:
            log_error(f'Error init {e}')
        finally:
            conn.close()

    @staticmethod
    def save_image(image: Image) -> Tuple[bool, Optional[int]]:
        conn = Database.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                INSERT INTO images (filename, original_name, size, file_type)
                VALUES(%s, %s, %s, %s)
                RETURNING id
                ''', (image.filename, image.original_name, image.size, image.file_type))
                image_id = cursor.fetchone()[0]
                conn.commit()
                log_success(f'Изображение сохранено в БД: {image.filename}, ID: {image_id}')
                return True, image_id
        except Exception as e:
            log_error(f'Error save in DB {e}')
            return False, None
        finally:
            conn.close()

    @staticmethod
    def get_images(page: int = 1, per_page: int = 10) -> Tuple[List[Image], int]:
        conn = Database.get_connection()
        try:
            offset = (page - 1) * per_page
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM images ORDER BY upload_time DESC LIMIT %s OFFSET %s', 
                             (per_page, offset))
                rows = cursor.fetchall()
                images = [
                    Image(
                        id=row[0],
                        filename=row[1],
                        original_name=row[2],
                        size=row[3],
                        upload_time=row[4],
                        file_type=row[5]
                    )
                    for row in rows
                ]
                cursor.execute('SELECT COUNT(*) FROM images')
                total = cursor.fetchone()[0]
                return images, total
        except Exception as e:
            log_error(f'Error get images {e}')
            return [], 0
        finally:
            conn.close()

    @staticmethod
    def delete_image(image_id: int) -> Tuple[bool, Optional[str]]:
        conn = Database.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT filename FROM images WHERE id = %s', (image_id,))
                row = cursor.fetchone()
                if not row:
                    return False, None
                
                filename = row[0]
                cursor.execute('DELETE FROM images WHERE id = %s', (image_id,))
                conn.commit()
                log_success(f'Изображение удалено из БД: {filename}')
                return True, filename
        except Exception as e:
            log_error(f'Error delete from DB {e}')
            return False, None
        finally:
            conn.close()