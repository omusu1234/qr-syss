# Setup Instructions

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database

Edit `config.py` and update the database connection settings:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/qr_attendance'
```

For multiple database synchronization, update the `DATABASE_SERVERS` list.

### 3. Create MySQL Database

```sql
CREATE DATABASE qr_attendance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Initialize Database Schema

```bash
python setup_database.py
```

This will:
- Create all necessary tables
- Create default admin user (username: `admin`, password: `admin123`)

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## First Steps After Setup

1. **Login as Admin**:
   - Username: `admin`
   - Password: `admin123`
   - Role: Admin

2. **Change Admin Password** (Important for security!)

3. **Create Lecturers**:
   - Go to Admin Dashboard
   - Click "Manage Lecturers"
   - Add lecturer accounts

4. **Create Units**:
   - Go to Admin Dashboard
   - Click "Manage Units"
   - Add courses/units and assign to lecturers

5. **Test QR Code Generation**:
   - Login as a lecturer
   - Create a new session
   - Generate QR code
   - Test scanning with a mobile device

## Configuration Options

Edit `config.py` to customize:

- **QR_CODE_EXPIRY_MINUTES**: Default is 120 minutes (2 hours)
- **LECTURE_HALL_RADIUS**: Default is 100 meters
- **DATABASE_SERVERS**: Configure multiple MySQL servers for sync

## Troubleshooting

### Database Connection Errors
- Ensure MySQL server is running
- Verify credentials in `config.py`
- Check that the database exists

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)

### Location Access Issues
- Students must allow location access in their browsers
- Ensure GPS is enabled on mobile devices
- Check that coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)



