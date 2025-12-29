# Fraud Detection System

## Overview

The fraud detection system helps lecturers identify when one person is signing attendance for multiple students by analyzing photos submitted during attendance.

## Features

### 1. Duplicate Photo Detection (Always Available)
- Uses perceptual hashing to detect exact or near-duplicate photos
- Fast and lightweight - works on all platforms
- No special dependencies required

### 2. Face Similarity Matching (Optional)
- Uses face recognition to detect similar faces across different submissions
- Requires `dlib` and `face-recognition` libraries
- More accurate but requires system dependencies

## Installation

### Basic Installation (Duplicate Detection Only)

The basic installation works on all platforms including Vercel, Render, etc.:

```bash
pip install -r requirements.txt
```

This will install:
- `imagehash` - for duplicate photo detection
- `numpy` - for image processing

### Full Installation (With Face Recognition)

For face recognition, you need to install system dependencies first:

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
pip install dlib==19.24.2
pip install face-recognition==1.3.0
```

**On macOS:**
```bash
brew install cmake
pip install dlib==19.24.2
pip install face-recognition==1.3.0
```

**Note:** Face recognition is **not recommended** for serverless platforms (Vercel, Netlify, etc.) due to build complexity.

## How It Works

### On Attendance Submission

1. **Photo Hash Calculation**: Creates a perceptual hash of the submitted photo
2. **Face Encoding Extraction** (if available): Extracts face encoding for similarity matching
3. **Comparison**: Compares against all existing photos in the session
4. **Match Detection**: Creates `PhotoMatch` records for:
   - Duplicate photos (exact or near-exact matches)
   - Similar faces (85%+ similarity if face recognition is available)

### In Attendance View

- Shows alert banner if unverified matches are detected
- Highlights rows with fraud indicators
- Displays match type badges (Duplicate/Similar Face)

### Review Interface

Lecturers can:
- View side-by-side photo comparisons
- Verify matches as fraud or dismiss as false positives
- Add notes for documentation
- Track verification history

## Database Migration

Run the migration script to add required columns and tables:

```sql
-- PostgreSQL
\i add_fraud_detection_migration.sql

-- Or manually:
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_hash VARCHAR(64);
ALTER TABLE attendances ADD COLUMN IF NOT EXISTS face_encoding TEXT;
-- ... (see migration file for full SQL)
```

## Configuration

### Similarity Thresholds

In `photo_analysis.py`, you can adjust:

- **Duplicate Detection**: Hash threshold (default: 5)
  ```python
  compare_photo_hashes(hash1, hash2, threshold=5)  # Lower = stricter
  ```

- **Face Similarity**: Similarity threshold (default: 0.85 = 85%)
  ```python
  if similarity and similarity >= 0.85:  # Higher = stricter
  ```

## Troubleshooting

### Face Recognition Not Working

If you see warnings about face recognition not being available:

1. **Check if libraries are installed:**
   ```python
   python -c "import face_recognition; print('OK')"
   ```

2. **If not installed**, the system will still work with duplicate detection only

3. **For serverless platforms**, face recognition is intentionally disabled due to build complexity

### Performance Considerations

- **Duplicate Detection**: Very fast, suitable for real-time use
- **Face Recognition**: Slower, may add 1-3 seconds per submission
- **Batch Processing**: For large sessions, consider processing matches asynchronously

## Limitations

1. **Face Recognition**: 
   - Requires good lighting and clear face visibility
   - May have false positives with similar-looking people
   - Not available on all deployment platforms

2. **Duplicate Detection**:
   - May miss photos that are similar but not identical
   - Works best with exact duplicates

3. **Privacy**:
   - Photos are stored in the database
   - Face encodings are stored (not raw biometrics)
   - Consider GDPR/privacy regulations in your region

## Best Practices

1. **Review All Matches**: Don't rely solely on automated detection
2. **Use Notes**: Document why matches were confirmed or dismissed
3. **Regular Reviews**: Check matches regularly, not just at session end
4. **Combine with Other Checks**: Use IP address, time patterns, and location data together

## Support

If you encounter issues:

1. Check that `imagehash` is installed (for duplicate detection)
2. Verify database migration was run successfully
3. Check application logs for error messages
4. Ensure photos are being captured and stored correctly

