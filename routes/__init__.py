"""
Route handlers for the Cold-Chain Expiry Accelerator.
"""
from routes.auth_routes        import auth_bp
from routes.product_routes     import product_bp
from routes.batch_routes       import batch_bp
from routes.temperature_routes import temperature_bp
from routes.dashboard_routes   import dashboard_bp
from routes.report_routes      import report_bp
from routes.delivery_routes    import delivery_bp

__all__ = ['auth_bp', 'product_bp', 'batch_bp', 'temperature_bp', 'dashboard_bp', 'report_bp', 'delivery_bp']
