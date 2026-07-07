"""
Routes for report generation and export.
"""
from flask import Blueprint, render_template, make_response, request
from flask_login import login_required
from services.report_service import ReportService

report_bp = Blueprint('reports', __name__, url_prefix='/reports')


@report_bp.route('/')
@login_required
def index():
    """Report generation page."""
    return render_template('reports/index.html')


@report_bp.route('/inventory/csv')
@login_required
def inventory_csv():
    """Generate and download inventory report as CSV."""
    csv_content = ReportService.generate_inventory_csv()
    
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=inventory_report.csv'
    
    return response


@report_bp.route('/expiring/csv')
@login_required
def expiring_csv():
    """Generate and download expiring products report as CSV."""
    days = int(request.args.get('days', 7))
    csv_content = ReportService.generate_expiring_products_csv(days)
    
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=expiring_products_{days}days.csv'
    
    return response


@report_bp.route('/violations/csv')
@login_required
def violations_csv():
    """Generate and download temperature violations report as CSV."""
    days = int(request.args.get('days', 30))
    csv_content = ReportService.generate_temperature_violations_csv(days)
    
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=temperature_violations_{days}days.csv'
    
    return response
