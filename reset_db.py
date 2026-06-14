import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()


cursor.execute("DELETE FROM users;")
cursor.execute("DELETE FROM orders;")
cursor.execute("DELETE FROM sqlite_sequence;")

conn.commit()
conn.close()