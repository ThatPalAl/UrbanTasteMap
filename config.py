from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = '?'
    GOOGLE_API_KEY = '?-knQ'
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
