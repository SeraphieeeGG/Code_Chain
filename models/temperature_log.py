"""
TemperatureLog model for recording temperature checks.
"""
from datetime import datetime
from models import db


class TemperatureLog(db.Model):
    """Temperature log model for tracking temperature inspections."""
    
    __tablename__ = 'temperature_logs'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)  # Recorded temperature in Celsius
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employee_name = db.Column(db.String(100), nullable=False)
    days_deducted = db.Column(db.Float, default=0.0)  # Days deducted due to temperature violation
    
    def __repr__(self):
        return f'<TemperatureLog {self.log_id}: Batch {self.batch_id} @ {self.temperature}°C>'
    
    def to_dict(self):
        """Convert temperature log to dictionary."""
        return {
            'log_id': self.log_id,
            'batch_id': self.batch_id,
            'temperature': self.temperature,
            'recorded_at': self.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'employee_name': self.employee_name,
            'days_deducted': self.days_deducted
        }
    
    @staticmethod
    def get_logs_by_batch(batch_id):
        """Get all temperature logs for a specific batch."""
        return TemperatureLog.query.filter_by(batch_id=batch_id).order_by(
            TemperatureLog.recorded_at.desc()
        ).all()
    
    @staticmethod
    def get_recent_violations(days=7):
        """Get recent temperature violations within specified days."""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return TemperatureLog.query.filter(
            TemperatureLog.days_deducted > 0,
            TemperatureLog.recorded_at >= cutoff_date
        ).order_by(TemperatureLog.recorded_at.desc()).all()
