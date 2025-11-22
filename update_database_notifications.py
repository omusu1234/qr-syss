"""
Database update script to add notifications table
"""
import pymysql
from config import Config
import sys

def update_database():
    """Add notifications table"""
    try:
        # Parse database connection from config
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        
        # Extract connection details
        if db_uri.startswith('mysql+pymysql://'):
            db_uri = db_uri.replace('mysql+pymysql://', '')
        
        parts = db_uri.split('@')
        if len(parts) != 2:
            print("Error: Invalid database URI format")
            return False
        
        user_pass = parts[0].split(':')
        user = user_pass[0]
        password = ':'.join(user_pass[1:]) if len(user_pass) > 1 else ''
        
        # URL decode password
        if '%40' in password:
            password = password.replace('%40', '@')
        if '%23' in password:
            password = password.replace('%23', '#')
        
        host_db = parts[1].split('/')
        if len(host_db) != 2:
            print("Error: Invalid database URI format")
            return False
        
        host = host_db[0]
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 3306
        
        database = host_db[1]
        
        print(f"Connecting to MySQL server at {host}:{port}...")
        print(f"Database: {database}")
        
        # Connect to database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected successfully!")
        
        with connection.cursor() as cursor:
            # Check if table already exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'notifications'
            """, (database,))
            
            table_exists = cursor.fetchone()['count'] > 0
            
            if not table_exists:
                print("\nCreating notifications table...")
                cursor.execute("""
                    CREATE TABLE notifications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        message TEXT NOT NULL,
                        sender_id INT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        is_read BOOLEAN DEFAULT FALSE,
                        recipient_type VARCHAR(20) DEFAULT 'all_lecturers',
                        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                        INDEX idx_notification_created (created_at),
                        INDEX idx_sender_id (sender_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("✅ Notifications table created successfully!")
            else:
                print("✅ Notifications table already exists")
        
        connection.commit()
        connection.close()
        
        print("\n" + "="*50)
        print("✅ Database update completed successfully!")
        print("="*50)
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("="*50)
    print("Database Update Script - Notifications Table")
    print("="*50)
    print()
    
    success = update_database()
    
    if success:
        print("\n✅ All done! Notification system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

