-- Manual SQL to change contact_person from enum to text
-- Run this directly in your PostgreSQL database

-- Step 1: Alter the column type from enum to text
ALTER TABLE users ALTER COLUMN contact_person TYPE TEXT;

-- Step 2 (Optional): Drop the enum type if not used elsewhere
-- Uncomment if you want to fully remove the enum type
-- DROP TYPE contact_person_enum;

-- Note: Existing data will be preserved (enum values like 's', 'd', 'm', 'b' will become text)
