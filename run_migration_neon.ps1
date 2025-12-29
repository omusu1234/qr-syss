# PowerShell script to add photo_data column to Neon PostgreSQL database
# Run this script in PowerShell

$connectionString = "postgresql://neondb_owner:npg_W9nEdeIrBN6y@ep-lingering-grass-aeb3wt2q-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require"

Write-Host "Connecting to Neon database..." -ForegroundColor Cyan
Write-Host "Adding photo_data column to attendances table..." -ForegroundColor Yellow

# Run the migration SQL
$sqlCommand = "ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT;"

# Execute using psql
$psqlCommand = "psql `"$connectionString`" -c `"$sqlCommand`""

Write-Host "Executing: $psqlCommand" -ForegroundColor Gray
Invoke-Expression $psqlCommand

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Successfully added photo_data column to attendances table!" -ForegroundColor Green
    Write-Host "The photo capture feature is now ready to use." -ForegroundColor Green
} else {
    Write-Host "`n✗ Error running migration. Please check:" -ForegroundColor Red
    Write-Host "  1. psql is installed and in your PATH" -ForegroundColor Yellow
    Write-Host "  2. You have network access to Neon database" -ForegroundColor Yellow
    Write-Host "  3. Database credentials are correct" -ForegroundColor Yellow
    Write-Host "`nYou can also run the SQL manually:" -ForegroundColor Cyan
    Write-Host "  psql `"$connectionString`"" -ForegroundColor Gray
    Write-Host "  Then run: ALTER TABLE attendances ADD COLUMN IF NOT EXISTS photo_data TEXT;" -ForegroundColor Gray
}

