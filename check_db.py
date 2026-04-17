import sqlite3

conn = sqlite3.connect("alis.db")
cursor = conn.cursor()

print("📂 Sessions:")
cursor.execute("SELECT * FROM sessions")
print(cursor.fetchall())

print("\n📊 Responses:")
cursor.execute("SELECT * FROM responses")
print(cursor.fetchall())

conn.close()
