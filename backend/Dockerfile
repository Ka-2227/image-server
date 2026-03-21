FROM python:3.12-slim

WORKDIR /app

# Сначала только requirements (для кэширования)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь весь код
COPY . .

EXPOSE 8000

CMD ["python", "app.py"]