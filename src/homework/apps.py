from django.apps import AppConfig
from datetime import datetime

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homework'

def my_great_func():
    # do something
    return datetime.now()