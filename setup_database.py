"""
Database setup script for QR Code Attendance System
This script creates the database and all tables automatically.
"""
import pymysql
import sys
import config

def create_database():
    """Create the database and tables"""
    # Parse database connection from SQLALCHEMY_DATABASE_URI
    # Format: mysql+pymysql://user:password@host/database
    db_uri = config.Config.SQLALCHEMY_DATABASE_URI
    if db_uri.startswith('mysql+pymysql://'):
        db_uri = db_uri.replace('mysql+pymysql://', '')
    
    # Extract components
    parts = db_uri.split('@')
    if len(parts) != 2:
        print("Error: Invalid database URI format")
        return False
    
    auth_part = parts[0]
    host_db_part = parts[1]
    
    # Extract user and password
    if ':' in auth_part:
        user, password = auth_part.split(':', 1)
    else:
        user = auth_part
        password = ''
    
    # Extract host and database
    if '/' in host_db_part:
        host_part, db_name = host_db_part.split('/', 1)
        if ':' in host_part:
            host, port = host_part.split(':')
            port = int(port)
        else:
            host = host_part
            port = 3306
    else:
        host = host_db_part
        port = 3306
        db_name = 'qr_attendance'
    
    print(f"Connecting to MySQL server at {host}:{port}...")
    print(f"User: {user}")
    print(f"Database: {db_name}")
    
    try:
        # Connect to MySQL server (without selecting a database)
        connection = pymysql.connect(
            host=host,
            port=port,
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
            print(f"✓ Database '{db_name}' ready")
            
            # Select the database
            cursor.execute(f"USE `{db_name}`")
            
            # Create tables using SQLAlchemy
            print("\nCreating tables using SQLAlchemy...")
            from flask import Flask
            from models import db, User, Lecturer, Unit, LectureSession, Attendance
            
            app = Flask(__name__)
            app.config.from_object(config.Config)
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
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def setup_sync_databases():
    """Setup databases for synchronization servers"""
    print("\n" + "="*50)
    print("Setting up synchronization databases...")
    print("="*50)
    
    for i, server_config in enumerate(config.Config.DATABASE_SERVERS, 1):
        print(f"\nServer {i}: {server_config['host']}")
        try:
            connection = pymysql.connect(
                host=server_config['host'],
                user=server_config['user'],
                password=server_config['password'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with connection.cursor() as cursor:
                db_name = server_config['database']
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                connection.commit()
                cursor.execute(f"USE `{db_name}`")
                
                # Create tables
                from flask import Flask
                from models import db
                
                app = Flask(__name__)
                app.config.from_object(config.Config)
                # Set the sync database URI
                sync_uri = f"mysql+pymysql://{server_config['user']}:{server_config['password']}@{server_config['host']}/{db_name}"
                app.config['SQLALCHEMY_DATABASE_URI'] = sync_uri
                db.init_app(app)
                
                with app.app_context():
                    db.create_all()
                
                print(f"✓ Database '{db_name}' on {server_config['host']} ready")
            
            connection.close()
        except Exception as e:
            print(f"⚠️  Warning: Could not setup sync database on {server_config['host']}: {e}")
            print("   (This is okay if you're using the same database for all servers)")

if __name__ == '__main__':
    print("="*50)
    print("QR Code Attendance System - Database Setup")
    print("="*50)
    
    success = create_database()
    
    if success:
        # Optionally setup sync databases
        setup_sync_databases()
        print("\n✓ Setup complete! You can now run the application with: python app.py")
    else:
        print("\n❌ Setup failed. Please check your MySQL connection settings in config.py")
        sys.exit(1)
