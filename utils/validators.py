"""
Validation functions for user input.
"""
from datetime import datetime


def validate_product_data(data):
    """
    Validate product data.
    
    Args:
        data (dict): Product data to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check required fields
    if not data.get('product_name') or not data.get('product_name').strip():
        return False, 'Product name is required.'
    
    if not data.get('category') or not data.get('category').strip():
        return False, 'Category is required.'
    
    # Validate temperatures
    try:
        ideal_temp = float(data.get('ideal_temperature', 0))
        max_temp = float(data.get('maximum_temperature', 0))
    except (ValueError, TypeError):
        return False, 'Temperatures must be numeric values.'
    
    if max_temp < ideal_temp:
        return False, 'Maximum temperature cannot be less than ideal temperature.'
    
    # Validate shelf life
    try:
        shelf_life = int(data.get('shelf_life_days', 0))
    except (ValueError, TypeError):
        return False, 'Shelf life must be a numeric value.'
    
    if shelf_life <= 0:
        return False, 'Shelf life must be greater than zero.'
    
    return True, None


def validate_batch_data(data):
    """
    Validate batch data.
    
    Args:
        data (dict): Batch data to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check required fields
    if not data.get('product_id'):
        return False, 'Product is required.'
    
    if not data.get('manufacturing_date'):
        return False, 'Manufacturing date is required.'
    
    # Validate manufacturing date
    try:
        mfg_date = datetime.strptime(data.get('manufacturing_date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return False, 'Invalid manufacturing date format.'
    
    # Manufacturing date cannot be in the future
    if mfg_date > datetime.now().date():
        return False, 'Manufacturing date cannot be in the future.'
    
    # Validate quantity
    try:
        quantity = int(data.get('quantity', 0))
    except (ValueError, TypeError):
        return False, 'Quantity must be a numeric value.'
    
    if quantity < 0:
        return False, 'Quantity cannot be negative.'
    
    return True, None


def validate_temperature_data(data):
    """
    Validate temperature log data.
    
    Args:
        data (dict): Temperature data to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check required fields
    if not data.get('employee_name') or not data.get('employee_name').strip():
        return False, 'Employee name is required.'
    
    # Validate temperature
    if not data.get('temperature'):
        return False, 'Temperature is required.'
    
    try:
        temperature = float(data.get('temperature'))
    except (ValueError, TypeError):
        return False, 'Temperature must be a numeric value.'
    
    # Reasonable temperature range (-50 to 50 Celsius)
    if temperature < -50 or temperature > 50:
        return False, 'Temperature must be between -50°C and 50°C.'
    
    return True, None
