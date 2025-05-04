-- migration: drop_is_active_from_users

ALTER TABLE users
DROP COLUMN IF EXISTS is_active;