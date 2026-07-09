"""
Product model representing temperature-sensitive products.
"""
from models import db


class Product(db.Model):
    """Product model for storing product information."""
    
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    supplier_name = db.Column(db.String(200), nullable=True)
    ideal_temperature = db.Column(db.Float, nullable=False)  # In Celsius
    maximum_temperature = db.Column(db.Float, nullable=False)  # Maximum safe temperature
    shelf_life_days = db.Column(db.Integer, nullable=False)  # Default shelf life in days
    
    # Relationship with batches
    batches = db.relationship('Batch', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.product_name}>'
    
    def to_dict(self):
        """Convert product to dictionary."""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'supplier_name': self.supplier_name,
            'ideal_temperature': self.ideal_temperature,
            'maximum_temperature': self.maximum_temperature,
            'shelf_life_days': self.shelf_life_days
        }
    
    @classmethod
    def get_all_categories(cls):
        """Get all unique categories."""
        categories = db.session.query(cls.category).distinct().all()
        return [cat[0] for cat in categories]
