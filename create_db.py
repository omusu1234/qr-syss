"""
Create database script with specific credentials
"""
import pymysql
from flask import Flask
from models import db, User
import config

def create_database():
    """Create the database and tables"""
    host = '192.168.137.60'
    user = 'admin'
    password = 'admin@123'
    db_name = 'qrattendance'
    
    print(f"Connecting to MySQL server at {host}...")
    print(f"User: {user}")
    print(f"Database: {db_name}")
    
    try:
        # Try to connect directly to the database first
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"✓ Connected to database '{db_name}'")
            db_exists = True
        except pymysql.Error:
            # If database doesn't exist, try to connect without database and create it
            print(f"\nDatabase '{db_name}' doesn't exist. Attempting to create...")
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                connection.commit()
                print(f"✓ Database '{db_name}' created successfully")
            connection.close()
            # Reconnect to the new database
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            db_exists = True
        
        with connection.cursor() as cursor:
            # Select the database
            cursor.execute(f"USE `{db_name}`")
            
            # Create tables using SQLAlchemy
            print("\nCreating tables...")
            app = Flask(__name__)
            
            # Update config with provided credentials
            # URL encode the password (especially @ symbol)
            import urllib.parse
            encoded_password = urllib.parse.quote_plus(password)
            db_uri = f"mysql+pymysql://{user}:{encoded_password}@{host}/{db_name}"
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
    
    success = create_database()
    
    if success:
        print("\n✓ Setup complete! You can now run the application with: python app.py")
    else:
        print("\n❌ Setup failed. Please check your MySQL credentials and try again.")
        import sys
        sys.exit(1)

