-- Add AI-generated categorization columns to support_tickets

ALTER TABLE support_tickets 
ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'General';

ALTER TABLE support_tickets 
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'Medium';
