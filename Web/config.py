import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    WTF_CSRF_ENABLED = True