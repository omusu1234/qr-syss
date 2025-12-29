-- Migration script to add fraud detection columns and table
-- Run this script on your database to add fraud detection support

-- Add photo hash and face encoding columns to attendances table
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_hash VARCHAR(64);
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS face_encoding TEXT;

-- Create photo_matches table
CREATE TABLE IF NOT EXISTS photo_matches (
    id SERIAL PRIMARY KEY,
    source_attendance_id INTEGER NOT NULL REFERENCES attendances(id) ON DELETE CASCADE,
    target_attendance_id INTEGER NOT NULL REFERENCES attendances(id) ON DELETE CASCADE,
    match_type VARCHAR(20) NOT NULL,  -- 'duplicate' or 'face_similar'
    similarity_score FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by_lecturer BOOLEAN,
    verified_at TIMESTAMP,
    verified_by_user_id INTEGER REFERENCES users(id),
    notes TEXT,
    UNIQUE(source_attendance_id, target_attendance_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_match_source ON photo_matches(source_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_target ON photo_matches(target_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_verified ON photo_matches(verified_by_lecturer);

-- For MySQL (if using MySQL instead of PostgreSQL):
-- ALTER TABLE attendances ADD COLUMN photo_hash VARCHAR(64);
-- ALTER TABLE attendances ADD COLUMN face_encoding TEXT;
-- 
-- CREATE TABLE IF NOT EXISTS photo_matches (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     source_attendance_id INT NOT NULL,
--     target_attendance_id INT NOT NULL,
--     match_type VARCHAR(20) NOT NULL,
--     similarity_score FLOAT,
--     detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     verified_by_lecturer BOOLEAN,
--     verified_at TIMESTAMP NULL,
--     verified_by_user_id INT,
--     notes TEXT,
--     FOREIGN KEY (source_attendance_id) REFERENCES attendances(id) ON DELETE CASCADE,
--     FOREIGN KEY (target_attendance_id) REFERENCES attendances(id) ON DELETE CASCADE,
--     FOREIGN KEY (verified_by_user_id) REFERENCES users(id),
--     UNIQUE KEY unique_photo_match (source_attendance_id, target_attendance_id),
--     INDEX idx_match_source (source_attendance_id),
--     INDEX idx_match_target (target_attendance_id),
--     INDEX idx_match_verified (verified_by_lecturer)
-- );

