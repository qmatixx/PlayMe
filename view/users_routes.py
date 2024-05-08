from flask import Blueprint
from flask_login import (current_user, login_required,
                         login_user, logout_user)
from model.models import User, SpotiClient
from model.queries import get_spoti_client
from flask import render_template, url_for, flash, redirect, request
from controller.users_forms import (RegistrationForm,
                                    LoginForm,
                                    UpdateAccountForm)
from app import bcrypt
from controller import db_handler

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register(*args):
    if current_user.is_authenticated:
        flash('You are already logged in', category="info")
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = (
            bcrypt.generate_password_hash(form.password.data)
            .decode('utf-8')
        )
        db_handler.add_user(username=form.username.data, password=hashed_pw)
        flash('Your account has been created. Please log in.', category="success")
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, css_path='static\\css\\main_page.css')


@users.route('/login', methods=['GET', 'POST'])
def login(*args):
    if current_user.is_authenticated:
        flash('You are already logged in', category="info")
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user and bcrypt.check_password_hash(user.password,
                                                form.password.data)):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are now logged in', category="success")
            return (
                redirect(url_for('users.account'))
            )
        flash('Login unsuccessful. Please check email and password', category="danger")
    return render_template('login.html', title='Login', form=form, css_path='static\\css\\main_page.css')


@users.route('/logout')
def logout(*args):
    logout_user()
    flash('You are now logged out', category="info")
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account(*args):
    form = UpdateAccountForm()
    spoti_client = get_spoti_client(current_user.id)
    if form.validate_on_submit():
        db_handler.update_spoti_client(spoti_client, client_id=form.client_id.data, client_secret=form.client_secret.data,
                                       client_name=form.client_name.data, user_id=current_user.id)
    
        flash('Your account has been updated', category="success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.client_id.data = spoti_client.client_id if spoti_client else ''
        form.client_secret.data = spoti_client.client_secret if spoti_client else ''
        form.client_name.data = spoti_client.client_name if spoti_client else ''

    return render_template(
        'account.html',
        form=form,
        css_path='static\\css\\main_page.css'
        )