from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from app import db
from app.models import User, Role
from functools import wraps

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if 'user_id' not in session:
                flash('You need to log in first.', 'danger')
                return redirect(url_for('auth.login'))

            # Check if the user has the required role (if specified)
            if role and session.get('role') != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('auth.login'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator



auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if user and user.password_hash == password:  # In a real app, use proper password hashing!
            # Store user information in the session
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role

            role = db.session.query(Role).filter_by(role_id=user.role).first()
            # Redirect based on role
            if role.role_name == 'manager':
                return redirect(url_for('manager.manager_dashboard'))
            elif role.role_name == 'staff':
                return redirect(url_for('staff.staff_dashboard'))
            elif role.role_name == 'supplier':
                return redirect(url_for('supplier.supplier_dashboard'))
            else:
                flash('Invalid role', 'danger')
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))