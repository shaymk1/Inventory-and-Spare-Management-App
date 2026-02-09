# test_migration.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.db import db

# Force migration
print("Testing database migration...")
db._migrate_database()

# Check result
conn = db.get_connection()
cursor = conn.cursor()

# Check movements table columns
cursor.execute("PRAGMA table_info(movements)")
columns = cursor.fetchall()

print("\nCurrent movements table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check if borrower_name exists
column_names = [col[1] for col in columns]
if "borrower_name" in column_names:
    print("\n✅ SUCCESS: borrower_name column is present!")

    # Check some sample data
    cursor.execute("SELECT COUNT(*) as total FROM movements")
    total = cursor.fetchone()[0]
    print(f"Total movements: {total}")

    cursor.execute(
        "SELECT COUNT(*) as with_name FROM movements WHERE borrower_name IS NOT NULL"
    )
    with_name = cursor.fetchone()[0]
    print(f"Movements with borrower name: {with_name}")

else:
    print("\n❌ FAILED: borrower_name column is missing!")

conn.close()
