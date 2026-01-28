-- sql/users.sql - SIMPLIFIED
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    is_developer INTEGER NOT NULL DEFAULT 0 CHECK (is_developer IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Insert real users
INSERT OR IGNORE INTO users (username, password_hash, full_name, is_developer) VALUES
    -- Developer (you) - emergency only
    ('dev_admin', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'System Developer', 1),
    
    -- Store Manager (daily user)
    ('store_manager', 'd1b1294f6b0b7c7c5e5c5c5a5b5c5d5e5f5a5b5c5d5e5f5a5b5c5d5e5f5a5b5c5d', 'Barend', 0),
    
    -- Boss (backup when store manager is off)
    ('boss_backup', 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'Attie', 0);
