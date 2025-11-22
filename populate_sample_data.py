"""
Populate database with sample data for testing
"""
from flask import Flask
from models import db, User, Lecturer, Unit, LectureSession, Attendance
from config import Config
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def populate_sample_data():
    """Add sample data to the database"""
    print("="*50)
    print("QR Code Attendance System - Populate Sample Data")
    print("="*50)
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("\n⚠️  Clearing existing sample data...")
        try:
            Attendance.query.delete()
            LectureSession.query.delete()
            Unit.query.delete()
            Lecturer.query.filter(Lecturer.user_id != 1).delete()  # Keep admin user
            User.query.filter(User.id != 1).delete()  # Keep admin user
            db.session.commit()
            print("✓ Existing data cleared")
        except Exception as e:
            print(f"Note: {e}")
            db.session.rollback()
        
        print("\nCreating sample lecturers...")
        
        # Sample Lecturer 1
        user1 = User(
            username='lecturer1',
            email='john.doe@university.edu',
            role='lecturer'
        )
        user1.set_password('lecturer123')
        db.session.add(user1)
        db.session.flush()
        
        lecturer1 = Lecturer(
            user_id=user1.id,
            full_name='Dr. John Doe',
            employee_id='EMP001'
        )
        db.session.add(lecturer1)
        db.session.flush()
        
        # Sample Lecturer 2
        user2 = User(
            username='lecturer2',
            email='jane.smith@university.edu',
            role='lecturer'
        )
        user2.set_password('lecturer123')
        db.session.add(user2)
        db.session.flush()
        
        lecturer2 = Lecturer(
            user_id=user2.id,
            full_name='Prof. Jane Smith',
            employee_id='EMP002'
        )
        db.session.add(lecturer2)
        db.session.flush()
        
        # Sample Lecturer 3
        user3 = User(
            username='lecturer3',
            email='michael.johnson@university.edu',
            role='lecturer'
        )
        user3.set_password('lecturer123')
        db.session.add(user3)
        db.session.flush()
        
        lecturer3 = Lecturer(
            user_id=user3.id,
            full_name='Dr. Michael Johnson',
            employee_id='EMP003'
        )
        db.session.add(lecturer3)
        db.session.flush()
        
        print("✓ Created 3 lecturers")
        
        print("\nCreating sample units/courses...")
        
        # Units for Lecturer 1
        unit1 = Unit(
            unit_code='CS101',
            unit_name='Introduction to Computer Science',
            lecturer_id=lecturer1.id
        )
        db.session.add(unit1)
        db.session.flush()
        
        unit2 = Unit(
            unit_code='CS201',
            unit_name='Data Structures and Algorithms',
            lecturer_id=lecturer1.id
        )
        db.session.add(unit2)
        db.session.flush()
        
        # Units for Lecturer 2
        unit3 = Unit(
            unit_code='MATH101',
            unit_name='Calculus I',
            lecturer_id=lecturer2.id
        )
        db.session.add(unit3)
        db.session.flush()
        
        unit4 = Unit(
            unit_code='MATH201',
            unit_name='Linear Algebra',
            lecturer_id=lecturer2.id
        )
        db.session.add(unit4)
        db.session.flush()
        
        # Units for Lecturer 3
        unit5 = Unit(
            unit_code='PHY101',
            unit_name='Physics Fundamentals',
            lecturer_id=lecturer3.id
        )
        db.session.add(unit5)
        db.session.flush()
        
        print("✓ Created 5 units/courses")
        
        print("\nCreating sample lecture sessions...")
        
        # Session 1 - CS101
        session1 = LectureSession(
            unit_id=unit1.id,
            session_name='CS101 - Week 1: Introduction',
            qr_code_token='sample_token_001',
            qr_code_data='sample_qr_base64_data_001',
            lecture_hall_latitude=-1.2921,  # Sample coordinates (Nairobi University area)
            lecture_hall_longitude=36.8219,
            expires_at=datetime.utcnow() + timedelta(hours=2),
            is_active=False  # Past session
        )
        db.session.add(session1)
        db.session.flush()
        
        # Session 2 - CS101 (Active)
        session2 = LectureSession(
            unit_id=unit1.id,
            session_name='CS101 - Week 2: Programming Basics',
            qr_code_token='sample_token_002',
            qr_code_data='sample_qr_base64_data_002',
            lecture_hall_latitude=-1.2921,
            lecture_hall_longitude=36.8219,
            expires_at=datetime.utcnow() + timedelta(hours=2),
            is_active=True
        )
        db.session.add(session2)
        db.session.flush()
        
        # Session 3 - CS201
        session3 = LectureSession(
            unit_id=unit2.id,
            session_name='CS201 - Week 1: Arrays and Lists',
            qr_code_token='sample_token_003',
            qr_code_data='sample_qr_base64_data_003',
            lecture_hall_latitude=-1.2921,
            lecture_hall_longitude=36.8219,
            expires_at=datetime.utcnow() + timedelta(hours=2),
            is_active=True
        )
        db.session.add(session3)
        db.session.flush()
        
        # Session 4 - MATH101
        session4 = LectureSession(
            unit_id=unit3.id,
            session_name='MATH101 - Week 1: Limits and Continuity',
            qr_code_token='sample_token_004',
            qr_code_data='sample_qr_base64_data_004',
            lecture_hall_latitude=-1.2921,
            lecture_hall_longitude=36.8219,
            expires_at=datetime.utcnow() + timedelta(hours=2),
            is_active=True
        )
        db.session.add(session4)
        db.session.flush()
        
        print("✓ Created 4 lecture sessions")
        
        print("\nCreating sample attendance records...")
        
        # Sample attendance for Session 1
        students_session1 = [
            ('STU001', 'Alice Johnson', -1.2920, 36.8218),
            ('STU002', 'Bob Williams', -1.2922, 36.8220),
            ('STU003', 'Charlie Brown', -1.2921, 36.8219),
            ('STU004', 'Diana Prince', -1.2920, 36.8217),
            ('STU005', 'Eve Davis', -1.2923, 36.8218),
        ]
        
        for admission_no, name, lat, lon in students_session1:
            attendance = Attendance(
                session_id=session1.id,
                admission_no=admission_no,
                student_name=name,
                submission_latitude=lat,
                submission_longitude=lon,
                submitted_at=datetime.utcnow() - timedelta(days=1),
                ip_address='192.168.1.100'
            )
            db.session.add(attendance)
        
        # Sample attendance for Session 2
        students_session2 = [
            ('STU001', 'Alice Johnson', -1.2921, 36.8219),
            ('STU006', 'Frank Miller', -1.2920, 36.8218),
            ('STU007', 'Grace Lee', -1.2922, 36.8220),
            ('STU008', 'Henry Wilson', -1.2921, 36.8219),
        ]
        
        for admission_no, name, lat, lon in students_session2:
            attendance = Attendance(
                session_id=session2.id,
                admission_no=admission_no,
                student_name=name,
                submission_latitude=lat,
                submission_longitude=lon,
                submitted_at=datetime.utcnow() - timedelta(hours=1),
                ip_address='192.168.1.101'
            )
            db.session.add(attendance)
        
        # Sample attendance for Session 3
        students_session3 = [
            ('STU009', 'Ivy Martinez', -1.2921, 36.8219),
            ('STU010', 'Jack Anderson', -1.2920, 36.8218),
            ('STU002', 'Bob Williams', -1.2922, 36.8220),
        ]
        
        for admission_no, name, lat, lon in students_session3:
            attendance = Attendance(
                session_id=session3.id,
                admission_no=admission_no,
                student_name=name,
                submission_latitude=lat,
                submission_longitude=lon,
                submitted_at=datetime.utcnow() - timedelta(minutes=30),
                ip_address='192.168.1.102'
            )
            db.session.add(attendance)
        
        print("✓ Created 12 attendance records")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ Sample data populated successfully!")
        print("="*50)
        
        print("\n📋 Summary:")
        print(f"  - Lecturers: 3")
        print(f"  - Units/Courses: 5")
        print(f"  - Lecture Sessions: 4")
        print(f"  - Attendance Records: 12")
        
        print("\n👤 Lecturer Login Credentials:")
        print("  Lecturer 1:")
        print("    Username: lecturer1")
        print("    Password: lecturer123")
        print("    Name: Dr. John Doe")
        print("    Units: CS101, CS201")
        print("\n  Lecturer 2:")
        print("    Username: lecturer2")
        print("    Password: lecturer123")
        print("    Name: Prof. Jane Smith")
        print("    Units: MATH101, MATH201")
        print("\n  Lecturer 3:")
        print("    Username: lecturer3")
        print("    Password: lecturer123")
        print("    Name: Dr. Michael Johnson")
        print("    Units: PHY101")
        
        print("\n✅ You can now test the application with this sample data!")

if __name__ == '__main__':
    populate_sample_data()

