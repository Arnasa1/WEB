from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from forms import SignUpForm, SignInForm
from models.models import User
from Web import db
from functools import wraps

routes = Blueprint('routes', __name__)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = request.cookies.get('user_id')
        if user_id is None:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('routes.signin'))
        return view(**kwargs)
    return wrapped_view

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('routes.signin'))
    return render_template('signup.html', form=form)

@routes.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            flash('You have been logged in successfully!', 'success')
            response = make_response(redirect(url_for('routes.main')))
            response.set_cookie('user_id', str(user.id))
            return response
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('signin.html', form=form)

@routes.route('/logout')
def logout():
    response = make_response(redirect(url_for('routes.index')))
    response.set_cookie('user_id', '', expires=0)
    flash('You have been logged out successfully!', 'success')
    return response

@routes.route('/main')
@login_required
def main():
    return render_template('main.html')
