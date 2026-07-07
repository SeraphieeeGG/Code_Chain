"""
User model for authentication and authorization.
"""
from datetime import datetime
from flask_login import UserMixin
from models import db, bcrypt


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'

    user_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(80),  nullable=False, unique=True)
    email         = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20),  nullable=False, default='staff')
    is_active     = db.Column(db.Boolean, nullable=False, default=True)
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Flask-Login requires get_id() to return a string
    def get_id(self):
        return str(self.user_id)

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------
    def set_password(self, plain_password):
        """Hash and store the password."""
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        """Return True if the password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, plain_password)

    # ------------------------------------------------------------------
    # Role helpers
    # ------------------------------------------------------------------
    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_manager(self):
        return self.role in ('admin', 'manager')

    # ------------------------------------------------------------------
    def __repr__(self):
        return f'<User {self.user_id}: {self.username} ({self.role})>'

    def to_dict(self):
        return {
            'user_id':    self.user_id,
            'username':   self.username,
            'email':      self.email,
            'role':       self.role,
            'is_active':  self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
