from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Base user model - can be Lecturer or Admin"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'lecturer' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship for lecturers
    lecturer_info = db.relationship('Lecturer', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_lecturer(self):
        return self.role == 'lecturer'

class Department(db.Model):
    """Department information"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)  # Department code like "CS", "ENG", etc.
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to lecturers
    lecturers = db.relationship('Lecturer', backref='department', lazy=True)

class Lecturer(db.Model):
    """Lecturer information"""
    __tablename__ = 'lecturers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    
    # Relationship to units
    units = db.relationship('Unit', backref='lecturer', lazy=True, cascade='all, delete-orphan')

class Unit(db.Model):
    """Course/Unit information"""
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True)
    unit_code = db.Column(db.String(20), unique=True, nullable=False)
    unit_name = db.Column(db.String(200), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('LectureSession', backref='unit', lazy=True, cascade='all, delete-orphan')

class LectureSession(db.Model):
    """Lecture session with QR code"""
    __tablename__ = 'lecture_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    session_name = db.Column(db.String(200), nullable=False)
    hall_name = db.Column(db.String(200), nullable=True)  # Name of the lecture hall
    qr_code_token = db.Column(db.String(100), unique=True, nullable=False)
    qr_code_data = db.Column(db.Text, nullable=False)  # Base64 encoded QR code image
    lecture_hall_latitude = db.Column(db.Float, nullable=False)
    lecture_hall_longitude = db.Column(db.Float, nullable=False)
    location_radius = db.Column(db.Float, nullable=False, default=100)  # Radius in meters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    session_start_time = db.Column(db.DateTime, nullable=True)  # Expected start time for late tracking
    late_threshold_minutes = db.Column(db.Integer, default=15)  # Minutes after start time considered late
    
    # Relationships
    attendances = db.relationship('Attendance', backref='session', lazy=True, cascade='all, delete-orphan')

class Attendance(db.Model):
    """Student attendance records"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('lecture_sessions.id'), nullable=False)
    admission_no = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    submission_latitude = db.Column(db.Float, nullable=False)
    submission_longitude = db.Column(db.Float, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    is_late = db.Column(db.Boolean, default=False)  # Late arrival tracking
    arrival_minutes_late = db.Column(db.Integer, nullable=True)  # Minutes late
    absence_reason = db.Column(db.Text, nullable=True)  # Reason for absence (if collected)
    photo_data = db.Column(db.Text, nullable=True)  # Base64 encoded photo of student
    
    # Unique constraint to prevent duplicate submissions
    __table_args__ = (db.UniqueConstraint('session_id', 'admission_no', name='unique_session_admission'),)

class Notification(db.Model):
    """Notifications sent by admin to lecturers"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Admin who sent it
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)  # For individual lecturer tracking
    recipient_type = db.Column(db.String(20), default='all_lecturers')  # 'all_lecturers' or 'specific'
    
    # Relationship to sender
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_notifications')
    
    # Index for efficient queries
    __table_args__ = (db.Index('idx_notification_created', 'created_at'),)

class ActivityLog(db.Model):
    """Audit log for system activities"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # e.g., 'create_session', 'login', 'delete_lecturer'
    entity_type = db.Column(db.String(50), nullable=True)  # e.g., 'lecturer', 'session', 'attendance'
    entity_id = db.Column(db.Integer, nullable=True)  # ID of the affected entity
    description = db.Column(db.Text, nullable=True)  # Human-readable description
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', foreign_keys=[user_id], backref='activity_logs')
    
    # Indexes for efficient queries
    __table_args__ = (
        db.Index('idx_activity_user', 'user_id'),
        db.Index('idx_activity_created', 'created_at'),
        db.Index('idx_activity_action', 'action'),
    )

class LoginHistory(db.Model):
    """Track user login history"""
    __tablename__ = 'login_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    login_at = db.Column(db.DateTime, default=datetime.utcnow)
    logout_at = db.Column(db.DateTime, nullable=True)
    success = db.Column(db.Boolean, default=True)  # False for failed login attempts
    failure_reason = db.Column(db.String(255), nullable=True)  # Reason for failed login
    
    # Relationship to user
    user = db.relationship('User', foreign_keys=[user_id], backref='login_history')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_login_user', 'user_id'),
        db.Index('idx_login_at', 'login_at'),
    )

