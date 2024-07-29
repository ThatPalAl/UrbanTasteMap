from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = '3f427aa2a7a05ff8b31732804771e7bc'
    GOOGLE_API_KEY = 'AIzaSyADhTVhRtGZHi3FDojp6cZHVtvfBQU-knQ'
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
