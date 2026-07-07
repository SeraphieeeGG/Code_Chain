"""
Configuration settings for the Cold-Chain Expiry Accelerator application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:password@localhost/cold_chain_db'
    
    # Disable SQLAlchemy modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    ITEMS_PER_PAGE = 20
    
    # Temperature adjustment penalty factor
    # Penalty days = temperature_difference * PENALTY_FACTOR
    PENALTY_FACTOR = 0.5
    
    # Status thresholds (days until expiry)
    STATUS_SAFE_THRESHOLD = 7  # More than 7 days = Safe
    STATUS_WARNING_THRESHOLD = 3  # 3-7 days = Warning
    STATUS_CRITICAL_THRESHOLD = 1  # 1-3 days = Critical
    # Less than 1 day or expired = Expired


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
