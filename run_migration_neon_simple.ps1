# Simple PowerShell one-liner to add photo_data column
# Copy and paste this entire command in PowerShell

psql "postgresql://neondb_owner:npg_W9nEdeIrBN6y@ep-lingering-grass-aeb3wt2q-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require" -c "ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT;"



