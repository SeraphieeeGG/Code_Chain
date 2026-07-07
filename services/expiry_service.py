"""
Service for handling expiry calculations and temperature-based adjustments.
"""
from datetime import timedelta
from models import db
from config import Config


class ExpiryService:
    """Service class for expiry-related business logic."""
    
    @staticmethod
    def calculate_penalty_days(temperature_difference):
        """
        Calculate penalty days based on temperature difference.
        
        Args:
            temperature_difference (float): Difference between logged and maximum safe temperature
            
        Returns:
            float: Number of days to deduct from shelf life
        """
        if temperature_difference <= 0:
            return 0.0
        
        penalty_days = temperature_difference * Config.PENALTY_FACTOR
        return penalty_days
    
    @staticmethod
    def adjust_batch_expiry(batch, temperature):
        """
        Adjust batch expiration date based on logged temperature.
        
        Args:
            batch: Batch object to adjust
            temperature (float): Logged temperature
            
        Returns:
            float: Number of days deducted (0 if no violation)
        """
        # Get the product's maximum safe temperature
        max_temp = batch.product.maximum_temperature
        
        # Calculate temperature difference
        temp_difference = temperature - max_temp
        
        # Calculate penalty if temperature exceeds maximum
        days_deducted = 0.0
        if temp_difference > 0:
            days_deducted = ExpiryService.calculate_penalty_days(temp_difference)
            
            # Adjust the expiry date (reduce by penalty days)
            batch.adjusted_expiry = batch.adjusted_expiry - timedelta(days=days_deducted)
            
            # Ensure adjusted expiry doesn't exceed original expiry
            if batch.adjusted_expiry > batch.original_expiry:
                batch.adjusted_expiry = batch.original_expiry
        
        # Update batch status based on new expiry date
        batch.update_status()
        
        # Commit changes to database
        db.session.commit()
        
        return days_deducted
    
    @staticmethod
    def update_all_batch_statuses():
        """
        Update status for all batches based on current date.
        Useful for scheduled tasks.
        """
        from models.batch import Batch
        
        batches = Batch.query.all()
        for batch in batches:
            batch.update_status()
        
        db.session.commit()
        return len(batches)
    
    @staticmethod
    def get_dashboard_stats():
        """
        Get statistics for the dashboard.
        
        Returns:
            dict: Dashboard statistics
        """
        from models.product import Product
        from models.batch import Batch
        
        total_products = Product.query.count()
        total_batches = Batch.query.count()
        
        safe_batches = Batch.query.filter_by(status='Safe').count()
        warning_batches = Batch.query.filter_by(status='Warning').count()
        critical_batches = Batch.query.filter_by(status='Critical').count()
        expired_batches = Batch.query.filter_by(status='Expired').count()
        
        return {
            'total_products': total_products,
            'total_batches': total_batches,
            'safe_batches': safe_batches,
            'warning_batches': warning_batches,
            'critical_batches': critical_batches,
            'expired_batches': expired_batches
        }
