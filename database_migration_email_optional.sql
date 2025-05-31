-- Migration script to remove email and username columns
-- Run this script if you have existing data in the database

-- Drop email and username columns from users table
ALTER TABLE users DROP COLUMN IF EXISTS email;
ALTER TABLE users DROP COLUMN IF EXISTS username;

-- Verify the changes
\d users;
