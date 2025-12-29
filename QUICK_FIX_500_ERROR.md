# Quick Fix for 500 Internal Server Error

## Problem
The 500 error occurs because the fraud detection database columns and tables don't exist yet.

## Solution

You have two options:

### Option 1: Run Database Migration (Recommended)

Run the migration script to add the required columns and tables:

**For PostgreSQL (Neon, etc.):**
```sql
-- Run this in your database console or via migration script
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_hash VARCHAR(64);
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS face_encoding TEXT;

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

CREATE INDEX IF NOT EXISTS idx_match_source ON photo_matches(source_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_target ON photo_matches(target_attendance_id);
CREATE INDEX IF NOT EXISTS idx_match_verified ON photo_matches(verified_by_lecturer);
```

**For MySQL:**
```sql
ALTER TABLE attendances ADD COLUMN photo_hash VARCHAR(64);
ALTER TABLE attendances ADD COLUMN face_encoding TEXT;

CREATE TABLE IF NOT EXISTS photo_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_attendance_id INT NOT NULL,
    target_attendance_id INT NOT NULL,
    match_type VARCHAR(20) NOT NULL,
    similarity_score FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by_lecturer BOOLEAN,
    verified_at TIMESTAMP NULL,
    verified_by_user_id INT,
    notes TEXT,
    FOREIGN KEY (source_attendance_id) REFERENCES attendances(id) ON DELETE CASCADE,
    FOREIGN KEY (target_attendance_id) REFERENCES attendances(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by_user_id) REFERENCES users(id),
    UNIQUE KEY unique_photo_match (source_attendance_id, target_attendance_id),
    INDEX idx_match_source (source_attendance_id),
    INDEX idx_match_target (target_attendance_id),
    INDEX idx_match_verified (verified_by_lecturer)
);
```

### Option 2: Use the Migration Script

The code has been updated to gracefully handle missing columns/tables, so the app should work even without the migration. However, fraud detection features won't be available until you run the migration.

## What Changed

The code now:
- ✅ Gracefully handles missing `photo_hash` and `face_encoding` columns
- ✅ Gracefully handles missing `photo_matches` table
- ✅ Continues working even if fraud detection isn't set up
- ✅ Shows appropriate messages when fraud detection features aren't available

## After Migration

Once you run the migration:
1. The app will automatically start using fraud detection
2. Photo hashes will be calculated on new submissions
3. Duplicate detection will work
4. Review interface will be available

## Testing

After deployment, check:
1. Can you submit attendance? ✅
2. Can you view attendance? ✅
3. Do you see any fraud detection alerts? (Only if migration is run)

The app should work normally even without the migration - fraud detection just won't be active.

