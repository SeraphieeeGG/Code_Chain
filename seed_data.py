"""
Seed script to populate database with sample data for testing.
"""
from datetime import datetime, timedelta
from app import create_app
from models import db
from models.product import Product
from models.batch import Batch
from models.temperature_log import TemperatureLog
from services.expiry_service import ExpiryService


def seed_database():
    """Seed the database with sample data."""
    app = create_app('development')
    
    with app.app_context():
        print('Seeding database with sample data...')
        
        # Clear existing data
        print('Clearing existing data...')
        TemperatureLog.query.delete()
        Batch.query.delete()
        Product.query.delete()
        db.session.commit()
        
        # Create sample products
        print('Creating sample products...')
        products = [
            Product(
                product_name='Fresh Milk',
                category='Dairy',
                ideal_temperature=4.0,
                maximum_temperature=6.0,
                shelf_life_days=7
            ),
            Product(
                product_name='Chicken Breast',
                category='Meat',
                ideal_temperature=2.0,
                maximum_temperature=4.0,
                shelf_life_days=5
            ),
            Product(
                product_name='Greek Yogurt',
                category='Dairy',
                ideal_temperature=4.0,
                maximum_temperature=6.0,
                shelf_life_days=14
            ),
            Product(
                product_name='Fresh Salmon',
                category='Seafood',
                ideal_temperature=0.0,
                maximum_temperature=2.0,
                shelf_life_days=3
            ),
            Product(
                product_name='Lettuce',
                category='Vegetables',
                ideal_temperature=4.0,
                maximum_temperature=7.0,
                shelf_life_days=10
            ),
            Product(
                product_name='Ice Cream',
                category='Frozen',
                ideal_temperature=-18.0,
                maximum_temperature=-15.0,
                shelf_life_days=180
            ),
            Product(
                product_name='Cheese',
                category='Dairy',
                ideal_temperature=5.0,
                maximum_temperature=8.0,
                shelf_life_days=30
            ),
            Product(
                product_name='Ground Beef',
                category='Meat',
                ideal_temperature=1.0,
                maximum_temperature=4.0,
                shelf_life_days=2
            ),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print(f'Created {len(products)} products')
        
        # Create sample batches
        print('Creating sample batches...')
        batches = []
        
        # Batch 1: Fresh Milk - Safe
        batch1 = Batch(
            product_id=1,
            manufacturing_date=datetime.now().date() - timedelta(days=2),
            original_expiry=datetime.now().date() + timedelta(days=5),
            adjusted_expiry=datetime.now().date() + timedelta(days=5),
            quantity=50,
            status='Safe'
        )
        batches.append(batch1)
        
        # Batch 2: Chicken Breast - Warning
        batch2 = Batch(
            product_id=2,
            manufacturing_date=datetime.now().date() - timedelta(days=3),
            original_expiry=datetime.now().date() + timedelta(days=2),
            adjusted_expiry=datetime.now().date() + timedelta(days=2),
            quantity=30,
            status='Warning'
        )
        batches.append(batch2)
        
        # Batch 3: Greek Yogurt - Safe
        batch3 = Batch(
            product_id=3,
            manufacturing_date=datetime.now().date() - timedelta(days=1),
            original_expiry=datetime.now().date() + timedelta(days=13),
            adjusted_expiry=datetime.now().date() + timedelta(days=13),
            quantity=100,
            status='Safe'
        )
        batches.append(batch3)
        
        # Batch 4: Fresh Salmon - Critical
        batch4 = Batch(
            product_id=4,
            manufacturing_date=datetime.now().date() - timedelta(days=2),
            original_expiry=datetime.now().date() + timedelta(days=1),
            adjusted_expiry=datetime.now().date() + timedelta(days=1),
            quantity=20,
            status='Critical'
        )
        batches.append(batch4)
        
        # Batch 5: Lettuce - Safe (with violation)
        batch5 = Batch(
            product_id=5,
            manufacturing_date=datetime.now().date() - timedelta(days=3),
            original_expiry=datetime.now().date() + timedelta(days=7),
            adjusted_expiry=datetime.now().date() + timedelta(days=5),  # Adjusted due to violation
            quantity=75,
            status='Safe'
        )
        batches.append(batch5)
        
        # Batch 6: Ice Cream - Safe
        batch6 = Batch(
            product_id=6,
            manufacturing_date=datetime.now().date() - timedelta(days=30),
            original_expiry=datetime.now().date() + timedelta(days=150),
            adjusted_expiry=datetime.now().date() + timedelta(days=150),
            quantity=200,
            status='Safe'
        )
        batches.append(batch6)
        
        # Batch 7: Cheese - Warning (with violation)
        batch7 = Batch(
            product_id=7,
            manufacturing_date=datetime.now().date() - timedelta(days=26),
            original_expiry=datetime.now().date() + timedelta(days=4),
            adjusted_expiry=datetime.now().date() + timedelta(days=2),  # Adjusted due to violations
            quantity=60,
            status='Warning'
        )
        batches.append(batch7)
        
        # Batch 8: Ground Beef - Expired
        batch8 = Batch(
            product_id=8,
            manufacturing_date=datetime.now().date() - timedelta(days=4),
            original_expiry=datetime.now().date() - timedelta(days=2),
            adjusted_expiry=datetime.now().date() - timedelta(days=2),
            quantity=15,
            status='Expired'
        )
        batches.append(batch8)
        
        for batch in batches:
            db.session.add(batch)
        
        db.session.commit()
        print(f'Created {len(batches)} batches')
        
        # Create sample temperature logs
        print('Creating sample temperature logs...')
        
        # Logs for Batch 1 (Milk) - All safe
        temp_logs = [
            TemperatureLog(batch_id=1, temperature=4.5, 
                         recorded_at=datetime.now() - timedelta(hours=48),
                         employee_name='John Smith', days_deducted=0),
            TemperatureLog(batch_id=1, temperature=5.0,
                         recorded_at=datetime.now() - timedelta(hours=24),
                         employee_name='Jane Doe', days_deducted=0),
            TemperatureLog(batch_id=1, temperature=4.2,
                         recorded_at=datetime.now() - timedelta(hours=12),
                         employee_name='Bob Wilson', days_deducted=0),
        ]
        
        # Logs for Batch 2 (Chicken) - One violation
        temp_logs.extend([
            TemperatureLog(batch_id=2, temperature=3.0,
                         recorded_at=datetime.now() - timedelta(hours=60),
                         employee_name='Alice Johnson', days_deducted=0),
            TemperatureLog(batch_id=2, temperature=6.5,  # Violation
                         recorded_at=datetime.now() - timedelta(hours=36),
                         employee_name='Charlie Brown', days_deducted=1.25),
            TemperatureLog(batch_id=2, temperature=2.5,
                         recorded_at=datetime.now() - timedelta(hours=12),
                         employee_name='David Lee', days_deducted=0),
        ])
        
        # Logs for Batch 5 (Lettuce) - With violations
        temp_logs.extend([
            TemperatureLog(batch_id=5, temperature=5.0,
                         recorded_at=datetime.now() - timedelta(hours=72),
                         employee_name='Emily Davis', days_deducted=0),
            TemperatureLog(batch_id=5, temperature=11.0,  # Violation
                         recorded_at=datetime.now() - timedelta(hours=48),
                         employee_name='Frank Miller', days_deducted=2.0),
            TemperatureLog(batch_id=5, temperature=6.5,
                         recorded_at=datetime.now() - timedelta(hours=24),
                         employee_name='Grace Taylor', days_deducted=0),
        ])
        
        # Logs for Batch 7 (Cheese) - Multiple violations
        temp_logs.extend([
            TemperatureLog(batch_id=7, temperature=7.0,
                         recorded_at=datetime.now() - timedelta(hours=120),
                         employee_name='Henry White', days_deducted=0),
            TemperatureLog(batch_id=7, temperature=10.0,  # Violation
                         recorded_at=datetime.now() - timedelta(hours=96),
                         employee_name='Iris Green', days_deducted=1.0),
            TemperatureLog(batch_id=7, temperature=12.0,  # Violation
                         recorded_at=datetime.now() - timedelta(hours=48),
                         employee_name='Jack Black', days_deducted=2.0),
            TemperatureLog(batch_id=7, temperature=7.5,
                         recorded_at=datetime.now() - timedelta(hours=12),
                         employee_name='Kate Brown', days_deducted=0),
        ])
        
        for log in temp_logs:
            db.session.add(log)
        
        db.session.commit()
        print(f'Created {len(temp_logs)} temperature logs')
        
        # Update batch statuses
        print('Updating batch statuses...')
        for batch in Batch.query.all():
            batch.update_status()
        db.session.commit()
        
        print('\n✓ Database seeding completed successfully!')
        print('\nSample Data Summary:')
        print(f'  - Products: {Product.query.count()}')
        print(f'  - Batches: {Batch.query.count()}')
        print(f'  - Temperature Logs: {TemperatureLog.query.count()}')
        print(f'  - Safe Batches: {Batch.query.filter_by(status="Safe").count()}')
        print(f'  - Warning Batches: {Batch.query.filter_by(status="Warning").count()}')
        print(f'  - Critical Batches: {Batch.query.filter_by(status="Critical").count()}')
        print(f'  - Expired Batches: {Batch.query.filter_by(status="Expired").count()}')
        print(f'  - Temperature Violations: {TemperatureLog.query.filter(TemperatureLog.days_deducted > 0).count()}')
        print('\nYou can now run the application with: python app.py')


if __name__ == '__main__':
    seed_database()
