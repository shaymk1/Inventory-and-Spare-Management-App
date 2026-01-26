# logic/db.py
# logic/database.py
import sqlite3
import os
from pathlib import Path


class Database:
    def __init__(self, db_path=None):
        """
        Initialize database connection
        """
        if db_path is None:
            # Default path: project_root/data/inventory.db
            self.base_dir = Path(__file__).parent.parent
            self.db_path = self.base_dir / "data" / "inventory.db"
        else:
            self.db_path = Path(db_path)

        # Create data directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize on first use
        self._setup_database()

    def _setup_database(self):
        """Create database and tables if they don't exist"""
        if not self.db_path.exists():
            print("📦 Creating new database...")
            self._create_tables()

    def _create_tables(self):
        """Read and execute all SQL files from sql/ folder"""
        sql_dir = self.base_dir / "sql"

        if not sql_dir.exists():
            raise FileNotFoundError(f"SQL folder not found: {sql_dir}")

        conn = self.get_connection()
        cursor = conn.cursor()

        # Execute all SQL files
        sql_files = list(sql_dir.glob("*.sql"))
        for sql_file in sorted(sql_files):
            print(f"  Creating tables from: {sql_file.name}")
            with open(sql_file, "r") as f:
                sql = f.read()
            cursor.executescript(sql)

        conn.commit()
        conn.close()
        print("✅ Database tables created")

    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(str(self.db_path))
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute(self, query, params=None, fetch=False):
        """
        Execute a SQL query

        Args:
            query: SQL query string
            params: Parameters for the query (prevents SQL injection)
            fetch: If True, fetch and return results

        Returns:
            List of results if fetch=True, otherwise None
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                results = cursor.fetchall()
                # Convert to list of dictionaries
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in results]
            else:
                conn.commit()
                return None

        except Exception as e:
            print(f"❌ Database error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    # Helper methods for common operations
    def get_all_spares(self):
        """Get all spare parts"""
        return self.execute("SELECT * FROM spares ORDER BY code", fetch=True)

    def add_spare(self, code, name, quantity=0, low_threshold=5):
        """Add a new spare part"""
        return self.execute(
            "INSERT INTO spares (code, name, quantity, low_stock_threshold) VALUES (?, ?, ?, ?)",
            (code, name, quantity, low_threshold),
        )

    def borrow_spare(self, spare_id, user_name, quantity, notes=""):
        """Borrow spare parts"""
        # First, get or create user
        user = self.execute(
            "SELECT id FROM users WHERE name = ?", (user_name,), fetch=True
        )

        if not user:
            # Create new user
            self.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
            user = self.execute(
                "SELECT id FROM users WHERE name = ?", (user_name,), fetch=True
            )

        user_id = user[0]["id"]

        # Record movement
        return self.execute(
            """
            INSERT INTO movements (spare_id, user_id, quantity, movement_type, notes)
            VALUES (?, ?, ?, 'borrow', ?)
            """,
            (spare_id, user_id, quantity, notes),
        )


# Create a global instance for easy access
db = Database()
