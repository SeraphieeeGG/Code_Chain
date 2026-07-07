"""
Routes for temperature logging.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from models import db
from models.batch import Batch
from models.temperature_log import TemperatureLog
from services.expiry_service import ExpiryService
from utils.validators import validate_temperature_data

temperature_bp = Blueprint('temperature', __name__, url_prefix='/temperature')


@temperature_bp.route('/log/<int:batch_id>', methods=['GET', 'POST'])
@login_required
def log_temperature(batch_id):
    """Log temperature for a specific batch."""
    batch = Batch.query.get_or_404(batch_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            temp_data = {
                'temperature': request.form.get('temperature'),
                'employee_name': request.form.get('employee_name')
            }
            
            # Validate data
            is_valid, error_message = validate_temperature_data(temp_data)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('temperature/log.html', batch=batch, form_data=temp_data)
            
            temperature = float(temp_data['temperature'])
            
            # Calculate days deducted before adjustment
            max_temp = batch.product.maximum_temperature
            days_deducted = 0.0
            
            if temperature > max_temp:
                temp_difference = temperature - max_temp
                days_deducted = ExpiryService.calculate_penalty_days(temp_difference)
            
            # Create temperature log
            temp_log = TemperatureLog(
                batch_id=batch_id,
                temperature=temperature,
                recorded_at=datetime.now(),
                employee_name=temp_data['employee_name'],
                days_deducted=days_deducted
            )
            
            db.session.add(temp_log)
            
            # Adjust batch expiry based on temperature
            actual_days_deducted = ExpiryService.adjust_batch_expiry(batch, temperature)
            
            # Update the log with actual days deducted (might be capped)
            temp_log.days_deducted = actual_days_deducted
            
            db.session.commit()
            
            if actual_days_deducted > 0:
                flash(f'Temperature logged! Warning: {actual_days_deducted:.2f} days deducted from shelf life due to temperature violation.', 'warning')
            else:
                flash('Temperature logged successfully. No shelf-life adjustment needed.', 'success')
            
            return redirect(url_for('batches.view_batch', batch_id=batch_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error logging temperature: {str(e)}', 'error')
    
    return render_template('temperature/log.html', batch=batch)


@temperature_bp.route('/history/<int:batch_id>')
@login_required
def temperature_history(batch_id):
    """View temperature history for a batch."""
    batch = Batch.query.get_or_404(batch_id)
    logs = TemperatureLog.get_logs_by_batch(batch_id)
    
    return render_template('temperature/history.html', batch=batch, logs=logs)


@temperature_bp.route('/violations')
@login_required
def recent_violations():
    """View recent temperature violations."""
    days_param = request.args.get('days', 30)
    
    try:
        days = int(days_param)
    except ValueError:
        days = 30
    
    violations = TemperatureLog.get_recent_violations(days)
    
    return render_template('temperature/violations.html', violations=violations, days=days)
