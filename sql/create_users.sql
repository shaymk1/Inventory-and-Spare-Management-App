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
    -- Developer (simple password)
    ('dev_admin', 'dev123', 'Developer Admin', 1),
    
    -- Store Manager (simple password)  
    ('store_manager', 'store123', 'Store Manager', 0),
    
    -- Boss (simple password)
    ('boss_backup', 'boss123', 'Backup Supervisor', 0);