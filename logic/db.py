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

    def _migrate_database(self):
        """Apply any needed database migrations"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # 1. Check and update spares table
            cursor.execute("PRAGMA table_info(spares)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]  # Column name is at index 1

            # Add missing columns to spares
            if "notes" not in column_names:
                print("🔄 Adding missing column: notes to spares table")
                cursor.execute("ALTER TABLE spares ADD COLUMN notes TEXT")

            # 2. Check and update movements table for borrower_name
            cursor.execute("PRAGMA table_info(movements)")
            movements_columns = cursor.fetchall()
            movements_column_names = [col[1] for col in movements_columns]

            # Add borrower_name if missing
            if "borrower_name" not in movements_column_names:
                print("🔄 Adding missing column: borrower_name to movements table")
                cursor.execute("ALTER TABLE movements ADD COLUMN borrower_name TEXT")

                # Optional: Backfill existing borrow records
                try:
                    cursor.execute(
                        """
                    UPDATE movements 
                    SET borrower_name = 
                        CASE 
                            WHEN movement_type = 'borrow' AND notes LIKE '%Borrowed by%' THEN
                                TRIM(SUBSTR(notes, INSTR(notes, 'Borrowed by') + 12))
                            WHEN movement_type = 'borrow' AND notes LIKE '%borrowed by%' THEN
                                TRIM(SUBSTR(notes, INSTR(notes, 'borrowed by') + 12))
                            ELSE NULL
                        END
                    """
                    )
                    updated = cursor.rowcount
                    print(
                        f"✅ Backfilled borrower names for {updated} existing borrow records"
                    )
                except Exception as backfill_error:
                    print(f"⚠️ Could not backfill borrower names: {backfill_error}")

            # 3. Also check for any other missing columns we might need
            # Add returned_quantity if missing (for backward compatibility)
            if "returned_quantity" not in movements_column_names:
                print("🔄 Adding missing column: returned_quantity to movements table")
                cursor.execute(
                    "ALTER TABLE movements ADD COLUMN returned_quantity INTEGER DEFAULT 0"
                )

            # Add return_date if missing
            if "return_date" not in movements_column_names:
                print("🔄 Adding missing column: return_date to movements table")
                cursor.execute("ALTER TABLE movements ADD COLUMN return_date TIMESTAMP")

            conn.commit()
            print("✅ Database migration complete")

        except Exception as e:
            # This might be normal if tables don't exist yet (first run)
            # The tables will be created with correct schema in setup_tables()
            print(f"⚠️ Migration error (may be normal if tables don't exist yet): {e}")
            conn.rollback()
        finally:
            conn.close()

    # setup database method:
    def _setup_database(self):
        """Create database and tables if they don't exist"""
        # Check if database file exists AND has tables
        if not self.db_path.exists():
            print("📦 Creating new database...")
            self._create_tables()
        else:
            # Check if tables exist in the file
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT  FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                conn.close()

                if len(tables) == 0:
                    print(
                        "📦 Database file exists but has no tables. Creating tables..."
                    )
                    self._create_tables()
                else:
                    print(f"✅ Database ready with {len(tables)} tables")
            except sqlite3.Error as e:
                # If any error, recreate tables
                print("⚠️  Database file may be corrupt. Recreating tables...")
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
        self._migrate_database()
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
                "SELECT id FROM users WHERE username = ?", (user_name,), fetch=True
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
