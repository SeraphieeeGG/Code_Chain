"""
Batch model representing product batches with expiration tracking.
"""
from datetime import datetime, timedelta
from models import db


class Batch(db.Model):
    """Batch model for tracking product batches."""
    
    __tablename__ = 'batches'
    
    batch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    manufacturing_date = db.Column(db.Date, nullable=False)
    original_expiry = db.Column(db.Date, nullable=False)
    adjusted_expiry = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Safe')
    
    # Relationship with temperature logs
    temperature_logs = db.relationship('TemperatureLog', backref='batch', lazy=True, 
                                      cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Batch {self.batch_id}: Product {self.product_id}>'
    
    def to_dict(self):
        """Convert batch to dictionary."""
        return {
            'batch_id': self.batch_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else 'N/A',
            'manufacturing_date': self.manufacturing_date.strftime('%Y-%m-%d'),
            'original_expiry': self.original_expiry.strftime('%Y-%m-%d'),
            'adjusted_expiry': self.adjusted_expiry.strftime('%Y-%m-%d'),
            'quantity': self.quantity,
            'status': self.status,
            'days_until_expiry': self.days_until_expiry()
        }
    
    def days_until_expiry(self):
        """Calculate days until adjusted expiration."""
        today = datetime.now().date()
        delta = self.adjusted_expiry - today
        return delta.days
    
    def update_status(self):
        """Update batch status based on days until expiry."""
        from config import Config
        
        days_remaining = self.days_until_expiry()
        
        if days_remaining < 0:
            self.status = 'Expired'
        elif days_remaining <= Config.STATUS_CRITICAL_THRESHOLD:
            self.status = 'Critical'
        elif days_remaining <= Config.STATUS_WARNING_THRESHOLD:
            self.status = 'Warning'
        else:
            self.status = 'Safe'
        
        return self.status
    
    @staticmethod
    def get_batches_by_status(status):
        """Get all batches with a specific status."""
        return Batch.query.filter_by(status=status).all()
    
    @staticmethod
    def get_expiring_soon(days=7):
        """Get batches expiring within specified days."""
        today = datetime.now().date()
        target_date = today + timedelta(days=days)
        return Batch.query.filter(
            Batch.adjusted_expiry >= today,
            Batch.adjusted_expiry <= target_date
        ).order_by(Batch.adjusted_expiry).all()
    
    @staticmethod
    def get_expired():
        """Get all expired batches."""
        today = datetime.now().date()
        return Batch.query.filter(Batch.adjusted_expiry < today).all()
