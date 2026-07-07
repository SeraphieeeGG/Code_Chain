"""
Routes for dashboard and main views.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from services.expiry_service import ExpiryService
from models.batch import Batch
from models.temperature_log import TemperatureLog

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard view."""
    # Get dashboard statistics
    stats = ExpiryService.get_dashboard_stats()
    
    # Get recent data
    expiring_soon = Batch.get_expiring_soon(7)
    recent_violations = TemperatureLog.get_recent_violations(7)
    critical_batches = Batch.get_batches_by_status('Critical')
    
    return render_template('dashboard/index.html',
                          stats=stats,
                          expiring_soon=expiring_soon[:5],  # Top 5
                          recent_violations=recent_violations[:5],  # Top 5
                          critical_batches=critical_batches[:5])  # Top 5
