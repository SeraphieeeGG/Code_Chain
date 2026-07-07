"""
Routes for product management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.product import Product
from utils.validators import validate_product_data

product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('/')
@login_required
def list_products():
    """Display all products."""
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(Product.product_name.ilike(f'%{search_query}%'))
    
    # Apply category filter
    if category_filter:
        query = query.filter(Product.category == category_filter)
    
    products = query.all()
    categories = Product.get_all_categories()
    
    return render_template('products/list.html', 
                          products=products, 
                          categories=categories,
                          search_query=search_query,
                          category_filter=category_filter)


@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product."""
    if request.method == 'POST':
        try:
            # Get form data
            product_data = {
                'product_name': request.form.get('product_name'),
                'category': request.form.get('category'),
                'ideal_temperature': request.form.get('ideal_temperature'),
                'maximum_temperature': request.form.get('maximum_temperature'),
                'shelf_life_days': request.form.get('shelf_life_days')
            }
            
            # Validate data
            is_valid, error_message = validate_product_data(product_data)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('products/add.html', form_data=product_data)
            
            # Create new product
            product = Product(
                product_name=product_data['product_name'],
                category=product_data['category'],
                ideal_temperature=float(product_data['ideal_temperature']),
                maximum_temperature=float(product_data['maximum_temperature']),
                shelf_life_days=int(product_data['shelf_life_days'])
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash(f'Product "{product.product_name}" added successfully!', 'success')
            return redirect(url_for('products.list_products'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'error')
    
    return render_template('products/add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edit an existing product."""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            product_data = {
                'product_name': request.form.get('product_name'),
                'category': request.form.get('category'),
                'ideal_temperature': request.form.get('ideal_temperature'),
                'maximum_temperature': request.form.get('maximum_temperature'),
                'shelf_life_days': request.form.get('shelf_life_days')
            }
            
            # Validate data
            is_valid, error_message = validate_product_data(product_data)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('products/edit.html', product=product)
            
            # Update product
            product.product_name = product_data['product_name']
            product.category = product_data['category']
            product.ideal_temperature = float(product_data['ideal_temperature'])
            product.maximum_temperature = float(product_data['maximum_temperature'])
            product.shelf_life_days = int(product_data['shelf_life_days'])
            
            db.session.commit()
            
            flash(f'Product "{product.product_name}" updated successfully!', 'success')
            return redirect(url_for('products.list_products'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
    
    return render_template('products/edit.html', product=product)


@product_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a product."""
    try:
        product = Product.query.get_or_404(product_id)
        product_name = product.product_name
        
        # Check if product has batches
        if product.batches:
            flash(f'Cannot delete product "{product_name}". It has associated batches.', 'error')
            return redirect(url_for('products.list_products'))
        
        db.session.delete(product)
        db.session.commit()
        
        flash(f'Product "{product_name}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('products.list_products'))


@product_bp.route('/view/<int:product_id>')
@login_required
def view_product(product_id):
    """View product details."""
    product = Product.query.get_or_404(product_id)
    return render_template('products/view.html', product=product)
