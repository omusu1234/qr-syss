-- PostgreSQL Schema for QR Attendance System
-- Run this script in your Render PostgreSQL database

-- Enable UUID extension if needed (optional)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS attendances CASCADE;
DROP TABLE IF EXISTS lecture_sessions CASCADE;
DROP TABLE IF EXISTS units CASCADE;
DROP TABLE IF EXISTS lecturers CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS activity_logs CASCADE;
DROP TABLE IF EXISTS login_history CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lecturers table
CREATE TABLE lecturers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL
);

-- Create units table
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    unit_code VARCHAR(20) UNIQUE NOT NULL,
    unit_name VARCHAR(200) NOT NULL,
    lecturer_id INTEGER NOT NULL REFERENCES lecturers(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lecture_sessions table
CREATE TABLE lecture_sessions (
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

-- Create attendances table
CREATE TABLE attendances (
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
    UNIQUE(session_id, admission_no)
);

-- Create notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    recipient_type VARCHAR(20) DEFAULT 'all_lecturers'
);

-- Create index for notifications
CREATE INDEX idx_notification_created ON notifications(created_at);

-- Create activity_logs table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for activity_logs
CREATE INDEX idx_activity_user ON activity_logs(user_id);
CREATE INDEX idx_activity_created ON activity_logs(created_at);
CREATE INDEX idx_activity_action ON activity_logs(action);

-- Create login_history table
CREATE TABLE login_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_at TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    failure_reason VARCHAR(255)
);

-- Create indexes for login_history
CREATE INDEX idx_login_user ON login_history(user_id);
CREATE INDEX idx_login_at ON login_history(login_at);

