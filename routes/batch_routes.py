"""
Routes for batch management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime, timedelta
from models import db
from models.product import Product
from models.batch import Batch
from utils.validators import validate_batch_data

batch_bp = Blueprint('batches', __name__, url_prefix='/batches')


@batch_bp.route('/')
@login_required
def list_batches():
    """Display all batches."""
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    product_filter = request.args.get('product_id', '')
    
    query = Batch.query
    
    # Apply search filter (search by batch ID or product name)
    if search_query:
        query = query.join(Product).filter(
            db.or_(
                Batch.batch_id == int(search_query) if search_query.isdigit() else False,
                Product.product_name.ilike(f'%{search_query}%')
            )
        )
    
    # Apply status filter
    if status_filter:
        query = query.filter(Batch.status == status_filter)
    
    # Apply product filter
    if product_filter:
        query = query.filter(Batch.product_id == int(product_filter))
    
    batches = query.all()
    products = Product.query.all()
    
    return render_template('batches/list.html', 
                          batches=batches,
                          products=products,
                          search_query=search_query,
                          status_filter=status_filter,
                          product_filter=product_filter)


@batch_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_batch():
    """Add a new batch."""
    products = Product.query.all()
    
    if request.method == 'POST':
        try:
            # Get form data
            batch_data = {
                'product_id': request.form.get('product_id'),
                'manufacturing_date': request.form.get('manufacturing_date'),
                'quantity': request.form.get('quantity')
            }
            
            # Validate data
            is_valid, error_message = validate_batch_data(batch_data)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('batches/add.html', products=products, form_data=batch_data)
            
            # Get product to calculate expiry date
            product = Product.query.get(int(batch_data['product_id']))
            if not product:
                flash('Invalid product selected.', 'error')
                return render_template('batches/add.html', products=products, form_data=batch_data)
            
            # Parse manufacturing date
            mfg_date = datetime.strptime(batch_data['manufacturing_date'], '%Y-%m-%d').date()
            
            # Calculate expiry date
            expiry_date = mfg_date + timedelta(days=product.shelf_life_days)
            
            # Create new batch
            batch = Batch(
                product_id=int(batch_data['product_id']),
                manufacturing_date=mfg_date,
                original_expiry=expiry_date,
                adjusted_expiry=expiry_date,
                quantity=int(batch_data['quantity']),
                status='Safe'
            )
            
            # Update status based on expiry
            batch.update_status()
            
            db.session.add(batch)
            db.session.commit()
            
            flash(f'Batch #{batch.batch_id} added successfully!', 'success')
            return redirect(url_for('batches.list_batches'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding batch: {str(e)}', 'error')
    
    return render_template('batches/add.html', products=products)


@batch_bp.route('/edit/<int:batch_id>', methods=['GET', 'POST'])
@login_required
def edit_batch(batch_id):
    """Edit an existing batch."""
    batch = Batch.query.get_or_404(batch_id)
    products = Product.query.all()
    
    if request.method == 'POST':
        try:
            # Get form data
            batch_data = {
                'product_id': request.form.get('product_id'),
                'quantity': request.form.get('quantity')
            }
            
            # Validate quantity
            if not batch_data['quantity'] or int(batch_data['quantity']) < 0:
                flash('Quantity must be a non-negative number.', 'error')
                return render_template('batches/edit.html', batch=batch, products=products)
            
            # Update batch (dates are not editable for data integrity)
            batch.product_id = int(batch_data['product_id'])
            batch.quantity = int(batch_data['quantity'])
            batch.update_status()
            
            db.session.commit()
            
            flash(f'Batch #{batch.batch_id} updated successfully!', 'success')
            return redirect(url_for('batches.list_batches'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating batch: {str(e)}', 'error')
    
    return render_template('batches/edit.html', batch=batch, products=products)


@batch_bp.route('/delete/<int:batch_id>', methods=['POST'])
@login_required
def delete_batch(batch_id):
    """Delete a batch."""
    try:
        batch = Batch.query.get_or_404(batch_id)
        
        db.session.delete(batch)
        db.session.commit()
        
        flash(f'Batch #{batch_id} deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting batch: {str(e)}', 'error')
    
    return redirect(url_for('batches.list_batches'))


@batch_bp.route('/view/<int:batch_id>')
@login_required
def view_batch(batch_id):
    """View batch details with temperature history."""
    batch = Batch.query.get_or_404(batch_id)
    return render_template('batches/view.html', batch=batch)


@batch_bp.route('/expiring')
@login_required
def expiring_batches():
    """Display batches expiring soon."""
    days_param = request.args.get('days', 7)
    
    try:
        days = int(days_param)
    except ValueError:
        days = 7
    
    expiring = Batch.get_expiring_soon(days)
    expired = Batch.get_expired()
    
    return render_template('batches/expiring.html', 
                          expiring=expiring,
                          expired=expired,
                          days=days)
