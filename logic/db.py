# database/setup.py
import sqlite3
import os
from pathlib import Path


class DatabaseSetup:
    def __init__(self, db_path="data/inventory.db"):
        self.db_path = Path(db_path)
        self.sql_folder = Path("sql")

        # Create directories if they don't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.sql_folder.mkdir(exist_ok=True)

    def execute_sql_file(self, sql_file):
        """Execute a single SQL file"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        try:
            with open(sql_file, "r") as f:
                sql = f.read()

            cursor.executescript(sql)
            conn.commit()
            print(f"✅ Executed: {sql_file.name}")

        except Exception as e:
            print(f"❌ Error in {sql_file.name}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_database(self):
        """Initialize database by running all SQL files"""
        print(f"📦 Initializing database at: {self.db_path}")

        # Check if SQL files exist
        sql_files = list(self.sql_folder.glob("*.sql"))
        if not sql_files:
            print("⚠️  No SQL files found in 'sql/' folder")
            return False

        # Execute each SQL file in order
        for sql_file in sorted(sql_files):
            self.execute_sql_file(sql_file)

        # Verify tables were created
        self._verify_tables()

        print(f"🎉 Database ready! Location: {self.db_path}")
        return True

    def _verify_tables(self):
        """Check that all tables were created"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """
        )

        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tables created: {', '.join(tables)}")

        # Count records in each table
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} records")

        conn.close()

    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(str(self.db_path))


# Create a global instance
db_setup = DatabaseSetup()

if __name__ == "__main__":
    # Run when executed directly
    success = db_setup.init_database()

    if success:
        print("\n🚀 Database setup complete!")
        print("👉 Next: Add some test data or start building your UI!")
    else:
        print("\n❌ Database setup failed!")
