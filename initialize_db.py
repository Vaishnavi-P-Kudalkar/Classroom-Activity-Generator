import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Check if the activities table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities';")
table_exists = cursor.fetchone()

if table_exists:
    print("✅ Table 'activities' exists!")
else:
    print("❌ Table 'activities' does NOT exist! Creating it now...")

    # Create the table
    cursor.execute("""
        CREATE TABLE activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            description TEXT NOT NULL
        );
    """)
    conn.commit()
    print("✅ Table 'activities' created successfully!")

conn.close()
