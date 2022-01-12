from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from models.db import db, User
from utils.access import is_logged_in, is_full_access
from models import forms
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError
from psycopg2 import connect
from models.config import config
import uuid
from datetime import datetime


dashboard_view = Blueprint("dashboard", __name__, static_folder="static", template_folder="template")


# Dashboard
@dashboard_view.route('/')
@is_logged_in
def dashboard():
    # list all registered users
    users = User.query.all()
    return render_template('dashboard.html', users=users)


# Add Account
@dashboard_view.route('/add_account', methods=['GET', 'POST'])
@is_full_access
def add_account():
    form = forms.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            idx = uuid.uuid4()
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.encrypt(str(form.password.data))
            access = 0
            register_date = datetime.utcnow()

            params = config()
            connection = connect(**params)
            cursor = connection.cursor()
            cursor.execute("""
                        INSERT INTO user_data (id, email, first_name, last_name, password, access, register_date) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s)
                        """, (idx, email, first_name, last_name, password, access, register_date))

            connection.commit()
            flash(f'{first_name} registered successfully', 'success')
            return redirect(url_for('dashboard.dashboard'))

        except IntegrityError:
            flash(f'Email address {form.email.data} already exists. Try to use another address.', 'danger')

    return render_template('register.html', form=form)


# Edit Account
@dashboard_view.route('/edit_account/<uuid:user_id>', methods=['GET', 'POST'])
@is_full_access
def edit_account(user_id):
    # fill up form
    user = User.query.filter_by(id=user_id).first()
    form = forms.RegisterForm(request.form)
    form.email.data = user.email
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name

    # edit account
    if request.method == 'POST' and form.validate():
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.password = request.form['password']
        user.confirm = request.form['confirm']

        # save changes to database
        db.session.commit()

        flash('Account Updated', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('edit_account.html', form=form)


# Delete Account
@dashboard_view.route('/delete_account/<uuid:user_id>', methods=['GET', 'POST'])
@is_full_access
def delete_account(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    if session['email'] == user.email:
        session['logged_in'] = False
    flash(f'Account {user.first_name} was deleted')
    return redirect(url_for('dashboard.dashboard'))


# Give Access
@dashboard_view.route('/give_access/<uuid:user_id>', methods=['POST'])
@is_full_access
def give_access(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.access = 1
    db.session.commit()
    flash(f'{user.first_name} got full access', 'success')
    return redirect(url_for('dashboard.dashboard'))


# Denied Access
@dashboard_view.route('/denied_access/<uuid:user_id>', methods=['POST'])
@is_full_access
def denied_access(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.access = 0
    db.session.commit()
    flash(f'{user.first_name} has no access', 'success')
    return redirect(url_for('dashboard.dashboard'))
