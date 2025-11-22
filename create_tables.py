"""
Create tables in the existing database
This script assumes the database 'qrattendance' already exists in MySQL
"""
from flask import Flask
from models import db, User
import config

def create_tables():
    """Create all tables in the existing database"""
    print("="*50)
    print("QR Code Attendance System - Create Tables")
    print("="*50)
    
    print("\nConnecting to database and creating tables...")
    print("Database: qrattendance")
    print("Host: 192.168.137.60")
    
    try:
        app = Flask(__name__)
        app.config.from_object(config.Config)
        db.init_app(app)
        
        with app.app_context():
            # Create all tables
            print("\nCreating tables...")
            db.create_all()
            print("✓ All tables created successfully")
            
            # Create default admin user if it doesn't exist
            print("\nChecking for default admin user...")
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin', email='admin@university.edu', role='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin user created")
                print("  Username: admin")
                print("  Password: admin123")
                print("  ⚠️  IMPORTANT: Change this password in production!")
            else:
                print("✓ Admin user already exists")
        
        print("\n" + "="*50)
        print("✓ Setup completed successfully!")
        print("="*50)
        print("\nYou can now run the application with: python app.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure:")
        print("  1. The database 'qrattendance' exists in MySQL")
        print("  2. The user 'admin' has permission to create tables")
        print("  3. MySQL server is accessible at 192.168.137.60")
        return False

if __name__ == '__main__':
    success = create_tables()
    if not success:
        import sys
        sys.exit(1)

