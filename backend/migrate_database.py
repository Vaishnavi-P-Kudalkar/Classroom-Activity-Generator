import sqlite3
import os

def migrate_database():
    # Path to your database
    db_path = os.path.abspath("database.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Try to add grade column
        cursor.execute("ALTER TABLE activities ADD COLUMN grade TEXT")
    except sqlite3.OperationalError:
        print("Grade column might already exist")

    try:
        # Try to add board column
        cursor.execute("ALTER TABLE activities ADD COLUMN board TEXT")
    except sqlite3.OperationalError:
        print("Board column might already exist")

    # If no columns exist, recreate the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS new_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        grade TEXT NOT NULL,
        board TEXT NOT NULL,
        activity TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Copy existing data to new table (if any)
    cursor.execute('''
    INSERT INTO new_activities (topic, grade, board, activity, timestamp)
    SELECT topic, 
           COALESCE(grade, '5') as grade, 
           COALESCE(board, 'CBSE') as board, 
           activity, 
           timestamp 
    FROM activities
    ''')

    # Drop old table
    cursor.execute("DROP TABLE IF EXISTS activities")

    # Rename new table to activities
    cursor.execute("ALTER TABLE new_activities RENAME TO activities")

    # Commit changes
    conn.commit()
    conn.close()

    print("Database migration completed successfully!")

# Run the migration
if __name__ == "__main__":
    migrate_database()