# test_setup.py
# logic/test_db.py
"""
Test database functionality
"""
from .db import db


def test_database():
    print("🧪 Testing database setup...")
    print("=" * 50)

    # Test 1: Check tables exist
    print("\n1. Checking database structure...")
    tables = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", fetch=True
    )

    print(f"   Found {len(tables)} tables:")
    for table in tables:
        print(f"   - {table['name']}")

    # Test 2: Check ALL users
    print("\n2. Checking all users...")
    all_users = db.execute(
        "SELECT username, full_name, is_developer FROM users ORDER BY is_developer DESC, username",
        fetch=True,
    )

    print(f"   Found {len(all_users)} users:")
    for user in all_users:
        role = "👨‍💻 Developer" if user["is_developer"] else "👷 User"
        print(f"   {role}: {user['username']} ({user['full_name']})")

    # Test 3: Add a test spare
    print("\n3. Testing spare insertion...")
    try:
        db.add_spare("TEST-001", "Test Bolt", 100, 10)  # ← FIXED: 4 arguments
        print("   ✅ Test spare added successfully")
    except Exception as e:
        print(f"   ⚠️  Could not add test spare: {e}")

    # Test 4: List all spares
    print("\n4. Listing all spares...")
    spares = db.get_all_spares()
    print(f"   Found {len(spares)} spares:")
    for spare in spares[:5]:
        print(f"   - {spare['code']}: {spare['name']} (Qty: {spare['quantity']})")

    if len(spares) > 5:
        print(f"   ... and {len(spares) - 5} more")

    print("\n🎉 Database tests complete!")
    print(f"📁 Database location: {db.db_path}")
    return True


# # logic/test_db.py - UPDATED
# def test_database():
#     print("🧪 Testing database setup...")
#     print("=" * 50)

#     # Test 1: Check tables exist
#     print("\n1. Checking database structure...")
#     tables = db.execute(
#         "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", fetch=True
#     )

#     print(f"   Found {len(tables)} tables:")
#     for table in tables:
#         print(f"   - {table['name']}")

#     # Test 2: Check default admin - UPDATED QUERY!
#     print("\n2. Checking default users...")

#     # users = db.execute(
#     #     "SELECT username, full_name, is_developer FROM users", fetch=True
#     # )
#     admin = db.execute(
#         "SELECT username, full_name, is_developer FROM users WHERE is_developer = 1",
#         fetch=True,
#     )

#     print(f"   Found {len(users)} users:")
#     for user in users:
#         role = "Developer" if user["is_developer"] else "User"
#         print(f"   - {user['username']} ({user['full_name']}) - {role}")

#     # Test 3: Add a test spare
#     print("\n3. Testing spare insertion...")
#     try:
#         db.add_spare("TEST-001", "Test Bolt", 100, 10)
#         print("   ✅ Test spare added successfully")
#     except Exception as e:
#         print(f"   ⚠️  Could not add test spare (maybe already exists): {e}")

#     # Test 4: List all spares
#     print("\n4. Listing all spares...")
#     spares = db.get_all_spares()
#     print(f"   Found {len(spares)} spares:")
#     for spare in spares[:5]:  # Show first 5
#         print(f"   - {spare['code']}: {spare['name']} (Qty: {spare['quantity']})")

#     if len(spares) > 5:
#         print(f"   ... and {len(spares) - 5} more")

#     print("\n🎉 Database tests complete!")
#     print(f"📁 Database location: {db.db_path}")
#     return True


# def test_database():
#     print("🧪 Testing database setup...")
#     print("=" * 50)

#     # Test 1: Check tables exist
#     print("\n1. Checking database structure...")
#     tables = db.execute(
#         "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", fetch=True
#     )

#     print(f"   Found {len(tables)} tables:")
#     for table in tables:
#         print(f"   - {table['name']}")

#     # Test 2: Check default admin
#     print("\n2. Checking default admin user...")
#     admin = db.execute(
#         "SELECT name, is_admin FROM users WHERE is_admin = 1", fetch=True
#     )

#     if admin:
#         print(f"   ✅ Admin user: {admin[0]['name']}")
#     else:
#         print("   ⚠️  No admin user found (this is OK if you didn't add one)")

#     # Test 3: Add a test spare
#     print("\n3. Testing spare insertion...")
#     try:
#         db.add_spare("TEST-001", "Test Bolt", 100, 10)
#         print("   ✅ Test spare added successfully")
#     except Exception as e:
#         print(f"   ⚠️  Could not add test spare (maybe already exists): {e}")

#     # Test 4: List all spares
#     print("\n4. Listing all spares...")
#     spares = db.get_all_spares()
#     print(f"   Found {len(spares)} spares:")
#     for spare in spares[:5]:  # Show first 5
#         print(f"- {spare['code']}: {spare['name']} (Qty: {spare['quantity']})")

#     if len(spares) > 5:
#         print(f"   ... and {len(spares) - 5} more")

#     print("\n🎉 Database tests complete!")
#     print(f"📁 Database location: {db.db_path}")
#     return True


# if __name__ == "__main__":
#     test_database()
