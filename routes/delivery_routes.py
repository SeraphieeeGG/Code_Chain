"""
Routes for delivery management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from models import db
from models.delivery import Delivery
from models.batch import Batch

delivery_bp = Blueprint('deliveries', __name__, url_prefix='/deliveries')


@delivery_bp.route('/')
@login_required
def list_deliveries():
    """Display all deliveries."""
    status_filter = request.args.get('status', '')
    
    query = Delivery.query
    
    if status_filter:
        query = query.filter(Delivery.delivery_status == status_filter)
    
    deliveries = query.order_by(Delivery.created_at.desc()).all()
    
    return render_template('deliveries/list.html', 
                          deliveries=deliveries,
                          status_filter=status_filter)


@delivery_bp.route('/add/<int:batch_id>', methods=['GET', 'POST'])
@login_required
def add_delivery(batch_id):
    """Add a delivery for a batch."""
    batch = Batch.query.get_or_404(batch_id)
    
    if request.method == 'POST':
        try:
            destination = request.form.get('destination', '').strip()
            delivery_status = request.form.get('delivery_status', 'Pending')
            
            if not destination:
                flash('Destination is required.', 'error')
                return render_template('deliveries/add.html', batch=batch)
            
            delivery = Delivery(
                batch_id=batch_id,
                destination=destination,
                delivery_status=delivery_status
            )
            
            db.session.add(delivery)
            db.session.commit()
            
            flash(f'Delivery created successfully for Batch #{batch_id}!', 'success')
            return redirect(url_for('deliveries.list_deliveries'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating delivery: {str(e)}', 'error')
    
    return render_template('deliveries/add.html', batch=batch)


@delivery_bp.route('/edit/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def edit_delivery(delivery_id):
    """Edit delivery status."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    if request.method == 'POST':
        try:
            destination = request.form.get('destination', '').strip()
            delivery_status = request.form.get('delivery_status')
            
            if not destination:
                flash('Destination is required.', 'error')
                return render_template('deliveries/edit.html', delivery=delivery)
            
            delivery.destination = destination
            delivery.delivery_status = delivery_status
            
            # Set delivery date when marked as Delivered
            if delivery_status == 'Delivered' and not delivery.delivery_date:
                delivery.delivery_date = datetime.now()
            
            db.session.commit()
            
            flash(f'Delivery #{delivery_id} updated successfully!', 'success')
            return redirect(url_for('deliveries.list_deliveries'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating delivery: {str(e)}', 'error')
    
    return render_template('deliveries/edit.html', delivery=delivery)


@delivery_bp.route('/delete/<int:delivery_id>', methods=['POST'])
@login_required
def delete_delivery(delivery_id):
    """Delete a delivery."""
    try:
        delivery = Delivery.query.get_or_404(delivery_id)
        
        db.session.delete(delivery)
        db.session.commit()
        
        flash(f'Delivery #{delivery_id} deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting delivery: {str(e)}', 'error')
    
    return redirect(url_for('deliveries.list_deliveries'))


@delivery_bp.route('/view/<int:delivery_id>')
@login_required
def view_delivery(delivery_id):
    """View delivery details."""
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('deliveries/view.html', delivery=delivery)
