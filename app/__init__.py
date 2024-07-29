from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.static_folder = 'static'

from app.celery import make_celery
celery = make_celery(app)

from app import routes
