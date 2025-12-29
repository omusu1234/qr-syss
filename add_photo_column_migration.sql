-- Migration script to add photo_data column to attendances table
-- Run this script on your database to add photo support

-- For PostgreSQL
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT;

-- For MySQL (if using MySQL)
-- ALTER TABLE attendances ADD COLUMN photo_data TEXT;

-- Note: The column is nullable to allow existing records without photos
-- New attendance submissions will require a photo

