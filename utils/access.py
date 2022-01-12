from functools import wraps
from flask import flash, redirect, url_for, session


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('authentication.login'))
    return wrap


# Check if user has full access
def is_full_access(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['access'] > 0:
                return f(*args, **kwargs)
            else:
                flash('No access for this action', 'danger')
                return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('authentication.login'))
    return wrap
