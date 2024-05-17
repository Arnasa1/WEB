from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from forms import SignUpForm, SignInForm, TaskForm
from models.models import User, UserRequest
from Web import db, cache
from datetime import datetime
from functools import wraps
from flask_caching import Cache

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

@routes.route('/main', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=60)
def main():
    user_id = request.cookies.get('user_id')
    requests = UserRequest.query.filter_by(user_id=user_id).all()
    form = TaskForm()
    if form.validate_on_submit():
        task = UserRequest(task_name=form.task_name.data, task_desc=form.task_desc.data, user_id=request.cookies.get('user_id'))
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        cache.clear()
    return render_template('main.html', requests=requests, form=form)

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
    cache.clear()
    return response

@routes.route('/add_task', methods=['POST', 'GET'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = UserRequest(task_name=form.task_name.data, task_desc=form.task_desc.data, user_id=request.cookies.get('user_id'))
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('routes.main'))
    return redirect(url_for('routes.main'))

@routes.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = UserRequest.query.get(task_id)
    if task:
        task.end_date = datetime.now()
        db.session.commit()
        flash('Task completed successfully!', 'success')
    return redirect(url_for('routes.main'))

@routes.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = UserRequest.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.task_name = form.task_name.data
        task.task_desc = form.task_desc.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('routes.main'))
    return render_template('edit_task.html', form=form, task=task)

@routes.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = UserRequest.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('routes.main'))