-- PostgreSQL Sample Data for QR Attendance System
-- Run this AFTER running postgresql_schema.sql
-- Note: Password hashes are generated for 'admin123' and 'lecturer123'

-- Insert default admin user
-- Password: admin123
INSERT INTO users (username, email, password_hash, role, created_at) VALUES
('admin', 'admin@university.edu', 'pbkdf2:sha256:260000$VmbGb453i2yOQDMV$68f06085502fd6d25c8f4c278ec41f904fb4401c3bd450b12b93135677942e21', 'admin', CURRENT_TIMESTAMP);

-- Insert departments
INSERT INTO departments (name, code, description, created_at) VALUES
('Computer Science', 'CS', 'Department of Computer Science', CURRENT_TIMESTAMP),
('Mathematics', 'MATH', 'Department of Mathematics', CURRENT_TIMESTAMP),
('Physics', 'PHY', 'Department of Physics', CURRENT_TIMESTAMP);

-- Insert sample lecturers (users first, then lecturers)
-- Lecturer 1: Dr. John Doe
-- Password: lecturer123
INSERT INTO users (username, email, password_hash, role, created_at) VALUES
('lecturer1', 'john.doe@university.edu', 'pbkdf2:sha256:260000$0seOqbmgAEc2NYbo$c1abd596f5e942677212c1c95d1756951ef29f0a7c8bc525ddb63139c2e5c61d', 'lecturer', CURRENT_TIMESTAMP);

INSERT INTO lecturers (user_id, full_name, employee_id, department_id) VALUES
((SELECT id FROM users WHERE username = 'lecturer1'), 'Dr. John Doe', 'EMP001', (SELECT id FROM departments WHERE code = 'CS'));

-- Lecturer 2: Prof. Jane Smith
-- Password: lecturer123
INSERT INTO users (username, email, password_hash, role, created_at) VALUES
('lecturer2', 'jane.smith@university.edu', 'pbkdf2:sha256:260000$0seOqbmgAEc2NYbo$c1abd596f5e942677212c1c95d1756951ef29f0a7c8bc525ddb63139c2e5c61d', 'lecturer', CURRENT_TIMESTAMP);

INSERT INTO lecturers (user_id, full_name, employee_id, department_id) VALUES
((SELECT id FROM users WHERE username = 'lecturer2'), 'Prof. Jane Smith', 'EMP002', (SELECT id FROM departments WHERE code = 'MATH'));

-- Lecturer 3: Dr. Michael Johnson
-- Password: lecturer123
INSERT INTO users (username, email, password_hash, role, created_at) VALUES
('lecturer3', 'michael.johnson@university.edu', 'pbkdf2:sha256:260000$0seOqbmgAEc2NYbo$c1abd596f5e942677212c1c95d1756951ef29f0a7c8bc525ddb63139c2e5c61d', 'lecturer', CURRENT_TIMESTAMP);

INSERT INTO lecturers (user_id, full_name, employee_id, department_id) VALUES
((SELECT id FROM users WHERE username = 'lecturer3'), 'Dr. Michael Johnson', 'EMP003', (SELECT id FROM departments WHERE code = 'PHY'));

-- Insert units/courses
INSERT INTO units (unit_code, unit_name, lecturer_id, created_at) VALUES
('CS101', 'Introduction to Computer Science', (SELECT id FROM lecturers WHERE employee_id = 'EMP001'), CURRENT_TIMESTAMP),
('CS201', 'Data Structures and Algorithms', (SELECT id FROM lecturers WHERE employee_id = 'EMP001'), CURRENT_TIMESTAMP),
('MATH101', 'Calculus I', (SELECT id FROM lecturers WHERE employee_id = 'EMP002'), CURRENT_TIMESTAMP),
('MATH201', 'Linear Algebra', (SELECT id FROM lecturers WHERE employee_id = 'EMP002'), CURRENT_TIMESTAMP),
('PHY101', 'Physics Fundamentals', (SELECT id FROM lecturers WHERE employee_id = 'EMP003'), CURRENT_TIMESTAMP);

-- Insert sample lecture sessions
INSERT INTO lecture_sessions (unit_id, session_name, hall_name, qr_code_token, qr_code_data, lecture_hall_latitude, lecture_hall_longitude, location_radius, created_at, expires_at, is_active, session_start_time, late_threshold_minutes) VALUES
((SELECT id FROM units WHERE unit_code = 'CS101'), 'CS101 - Week 1: Introduction', 'Hall A', 'sample_token_001', 'sample_qr_base64_data_001', -1.2921, 36.8219, 100, CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day' + INTERVAL '2 hours', FALSE, CURRENT_TIMESTAMP - INTERVAL '1 day', 15),
((SELECT id FROM units WHERE unit_code = 'CS101'), 'CS101 - Week 2: Programming Basics', 'Hall A', 'sample_token_002', 'sample_qr_base64_data_002', -1.2921, 36.8219, 100, CURRENT_TIMESTAMP - INTERVAL '1 hour', CURRENT_TIMESTAMP + INTERVAL '1 hour', TRUE, CURRENT_TIMESTAMP - INTERVAL '1 hour', 15),
((SELECT id FROM units WHERE unit_code = 'CS201'), 'CS201 - Week 1: Arrays and Lists', 'Hall B', 'sample_token_003', 'sample_qr_base64_data_003', -1.2921, 36.8219, 100, CURRENT_TIMESTAMP - INTERVAL '30 minutes', CURRENT_TIMESTAMP + INTERVAL '1 hour 30 minutes', TRUE, CURRENT_TIMESTAMP - INTERVAL '30 minutes', 15),
((SELECT id FROM units WHERE unit_code = 'MATH101'), 'MATH101 - Week 1: Limits and Continuity', 'Hall C', 'sample_token_004', 'sample_qr_base64_data_004', -1.2921, 36.8219, 100, CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP, TRUE, CURRENT_TIMESTAMP - INTERVAL '2 hours', 15);

-- Insert sample attendance records
-- Session 1 attendance (past session)
INSERT INTO attendances (session_id, admission_no, student_name, submission_latitude, submission_longitude, submitted_at, ip_address, is_late, arrival_minutes_late) VALUES
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_001'), 'STU001', 'Alice Johnson', -1.2920, 36.8218, CURRENT_TIMESTAMP - INTERVAL '1 day', '192.168.1.100', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_001'), 'STU002', 'Bob Williams', -1.2922, 36.8220, CURRENT_TIMESTAMP - INTERVAL '1 day', '192.168.1.100', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_001'), 'STU003', 'Charlie Brown', -1.2921, 36.8219, CURRENT_TIMESTAMP - INTERVAL '1 day', '192.168.1.100', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_001'), 'STU004', 'Diana Prince', -1.2920, 36.8217, CURRENT_TIMESTAMP - INTERVAL '1 day', '192.168.1.100', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_001'), 'STU005', 'Eve Davis', -1.2923, 36.8218, CURRENT_TIMESTAMP - INTERVAL '1 day', '192.168.1.100', FALSE, NULL);

-- Session 2 attendance
INSERT INTO attendances (session_id, admission_no, student_name, submission_latitude, submission_longitude, submitted_at, ip_address, is_late, arrival_minutes_late) VALUES
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_002'), 'STU001', 'Alice Johnson', -1.2921, 36.8219, CURRENT_TIMESTAMP - INTERVAL '1 hour', '192.168.1.101', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_002'), 'STU006', 'Frank Miller', -1.2920, 36.8218, CURRENT_TIMESTAMP - INTERVAL '1 hour', '192.168.1.101', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_002'), 'STU007', 'Grace Lee', -1.2922, 36.8220, CURRENT_TIMESTAMP - INTERVAL '1 hour', '192.168.1.101', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_002'), 'STU008', 'Henry Wilson', -1.2921, 36.8219, CURRENT_TIMESTAMP - INTERVAL '1 hour', '192.168.1.101', FALSE, NULL);

-- Session 3 attendance
INSERT INTO attendances (session_id, admission_no, student_name, submission_latitude, submission_longitude, submitted_at, ip_address, is_late, arrival_minutes_late) VALUES
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_003'), 'STU009', 'Ivy Martinez', -1.2921, 36.8219, CURRENT_TIMESTAMP - INTERVAL '30 minutes', '192.168.1.102', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_003'), 'STU010', 'Jack Anderson', -1.2920, 36.8218, CURRENT_TIMESTAMP - INTERVAL '30 minutes', '192.168.1.102', FALSE, NULL),
((SELECT id FROM lecture_sessions WHERE qr_code_token = 'sample_token_003'), 'STU002', 'Bob Williams', -1.2922, 36.8220, CURRENT_TIMESTAMP - INTERVAL '30 minutes', '192.168.1.102', FALSE, NULL);

-- Summary:
-- - 1 Admin user (username: admin, password: admin123)
-- - 3 Lecturers (username: lecturer1/2/3, password: lecturer123)
-- - 3 Departments (CS, MATH, PHY)
-- - 5 Units/Courses
-- - 4 Lecture Sessions
-- - 12 Attendance Records

