import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = {
        'en': 'English',
        'ar': 'العربية'
    }
