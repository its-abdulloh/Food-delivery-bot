import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


cursor.execute("DELETE FROM users;")
cursor.execute("DELETE FROM orders;")
cursor.execute("DELETE FROM sqlite_sequence;")
cursor.execute("DELETE FROM menu;")

conn.commit()
conn.close()