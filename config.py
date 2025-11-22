import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - Primary server
    # Supports both MySQL and PostgreSQL via DATABASE_URL environment variable
    # PostgreSQL format: postgresql://user:password@host:5432/database
    # MySQL format: mysql+pymysql://user:password@host:3306/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost:5432/qrattendance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Additional database servers for synchronization
    # Set to empty list to disable sync (recommended for production/cloud deployments)
    # Only enable if you have additional MySQL servers to sync to
    ENABLE_DB_SYNC = os.environ.get('ENABLE_DB_SYNC', 'false').lower() == 'true'
    
    if ENABLE_DB_SYNC:
        DATABASE_SERVERS = [
            {
                'host': os.environ.get('DB_HOST_1') or '192.168.137.60',
                'user': os.environ.get('DB_USER_1') or 'admin',
                'password': os.environ.get('DB_PASSWORD_1') or 'admin@123',
                'database': os.environ.get('DB_NAME_1') or 'qrattendance'
            },
            {
                'host': os.environ.get('DB_HOST_2') or '192.168.137.60',
                'user': os.environ.get('DB_USER_2') or 'admin',
                'password': os.environ.get('DB_PASSWORD_2') or 'admin@123',
                'database': os.environ.get('DB_NAME_2') or 'qrattendance'
            },
            {
                'host': os.environ.get('DB_HOST_3') or '192.168.137.60',
                'user': os.environ.get('DB_USER_3') or 'admin',
                'password': os.environ.get('DB_PASSWORD_3') or 'admin@123',
                'database': os.environ.get('DB_NAME_3') or 'qrattendance'
            }
        ]
    else:
        DATABASE_SERVERS = []  # Disable sync by default
    
    # QR Code expiration time (default: 2 hours)
    QR_CODE_EXPIRY_MINUTES = int(os.environ.get('QR_EXPIRY_MINUTES', 120))
    
    # Lecture hall radius in meters (default: 100 meters)
    LECTURE_HALL_RADIUS = int(os.environ.get('LECTURE_HALL_RADIUS', 100))
    
    # Rate limiting to prevent bulk submissions
    # Max number of submissions per IP address per time window
    MAX_SUBMISSIONS_PER_IP = int(os.environ.get('MAX_SUBMISSIONS_PER_IP', 1))
    SUBMISSION_TIME_WINDOW_MINUTES = int(os.environ.get('SUBMISSION_TIME_WINDOW_MINUTES', 10))
    
    # Session timeout
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Mapbox Configuration
    MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN') or 'pk.eyJ1IjoiZXJuZXN0MTIiLCJhIjoiY21pOG9uMGZ4MGE5djJrc2VsNWVxNmpmbyJ9.tOv_KzvDy-tkBsBiUzKrtQ'

