"""
Database update script to add hall_name and location_radius columns to lecture_sessions table
"""
import pymysql
from config import Config
import sys

def update_database():
    """Add new columns to lecture_sessions table"""
    try:
        # Parse database connection from config
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        
        # Extract connection details
        # Format: mysql+pymysql://user:password@host/database
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
            # Check if columns already exist
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'lecture_sessions'
                AND COLUMN_NAME IN ('hall_name', 'location_radius')
            """, (database,))
            
            existing_columns = [row['COLUMN_NAME'] for row in cursor.fetchall()]
            
            # Add hall_name column if it doesn't exist
            if 'hall_name' not in existing_columns:
                print("\nAdding hall_name column...")
                cursor.execute("""
                    ALTER TABLE lecture_sessions 
                    ADD COLUMN hall_name VARCHAR(200) NULL 
                    AFTER session_name
                """)
                print("✅ hall_name column added successfully!")
            else:
                print("✅ hall_name column already exists")
            
            # Add location_radius column if it doesn't exist
            if 'location_radius' not in existing_columns:
                print("\nAdding location_radius column...")
                cursor.execute("""
                    ALTER TABLE lecture_sessions 
                    ADD COLUMN location_radius FLOAT NOT NULL DEFAULT 100 
                    AFTER lecture_hall_longitude
                """)
                print("✅ location_radius column added successfully!")
            else:
                print("✅ location_radius column already exists")
            
            # Update existing rows to have default radius if they don't have one
            cursor.execute("""
                UPDATE lecture_sessions 
                SET location_radius = 100 
                WHERE location_radius IS NULL OR location_radius = 0
            """)
            updated_rows = cursor.rowcount
            if updated_rows > 0:
                print(f"✅ Updated {updated_rows} existing records with default radius")
        
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
    print("Database Update Script")
    print("Adding hall_name and location_radius columns")
    print("="*50)
    print()
    
    success = update_database()
    
    if success:
        print("\n✅ All done! You can now use the new features.")
        sys.exit(0)
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

