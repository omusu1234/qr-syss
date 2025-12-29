"""
Standalone migration script for Neon database
This script connects directly to the database without loading the full app
"""
import os
import sys
from sqlalchemy import create_engine, text

# Neon database connection string
DATABASE_URL = "postgresql://neondb_owner:npg_W9nEdeIrBN6y@ep-lingering-grass-aeb3wt2q-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require"

def migrate():
    """Add photo_data column to attendances table"""
    try:
        print("Connecting to Neon database...")
        engine = create_engine(DATABASE_URL)
        
        with engine.begin() as conn:
            print("Adding photo_data column to attendances table...")
            # Use IF NOT EXISTS to make it safe to run multiple times
            conn.execute(text("ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT"))
            print("✓ Successfully added photo_data column to attendances table!")
            print("The photo capture feature is now ready to use.")
            return True
    except Exception as e:
        print(f"✗ Error running migration: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the database URL is correct")
        print("3. Ensure psycopg2-binary is installed: pip install psycopg2-binary")
        return False

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)

