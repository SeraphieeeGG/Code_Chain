"""
Installation test script.
Run this to verify your installation is working correctly.
"""
import sys


def test_python_version():
    """Check Python version."""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False


def test_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    required = ['flask', 'sqlalchemy', 'mysqlclient', 'dotenv', 'reportlab']
    missing = []
    
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (Missing)")
            missing.append(package)
    
    return len(missing) == 0, missing


def test_project_structure():
    """Check if project structure is correct."""
    print("\nChecking project structure...")
    import os
    
    required_dirs = ['models', 'routes', 'services', 'templates', 'static', 'utils']
    required_files = ['app.py', 'config.py', 'init_db.py', 'requirements.txt']
    
    all_exist = True
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ (Missing)")
            all_exist = False
    
    for file in required_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (Missing)")
            all_exist = False
    
    return all_exist


def test_env_file():
    """Check if .env file exists."""
    print("\nChecking configuration...")
    import os
    
    if os.path.isfile('.env'):
        print("  ✓ .env file exists")
        
        # Check if it has the required variables
        with open('.env', 'r') as f:
            content = f.read()
            has_db = 'DATABASE_URL' in content
            has_secret = 'SECRET_KEY' in content
            
            if has_db:
                print("  ✓ DATABASE_URL configured")
            else:
                print("  ✗ DATABASE_URL not found in .env")
            
            if has_secret:
                print("  ✓ SECRET_KEY configured")
            else:
                print("  ✗ SECRET_KEY not found in .env")
            
            return has_db and has_secret
    else:
        print("  ✗ .env file not found")
        print("     Copy .env.example to .env and configure it")
        return False


def test_database_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    
    try:
        from app import create_app
        from models import db
        
        app = create_app('development')
        
        with app.app_context():
            # Try to connect
            db.engine.connect()
            print("  ✓ Database connection successful")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['products', 'batches', 'temperature_logs']
            all_tables_exist = all(table in tables for table in expected_tables)
            
            if all_tables_exist:
                print("  ✓ All database tables exist")
                for table in expected_tables:
                    print(f"    - {table}")
                return True
            else:
                print("  ✗ Some tables are missing")
                print("     Run: python init_db.py")
                return False
                
    except Exception as e:
        print(f"  ✗ Database connection failed: {str(e)}")
        print("     Check your DATABASE_URL in .env")
        print("     Make sure MySQL is running")
        return False


def test_app_creation():
    """Test if Flask app can be created."""
    print("\nTesting Flask application...")
    
    try:
        from app import create_app
        app = create_app('development')
        print("  ✓ Flask app created successfully")
        
        # Check blueprints
        blueprints = ['dashboard', 'products', 'batches', 'temperature', 'reports']
        for bp in blueprints:
            if bp in app.blueprints:
                print(f"  ✓ {bp} blueprint registered")
            else:
                print(f"  ✗ {bp} blueprint not registered")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed to create Flask app: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Cold-Chain Expiry Accelerator - Installation Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Python Version", test_python_version()))
    
    deps_ok, missing = test_dependencies()
    results.append(("Dependencies", deps_ok))
    
    results.append(("Project Structure", test_project_structure()))
    results.append(("Configuration", test_env_file()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Flask Application", test_app_creation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print("  3. (Optional) Run: python seed_data.py for sample data")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Create .env file: copy .env.example .env")
        print("  - Configure database in .env")
        print("  - Initialize database: python init_db.py")
        print("\nFor detailed help, see SETUP.md")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
