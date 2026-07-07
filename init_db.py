"""
Database initialization script.
Run this script to create all database tables.
"""
from app import create_app
from models import db


def init_database():
    """Initialize database and create all tables."""
    app = create_app('development')
    
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        print('Database tables created successfully!')
        
        # Print table names
        print('\nCreated tables:')
        for table in db.metadata.sorted_tables:
            print(f'  - {table.name}')


if __name__ == '__main__':
    init_database()
