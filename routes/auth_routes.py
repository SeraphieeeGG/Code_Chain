"""
Authentication routes: register, login, logout.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ------------------------------------------------------------------
# Register
# ------------------------------------------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username  = request.form.get('username',  '').strip()
        email     = request.form.get('email',     '').strip().lower()
        password  = request.form.get('password',  '')
        password2 = request.form.get('password2', '')
        role      = request.form.get('role', 'staff')

        # Basic validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != password2:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('auth/register.html')

        if role not in ('admin', 'manager', 'staff'):
            role = 'staff'

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(username=username).first()

        if user and user.is_active and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))

        flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')


# ------------------------------------------------------------------
# Logout
# ------------------------------------------------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
