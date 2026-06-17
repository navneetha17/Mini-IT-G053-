import sqlite3

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE user ADD COLUMN last_login DATETIME")

conn.commit()
conn.close()

print("Database updated successfully!")