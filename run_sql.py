import psycopg2
import sys
import os

url = "postgresql://neondb_owner:npg_W9nEdeIrBN6y@ep-lingering-grass-aeb3wt2q-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

sql_commands = """
-- 1. Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create departments table
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create lecturers table
CREATE TABLE IF NOT EXISTS lecturers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL
);

-- 4. Create units table
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    unit_code VARCHAR(20) UNIQUE NOT NULL,
    unit_name VARCHAR(200) NOT NULL,
    lecturer_id INTEGER NOT NULL REFERENCES lecturers(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create lecture_sessions table
CREATE TABLE IF NOT EXISTS lecture_sessions (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    session_name VARCHAR(200) NOT NULL,
    hall_name VARCHAR(200),
    qr_code_token VARCHAR(100) UNIQUE NOT NULL,
    qr_code_data TEXT NOT NULL,
    lecture_hall_latitude DOUBLE PRECISION NOT NULL,
    lecture_hall_longitude DOUBLE PRECISION NOT NULL,
    location_radius DOUBLE PRECISION NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    session_start_time TIMESTAMP,
    late_threshold_minutes INTEGER DEFAULT 15
);

-- 6. Create attendances table
CREATE TABLE IF NOT EXISTS attendances (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES lecture_sessions(id) ON DELETE CASCADE,
    admission_no VARCHAR(50) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    submission_latitude DOUBLE PRECISION NOT NULL,
    submission_longitude DOUBLE PRECISION NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    is_late BOOLEAN DEFAULT FALSE,
    arrival_minutes_late INTEGER,
    absence_reason TEXT,
    photo_data TEXT,
    photo_hash VARCHAR(64),
    face_encoding TEXT,
    UNIQUE(session_id, admission_no)
);

-- 7. Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    recipient_type VARCHAR(20) DEFAULT 'all_lecturers'
);

-- 8. Create activity_logs table
CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Create login_history table
CREATE TABLE IF NOT EXISTS login_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_at TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    failure_reason VARCHAR(255)
);

-- 10. Create photo_matches table
CREATE TABLE IF NOT EXISTS photo_matches (
    id SERIAL PRIMARY KEY,
    source_attendance_id INTEGER NOT NULL REFERENCES attendances(id) ON DELETE CASCADE,
    target_attendance_id INTEGER NOT NULL REFERENCES attendances(id) ON DELETE CASCADE,
    match_type VARCHAR(20) NOT NULL,
    similarity_score FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by_lecturer BOOLEAN,
    verified_at TIMESTAMP,
    verified_by_user_id INTEGER REFERENCES users(id),
    notes TEXT,
    UNIQUE(source_attendance_id, target_attendance_id)
);

-- CREATE INDEXES
CREATE INDEX IF NOT EXISTS idx_notification_created ON notifications(created_at);
CREATE INDEX IF NOT EXISTS idx_activity_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_created ON activity_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_activity_action ON activity_logs(action);
CREATE INDEX IF NOT EXISTS idx_login_user ON login_history(user_id);
CREATE INDEX IF NOT EXISTS idx_login_at ON login_history(login_at);
CREATE INDEX IF NOT EXISTS idx_match_source ON photo_matches(source_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_target ON photo_matches(target_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_verified ON photo_matches(verified_by_lecturer);

-- INSERT DEFAULT ADMIN
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@university.edu', 
    'scrypt:32768:8:1$7N5Yf45RkKjTfP0T$9c9a0a10408e0b6e15967b5e4c6c22fbb4c98f5dbfc7d0c83a54d55b0a33a5927515b139db495c05c0883b27cf17d23d8c1be182ef6b39d1b6e4e04313f1722e', 
    'admin'
) ON CONFLICT (username) DO NOTHING;
"""

try:
    print("Connecting to Neon DB...")
    conn = psycopg2.connect(url)
    conn.autocommit = True
    cursor = conn.cursor()
    print("Executing schema...")
    cursor.execute(sql_commands)
    cursor.close()
    conn.close()
    print("✓ All tables created successfully!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
