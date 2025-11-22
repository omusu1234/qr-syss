"""
Database update script to add late tracking columns to lecture_sessions and attendances tables
"""
import pymysql
from config import Config
import sys

def update_database():
    """Add late tracking columns"""
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
            # Check and add session_start_time to lecture_sessions
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'lecture_sessions'
                AND column_name = 'session_start_time'
            """, (database,))
            
            col_exists = cursor.fetchone()['count'] > 0
            
            if not col_exists:
                print("\nAdding session_start_time column to lecture_sessions...")
                cursor.execute("""
                    ALTER TABLE lecture_sessions
                    ADD COLUMN session_start_time DATETIME NULL
                """)
                print("✅ session_start_time column added successfully!")
            else:
                print("✅ session_start_time column already exists")
            
            # Check and add late_threshold_minutes to lecture_sessions
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'lecture_sessions'
                AND column_name = 'late_threshold_minutes'
            """, (database,))
            
            col_exists = cursor.fetchone()['count'] > 0
            
            if not col_exists:
                print("\nAdding late_threshold_minutes column to lecture_sessions...")
                cursor.execute("""
                    ALTER TABLE lecture_sessions
                    ADD COLUMN late_threshold_minutes INT DEFAULT 15
                """)
                print("✅ late_threshold_minutes column added successfully!")
            else:
                print("✅ late_threshold_minutes column already exists")
            
            # Check and add is_late to attendances
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'attendances'
                AND column_name = 'is_late'
            """, (database,))
            
            col_exists = cursor.fetchone()['count'] > 0
            
            if not col_exists:
                print("\nAdding is_late column to attendances...")
                cursor.execute("""
                    ALTER TABLE attendances
                    ADD COLUMN is_late BOOLEAN DEFAULT FALSE
                """)
                print("✅ is_late column added successfully!")
            else:
                print("✅ is_late column already exists")
            
            # Check and add arrival_minutes_late to attendances
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'attendances'
                AND column_name = 'arrival_minutes_late'
            """, (database,))
            
            col_exists = cursor.fetchone()['count'] > 0
            
            if not col_exists:
                print("\nAdding arrival_minutes_late column to attendances...")
                cursor.execute("""
                    ALTER TABLE attendances
                    ADD COLUMN arrival_minutes_late INT NULL
                """)
                print("✅ arrival_minutes_late column added successfully!")
            else:
                print("✅ arrival_minutes_late column already exists")
            
            # Check and add absence_reason to attendances
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'attendances'
                AND column_name = 'absence_reason'
            """, (database,))
            
            col_exists = cursor.fetchone()['count'] > 0
            
            if not col_exists:
                print("\nAdding absence_reason column to attendances...")
                cursor.execute("""
                    ALTER TABLE attendances
                    ADD COLUMN absence_reason TEXT NULL
                """)
                print("✅ absence_reason column added successfully!")
            else:
                print("✅ absence_reason column already exists")
        
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
    print("Database Update Script - Late Tracking")
    print("="*50)
    print()
    
    success = update_database()
    
    if success:
        print("\n✅ All done! Late tracking system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

