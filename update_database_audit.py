"""
Database update script to add audit tables (activity_logs and login_history)
"""
import pymysql
from config import Config
import sys

def update_database():
    """Add audit tables"""
    try:
        # Parse database connection from config
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        
        if db_uri.startswith('mysql+pymysql://'):
            db_uri = db_uri.replace('mysql+pymysql://', '')
        
        parts = db_uri.split('@')
        if len(parts) != 2:
            print("Error: Invalid database URI format")
            return False
        
        user_pass = parts[0].split(':')
        user = user_pass[0]
        password = ':'.join(user_pass[1:]) if len(user_pass) > 1 else ''
        
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
            # Check if activity_logs table exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'activity_logs'
            """, (database,))
            
            table_exists = cursor.fetchone()['count'] > 0
            
            if not table_exists:
                print("\nCreating activity_logs table...")
                cursor.execute("""
                    CREATE TABLE activity_logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NULL,
                        action VARCHAR(100) NOT NULL,
                        entity_type VARCHAR(50) NULL,
                        entity_id INT NULL,
                        description TEXT NULL,
                        ip_address VARCHAR(45) NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                        INDEX idx_activity_user (user_id),
                        INDEX idx_activity_created (created_at),
                        INDEX idx_activity_action (action)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("✅ activity_logs table created successfully!")
            else:
                print("✅ activity_logs table already exists")
            
            # Check if login_history table exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'login_history'
            """, (database,))
            
            login_table_exists = cursor.fetchone()['count'] > 0
            
            if not login_table_exists:
                print("\nCreating login_history table...")
                cursor.execute("""
                    CREATE TABLE login_history (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        ip_address VARCHAR(45) NULL,
                        user_agent VARCHAR(255) NULL,
                        login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        logout_at DATETIME NULL,
                        success BOOLEAN DEFAULT TRUE,
                        failure_reason VARCHAR(255) NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        INDEX idx_login_user (user_id),
                        INDEX idx_login_at (login_at)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("✅ login_history table created successfully!")
            else:
                print("✅ login_history table already exists")
        
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
    print("Database Update Script - Audit Tables")
    print("="*50)
    print()
    
    success = update_database()
    
    if success:
        print("\n✅ All done! Audit logging system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

