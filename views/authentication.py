from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from models.db import db, User
from utils.access import is_logged_in
from models import forms
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError


authentication_view = Blueprint("authentication", __name__, static_folder="static", template_folder="template")


# Index
@authentication_view.route('/')
def index():
    db.create_all()
    return render_template('home.html')


# Register
@authentication_view.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        users = User.query.all()
        # if there is no users is database, first user gets full access
        # otherwise only reading access
        if users:
            access = 0
        else:
            access = 1
        try:
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.encrypt(str(form.password.data))

            user = User(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        access=access
                        )
            db.session.add(user)
            db.session.commit()

            flash(f'{first_name} registered successfully', 'success')

            return redirect(url_for('authentication.login'))
        except IntegrityError:
            flash(f'Email address {form.email.data} already exists. Try to login, or use another address.', 'danger')
    return render_template('register.html', form=form)


# Login
@authentication_view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # Get password from database
        user = User.query.filter_by(email=email).first()

        # if user has been found in database
        if user:
            password = user.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                session['first_name'] = user.first_name
                session['access'] = user.access
                flash(f'{user.first_name}, logged in', 'success')
                return redirect(url_for('dashboard.dashboard'))

            else:
                error = f'Invalid password for {user.email}'
                return render_template('login.html', error=error)

        # if user has not been found in database
        else:
            error = f'User {user.email} not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout
@authentication_view.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('authentication.login'))
