-- car_images table was created before is_primary was added to
-- database.py's initialize_database(). CREATE TABLE IF NOT EXISTS
-- does not retroactively add new columns, so this had to be patched
-- in manually.
ALTER TABLE car_images ADD COLUMN IF NOT EXISTS is_primary BOOLEAN DEFAULT FALSE;
