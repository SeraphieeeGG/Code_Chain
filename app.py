"""
Cold-Chain Expiry Accelerator - Main Application
"""
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, bcrypt
from models.user import User
from routes import auth_bp, product_bp, batch_bp, temperature_bp, dashboard_bp, report_bp, delivery_bp
from config import config
import os


def create_app(config_name='default'):
    """
    Application factory function.

    Args:
        config_name (str): Configuration name (development, production, default)

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # ── Flask-Login setup ──────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'          # redirect here when @login_required fails
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ── Blueprints ─────────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(batch_bp)
    app.register_blueprint(temperature_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(delivery_bp)

    # ── Template filters ───────────────────────────────────────────────
    @app.template_filter('date')
    def date_filter(value, format='%Y-%m-%d'):
        """Format a date string or return today's date if value is 'now'."""
        from datetime import date
        if value == 'now':
            return date.today().strftime(format)
        if value:
            return value.strftime(format)
        return ''

    @app.template_filter('status_color')
    def status_color(status):
        """Return Bootstrap color class for status."""
        colors = {
            'Safe':     'success',
            'Warning':  'warning',
            'Critical': 'danger',
            'Expired':  'secondary',
        }
        return colors.get(status, 'secondary')

    @app.template_filter('format_date')
    def format_date(date):
        """Format date for display."""
        if date:
            return date.strftime('%Y-%m-%d')
        return 'N/A'

    @app.template_filter('format_datetime')
    def format_datetime(dt):
        """Format datetime for display."""
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return 'N/A'

    return app


if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(debug=True, host='0.0.0.0', port=5000)
