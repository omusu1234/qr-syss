"""
Database update script to add departments table and update lecturers table
"""
import pymysql
from config import Config
import sys

def update_database():
    """Add departments table and update lecturers table"""
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
            # Check if departments table already exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'departments'
            """, (database,))
            
            table_exists = cursor.fetchone()['count'] > 0
            
            if not table_exists:
                print("\nCreating departments table...")
                cursor.execute("""
                    CREATE TABLE departments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE,
                        code VARCHAR(20) NOT NULL UNIQUE,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_name (name),
                        INDEX idx_code (code)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("✅ Departments table created successfully!")
            else:
                print("✅ Departments table already exists")
            
            # Check if department_id column exists in lecturers table
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = 'lecturers'
                AND column_name = 'department_id'
            """, (database,))
            
            column_exists = cursor.fetchone()['count'] > 0
            
            if not column_exists:
                print("\nAdding department_id column to lecturers table...")
                cursor.execute("""
                    ALTER TABLE lecturers
                    ADD COLUMN department_id INT NULL,
                    ADD CONSTRAINT fk_lecturer_department
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                    ON DELETE SET NULL
                """)
                print("✅ department_id column added successfully!")
            else:
                print("✅ department_id column already exists")
        
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
    print("Database Update Script - Departments")
    print("="*50)
    print()
    
    success = update_database()
    
    if success:
        print("\n✅ All done! Department system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        sys.exit(1)

