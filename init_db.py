"""Initialize database tables"""
import os
from app import app, db
from models import User, Lecturer, Unit, LectureSession, Attendance, Notification, Department, ActivityLog, LoginHistory

# Set database URL
os.environ['DATABASE_URL'] = 'postgresql://admin:v3Uti3qu17RvBLrrcrNlXDTVE3S6712u@dpg-d4dcib8gjchc73dsrb8g-a.oregon-postgres.render.com/admin_jxqo'

with app.app_context():
    print("Creating database tables...")
    try:
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Create default admin user if doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@university.edu', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created: username='admin', password='admin123'")
        else:
            print("✓ Admin user already exists")
            
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()

