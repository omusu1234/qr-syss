# PostgreSQL Migration Guide

## Files Created
1. `postgresql_schema.sql` - Creates all tables
2. `postgresql_sample_data.sql` - Inserts sample data

## Steps to Migrate

### 1. Create PostgreSQL Database on Render
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name it (e.g., `qr-attendance-db`)
4. Create the database
5. Copy the **Internal Database URL** (you'll need this)

### 2. Run the SQL Scripts

#### Option A: Using Render's PostgreSQL Dashboard
1. Go to your PostgreSQL database in Render
2. Click on "Connect" or "Query"
3. Open the PostgreSQL web interface
4. Copy and paste the contents of `postgresql_schema.sql`
5. Run it
6. Then copy and paste the contents of `postgresql_sample_data.sql`
7. Run it

#### Option B: Using psql (Command Line)
```bash
# Connect to your Render PostgreSQL database
psql "your-render-postgresql-connection-string"

# Then run:
\i postgresql_schema.sql
\i postgresql_sample_data.sql
```

#### Option C: Using pgAdmin or DBeaver
1. Connect to your Render PostgreSQL database
2. Open SQL query window
3. Copy and paste `postgresql_schema.sql` → Execute
4. Copy and paste `postgresql_sample_data.sql` → Execute

### 3. Update Your Application Configuration

Update `config.py` to use PostgreSQL:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://user:password@hostname:5432/database_name'
```

**Important:** Change `mysql+pymysql://` to `postgresql://` or `postgresql+psycopg2://`

### 4. Update requirements.txt

Add PostgreSQL driver:
```
psycopg2-binary==2.9.9
```

Or if you already have it, make sure it's there.

### 5. Set Environment Variable in Render

In your Render Web Service:
- Go to "Environment" tab
- Add/Update `DATABASE_URL`:
  - Key: `DATABASE_URL`
  - Value: Your Render PostgreSQL Internal Database URL (from step 1)

### 6. Redeploy

Render will automatically redeploy when you save the environment variable.

## Sample Data Included

After running the scripts, you'll have:

### Users:
- **Admin**: username=`admin`, password=`admin123`
- **Lecturer 1**: username=`lecturer1`, password=`lecturer123`
- **Lecturer 2**: username=`lecturer2`, password=`lecturer123`
- **Lecturer 3**: username=`lecturer3`, password=`lecturer123`

### Departments:
- Computer Science (CS)
- Mathematics (MATH)
- Physics (PHY)

### Units:
- CS101 - Introduction to Computer Science
- CS201 - Data Structures and Algorithms
- MATH101 - Calculus I
- MATH201 - Linear Algebra
- PHY101 - Physics Fundamentals

### Lecture Sessions:
- 4 sample sessions (1 past, 3 active)

### Attendance Records:
- 12 sample attendance records

## Notes

- All password hashes are properly generated using Werkzeug
- Timestamps use PostgreSQL's `CURRENT_TIMESTAMP`
- Foreign key constraints are properly set up
- Indexes are created for performance
- All relationships are maintained

## Troubleshooting

If you get errors:
1. Make sure you run `postgresql_schema.sql` FIRST
2. Then run `postgresql_sample_data.sql`
3. Check that your `DATABASE_URL` in Render is correct
4. Ensure `psycopg2-binary` is in `requirements.txt`

