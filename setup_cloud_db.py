import os
from flask import Flask
from models import db, User
from config import Config

def init_cloud_db(db_url):
    print(f"\nConnecting to database...")
    
    app = Flask(__name__)
    app.config.from_object(Config)
    # Override the config with the provided URL
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    
    with app.app_context():
        try:
            print("Creating tables...")
            db.create_all()
            print("✓ Tables created successfully!")
            
            # Check if admin exists
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin', email='admin@university.edu', role='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin created (username: admin, password: admin123)")
                print("⚠️ IMPORTANT: Change this password in the application!")
            else:
                print("✓ Admin user already exists.")
                
            print("\nDatabase is fully set up and ready to use on Vercel!")
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure your DATABASE_URL is correct.")
            print("2. Ensure you have installed postgres drivers locally: pip install psycopg2-binary")

if __name__ == '__main__':
    print("="*50)
    print("Cloud Database Initializer")
    print("="*50)
    url = input("Please paste your Cloud DATABASE_URL (e.g., postgresql://...): ").strip()
    if url:
        init_cloud_db(url)
    else:
        print("No URL provided. Exiting.")
