


-- sql/movements.sql
CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spare_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    movement_type TEXT NOT NULL CHECK (movement_type IN ('borrow', 'return')),
    notes TEXT,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_quantity INTEGER DEFAULT 0 CHECK (returned_quantity >= 0),
    return_date TIMESTAMP,
    FOREIGN KEY (spare_id) REFERENCES spares(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_movements_date ON movements(movement_date);
CREATE INDEX IF NOT EXISTS idx_movements_spare ON movements(spare_id);
CREATE INDEX IF NOT EXISTS idx_movements_user ON movements(user_id);
CREATE INDEX IF NOT EXISTS idx_movements_returned ON movements(movement_type, returned_quantity) 
WHERE movement_type = 'borrow' AND returned_quantity = 0;