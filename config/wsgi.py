import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv # <-- Імпорт

# Завантажуємо .env
load_dotenv() # <-- Виклик функції

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()