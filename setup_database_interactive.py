"""
Interactive Database setup script for QR Code Attendance System
This script will prompt you for MySQL credentials and create the database.
"""
import pymysql
import sys
import getpass
from flask import Flask
from models import db, User
import config

def get_credentials():
    """Get MySQL credentials from user"""
    print("\nPlease enter your MySQL credentials:")
    print("(Press Enter to use default values)")
    
    host = input("MySQL Host [192.168.137.60]: ").strip() or "192.168.137.60"
    user = input("MySQL Username [root]: ").strip() or "root"
    password = getpass.getpass("MySQL Password: ")
    if not password:
        password = input("MySQL Password (or press Enter for empty): ").strip()
    
    return host, user, password

def create_database(host, user, password):
    """Create the database and tables"""
    db_name = 'qr_attendance'
    
    print(f"\nConnecting to MySQL server at {host}...")
    print(f"User: {user}")
    print(f"Database: {db_name}")
    
    try:
        # Connect to MySQL server (without selecting a database)
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            print(f"\nCreating database '{db_name}' if it doesn't exist...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            connection.commit()
            print(f"✓ Database '{db_name}' created successfully")
            
            # Select the database
            cursor.execute(f"USE `{db_name}`")
            
            # Create tables using SQLAlchemy
            print("\nCreating tables...")
            app = Flask(__name__)
            
            # Update config with provided credentials
            db_uri = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
            app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
            db.init_app(app)
            
            with app.app_context():
                db.create_all()
                print("✓ All tables created successfully")
            
            # Create default admin user if it doesn't exist
            print("\nChecking for default admin user...")
            with app.app_context():
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
        
        connection.close()
        print("\n" + "="*50)
        print("Database setup completed successfully!")
        print("="*50)
        print(f"\nDon't forget to update config.py with your credentials:")
        print(f"SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}'")
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ MySQL Error: {e}")
        if "Access denied" in str(e):
            print("\nPossible issues:")
            print("  - Incorrect username or password")
            print("  - User doesn't have permission to create databases")
            print("  - MySQL server is not allowing remote connections")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("="*50)
    print("QR Code Attendance System - Database Setup")
    print("="*50)
    
    host, user, password = get_credentials()
    
    success = create_database(host, user, password)
    
    if success:
        print("\n✓ Setup complete! You can now run the application with: python app.py")
    else:
        print("\n❌ Setup failed. Please check your MySQL credentials and try again.")
        sys.exit(1)

