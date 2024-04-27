from flask import Blueprint, flash, render_template, redirect, url_for, session, request
import forms
from models.models import User, UserRequest 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Web import db
import json

routes = Blueprint('routes', __name__)

def get_current_user_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        return None

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@routes.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('signin.html')