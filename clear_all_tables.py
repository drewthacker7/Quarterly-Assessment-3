import sqlite3

# Connect to the quiz bowl database
conn = sqlite3.connect("quiz_bowl.db")
cursor = conn.cursor()

# List of tables to clear
tables = [
    "python",
    "intermediate_accounting",
    "audit",
    "federal_taxation",
    "digital_forensics"
]

# Delete all rows from each table
for table in tables:
    cursor.execute(f"DELETE FROM {table}")
    print(f"Cleared table: {table}")

# Commit and close
conn.commit()
conn.close()
print("All tables cleared.")
