# QR Code Class Attendance System

A comprehensive QR code-based attendance system for educational institutions with automatic database synchronization across multiple MySQL servers.

## Features

1. **QR Code Generation**: Lecturers can generate unique QR codes for each lecture session, automatically linked to their unit/course
2. **Student Attendance**: Students scan QR codes with their phones and submit attendance via a web form
3. **Location Verification**: Attendance submission only works within a specified radius of the lecture hall
4. **Automatic Expiration**: QR codes expire after a configurable time period
5. **Multi-Database Sync**: Data is automatically synchronized across three local MySQL servers
6. **Role-Based Access**: 
   - Lecturers can only see attendance for their assigned units
   - Admin can manage lecturers and units
7. **Secure Authentication**: Login system with role selection (Lecturer or Admin)

## Requirements

- Python 3.8+
- MySQL Server (primary)
- MySQL Server instances (for sync - optional, can use same server)
- Modern web browser
- Mobile device with camera for QR code scanning

## Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL databases**:
   - Create a database named `qr_attendance` on your primary MySQL server
   - Optionally set up 2 additional MySQL servers for synchronization
   - Update database credentials in `config.py` or use environment variables

4. **Configure environment variables** (optional):
   ```bash
   export SECRET_KEY='your-secret-key-here'
   export DATABASE_URL='mysql+pymysql://user:password@localhost/qr_attendance'
   export DB_HOST_1='localhost'
   export DB_USER_1='root'
   export DB_PASSWORD_1='password'
   export DB_NAME_1='qr_attendance'
   # ... repeat for DB_HOST_2, DB_HOST_3, etc.
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   - Open your browser and go to `http://localhost:5002`
   - Default admin credentials:
     - Username: `admin`
     - Password: `admin123`
     - **⚠️ IMPORTANT: Change the default admin password in production!**

## Configuration

Edit `config.py` to customize:

- **QR_CODE_EXPIRY_MINUTES**: How long QR codes remain valid (default: 120 minutes)
- **LECTURE_HALL_RADIUS**: Maximum distance in meters for attendance submission (default: 100 meters)
- **DATABASE_SERVERS**: List of MySQL servers for synchronization

## Usage Guide

### For Administrators

1. **Login** as Admin
2. **Manage Lecturers**:
   - Click "Manage Lecturers"
   - Add new lecturers with username, email, password, full name, and employee ID
3. **Manage Units**:
   - Click "Manage Units"
   - Add new units/courses and assign them to lecturers

### For Lecturers

1. **Login** as Lecturer
2. **Create QR Session**:
   - Click "Create Session"
   - Select a unit/course
   - Enter session name
   - Set lecture hall location (use "Use Current Location" button)
   - Generate QR code
3. **View Attendance**:
   - Click on any session to view attendance records
   - See all students who submitted attendance

### For Students

1. **Scan QR Code**: Use your phone's camera or QR scanner app
2. **Submit Attendance**:
   - Allow location access when prompted
   - Enter your admission number and full name
   - Click "Submit Attendance"
   - System verifies you're within the lecture hall radius

## Database Schema

The system uses the following main tables:

- **users**: User accounts (lecturers and admins)
- **lecturers**: Lecturer information
- **units**: Course/unit information
- **lecture_sessions**: QR code sessions with expiration
- **attendances**: Student attendance records

## Database Synchronization

The system automatically syncs attendance and session data to multiple MySQL servers configured in `config.py`. This ensures data redundancy and availability.

## Security Notes

- Change the default admin password immediately
- Use strong SECRET_KEY in production
- Configure proper MySQL user permissions
- Use HTTPS in production
- Regularly backup your databases

## Troubleshooting

### Location permission issues
- Ensure students allow location access in their browsers
- Check that the device has GPS enabled
- Verify the lecture hall coordinates are correct

### Database connection errors
- Verify MySQL server is running
- Check database credentials in config.py
- Ensure databases exist on all configured servers

### QR code not scanning
- Ensure the QR code image is displayed clearly
- Check that the generated URL is accessible
- Verify the QR code hasn't expired

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please check:
- Database connection settings
- Python version compatibility
- MySQL server status
- Browser console for JavaScript errors

