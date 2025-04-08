import sqlite3

# Connect to the database
conn = sqlite3.connect("quiz_bowl.db")
cursor = conn.cursor()

# Get all user-defined tables (excluding SQLite internal ones)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

# Print each table name and its contents
for (table_name,) in tables:
    print(f"\n--- Contents of '{table_name}' ---")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("(No data found)")

# Close the connection
conn.close()
