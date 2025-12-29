-- Quick fix SQL script to add missing fraud detection columns
-- Run this in your Neon database console or via psql

-- Add missing columns to attendances table
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_hash VARCHAR(64);
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS face_encoding TEXT;

-- Create photo_matches table (optional - for fraud detection review)
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_match_source ON photo_matches(source_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_target ON photo_matches(target_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_verified ON photo_matches(verified_by_lecturer);

-- Verify the changes
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'attendances' 
AND column_name IN ('photo_hash', 'face_encoding')
ORDER BY column_name;

SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns 
WHERE table_name = 'photo_matches'
ORDER BY ordinal_position;

