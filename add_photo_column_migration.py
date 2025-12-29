"""
Migration script to add photo_data column to attendances table
Run this script to update your database schema
"""
from app import app
from models import db
from sqlalchemy import text

def migrate_database():
    """Add photo_data column to attendances table"""
    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('attendances')]
            
            if 'photo_data' in columns:
                print("✓ Column 'photo_data' already exists in attendances table")
                return
            
            # Add the column
            print("Adding photo_data column to attendances table...")
            db.session.execute(text("ALTER TABLE attendances ADD COLUMN photo_data TEXT"))
            db.session.commit()
            print("✓ Successfully added photo_data column to attendances table")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding photo_data column: {str(e)}")
            print("You may need to run the SQL migration script manually:")
            print("  PostgreSQL: ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT;")
            print("  MySQL: ALTER TABLE attendances ADD COLUMN photo_data TEXT;")
            raise

if __name__ == '__main__':
    migrate_database()

