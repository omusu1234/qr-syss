"""
Database Schema Diagnostic Script
Checks for missing columns and tables that might cause errors
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Database connection string
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_W9nEdeIrBN6y@ep-lingering-grass-aeb3wt2q-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

def check_database_schema():
    """Check database schema for missing columns and tables"""
    print("=" * 60)
    print("Database Schema Diagnostic")
    print("=" * 60)
    print(f"Connecting to database...")
    print()
    
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        
        with engine.connect() as conn:
            # Check if attendances table exists
            print("1. Checking 'attendances' table...")
            if inspector.has_table('attendances'):
                print("   ✅ 'attendances' table exists")
                
                # Get all columns in attendances table
                columns = inspector.get_columns('attendances')
                column_names = [col['name'] for col in columns]
                print(f"   Found {len(columns)} columns: {', '.join(column_names)}")
                print()
                
                # Check for required columns
                required_columns = {
                    'id': 'Primary key',
                    'session_id': 'Foreign key to lecture_sessions',
                    'admission_no': 'Student admission number',
                    'student_name': 'Student name',
                    'submission_latitude': 'Latitude',
                    'submission_longitude': 'Longitude',
                    'submitted_at': 'Submission timestamp',
                    'ip_address': 'IP address',
                    'is_late': 'Late flag',
                    'arrival_minutes_late': 'Minutes late',
                    'photo_data': 'Base64 photo data'
                }
                
                optional_columns = {
                    'photo_hash': 'Photo hash for duplicate detection',
                    'face_encoding': 'Face encoding for face matching',
                    'absence_reason': 'Reason for absence'
                }
                
                print("   Checking required columns:")
                missing_required = []
                for col_name, description in required_columns.items():
                    if col_name in column_names:
                        print(f"   ✅ {col_name} - {description}")
                    else:
                        print(f"   ❌ {col_name} - MISSING - {description}")
                        missing_required.append(col_name)
                
                print()
                print("   Checking optional columns (fraud detection):")
                missing_optional = []
                for col_name, description in optional_columns.items():
                    if col_name in column_names:
                        print(f"   ✅ {col_name} - {description}")
                    else:
                        print(f"   ⚠️  {col_name} - NOT PRESENT (optional) - {description}")
                        missing_optional.append(col_name)
                
                if missing_required:
                    print()
                    print("   ⚠️  WARNING: Missing required columns!")
                    print("   These columns are needed for basic functionality.")
                
                if missing_optional:
                    print()
                    print("   ℹ️  INFO: Optional fraud detection columns are missing.")
                    print("   The app will work without them, but fraud detection won't be available.")
                
            else:
                print("   ❌ 'attendances' table does NOT exist!")
                print("   This is a critical error - the app cannot function without this table.")
                return False
            
            print()
            print("2. Checking 'photo_matches' table...")
            if inspector.has_table('photo_matches'):
                print("   ✅ 'photo_matches' table exists")
                columns = inspector.get_columns('photo_matches')
                column_names = [col['name'] for col in columns]
                print(f"   Found {len(columns)} columns: {', '.join(column_names)}")
            else:
                print("   ⚠️  'photo_matches' table does NOT exist")
                print("   This is optional - fraud detection review won't work without it.")
                print("   The app will still function normally.")
            
            print()
            print("3. Checking other required tables...")
            required_tables = [
                'users', 'lecturers', 'units', 'lecture_sessions', 
                'notifications', 'activity_logs', 'login_history', 'departments'
            ]
            
            missing_tables = []
            for table_name in required_tables:
                if inspector.has_table(table_name):
                    print(f"   ✅ '{table_name}' table exists")
                else:
                    print(f"   ❌ '{table_name}' table MISSING")
                    missing_tables.append(table_name)
            
            print()
            print("=" * 60)
            print("Summary")
            print("=" * 60)
            
            if missing_required:
                print("❌ CRITICAL: Missing required columns in 'attendances' table:")
                for col in missing_required:
                    print(f"   - {col}")
                print()
                print("Run this SQL to add missing columns:")
                for col in missing_required:
                    if col == 'photo_data':
                        print(f"   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS {col} TEXT;")
                    elif col == 'photo_hash':
                        print(f"   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS {col} VARCHAR(64);")
                    elif col == 'face_encoding':
                        print(f"   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS {col} TEXT;")
                    elif col in ['is_late', 'arrival_minutes_late']:
                        print(f"   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS {col} INTEGER;")
                    else:
                        print(f"   -- Check your schema for {col}")
            
            if missing_optional:
                print("ℹ️  Optional fraud detection columns missing:")
                for col in missing_optional:
                    print(f"   - {col}")
                print()
                print("To enable fraud detection, run:")
                if 'photo_hash' in missing_optional:
                    print("   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_hash VARCHAR(64);")
                if 'face_encoding' in missing_optional:
                    print("   ALTER TABLE attendances ADD COLUMN IF NOT EXISTS face_encoding TEXT;")
                print("   -- Then run add_fraud_detection_migration.sql for the photo_matches table")
            
            if missing_tables:
                print("❌ CRITICAL: Missing required tables:")
                for table in missing_tables:
                    print(f"   - {table}")
            
            if not missing_required and not missing_tables:
                print("✅ All required tables and columns are present!")
                if missing_optional:
                    print("ℹ️  Optional fraud detection features are not set up.")
                else:
                    print("✅ Everything is set up correctly!")
            
            print()
            print("=" * 60)
            
            return len(missing_required) == 0 and len(missing_tables) == 0
            
    except SQLAlchemyError as e:
        print(f"❌ Database connection error: {str(e)}")
        print()
        print("Possible issues:")
        print("  - Incorrect connection string")
        print("  - Database server is down")
        print("  - Network connectivity issues")
        print("  - Authentication failed")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = check_database_schema()
    sys.exit(0 if success else 1)

