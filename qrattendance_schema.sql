-- QR Code Attendance System Database Schema
-- Import this file in phpMyAdmin after creating the database 'qrattendance'

USE qrattendance;

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: lecturers
CREATE TABLE IF NOT EXISTS lecturers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_employee_id (employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: units
CREATE TABLE IF NOT EXISTS units (
    id INT AUTO_INCREMENT PRIMARY KEY,
    unit_code VARCHAR(20) UNIQUE NOT NULL,
    unit_name VARCHAR(200) NOT NULL,
    lecturer_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id) ON DELETE CASCADE,
    INDEX idx_unit_code (unit_code),
    INDEX idx_lecturer_id (lecturer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: lecture_sessions
CREATE TABLE IF NOT EXISTS lecture_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    unit_id INT NOT NULL,
    session_name VARCHAR(200) NOT NULL,
    qr_code_token VARCHAR(100) UNIQUE NOT NULL,
    qr_code_data TEXT NOT NULL,
    lecture_hall_latitude FLOAT NOT NULL,
    lecture_hall_longitude FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE,
    INDEX idx_unit_id (unit_id),
    INDEX idx_qr_code_token (qr_code_token),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: attendances
CREATE TABLE IF NOT EXISTS attendances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    admission_no VARCHAR(50) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    submission_latitude FLOAT NOT NULL,
    submission_longitude FLOAT NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    FOREIGN KEY (session_id) REFERENCES lecture_sessions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_session_admission (session_id, admission_no),
    INDEX idx_session_id (session_id),
    INDEX idx_admission_no (admission_no),
    INDEX idx_submitted_at (submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Success message
SELECT 'Database tables created successfully!' AS message;

