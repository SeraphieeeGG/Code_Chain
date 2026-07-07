"""
Database models for the Cold-Chain Expiry Accelerator.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db     = SQLAlchemy()
bcrypt = Bcrypt()

# Import models to make them available when importing from models
from models.user            import User
from models.product         import Product
from models.batch           import Batch
from models.temperature_log import TemperatureLog

__all__ = ['db', 'bcrypt', 'User', 'Product', 'Batch', 'TemperatureLog']
