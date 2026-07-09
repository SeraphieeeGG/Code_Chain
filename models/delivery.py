"""
Delivery model for tracking batch deliveries.
"""
from models import db
from datetime import datetime


class Delivery(db.Model):
    """Delivery model for storing delivery information."""
    
    __tablename__ = 'deliveries'
    
    delivery_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id', ondelete='CASCADE'), nullable=False)
    destination = db.Column(db.String(500), nullable=False)
    delivery_status = db.Column(db.String(50), nullable=False, default='Pending')
    delivery_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Relationship with batch
    batch = db.relationship('Batch', backref='deliveries')
    
    def __repr__(self):
        return f'<Delivery {self.delivery_id}: Batch {self.batch_id} to {self.destination}>'
    
    def to_dict(self):
        """Convert delivery to dictionary."""
        return {
            'delivery_id': self.delivery_id,
            'batch_id': self.batch_id,
            'destination': self.destination,
            'delivery_status': self.delivery_status,
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d %H:%M:%S') if self.delivery_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def get_by_batch(cls, batch_id):
        """Get all deliveries for a batch."""
        return cls.query.filter_by(batch_id=batch_id).all()
    
    @classmethod
    def get_by_status(cls, status):
        """Get all deliveries by status."""
        return cls.query.filter_by(delivery_status=status).all()
