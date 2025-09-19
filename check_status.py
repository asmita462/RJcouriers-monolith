import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT id, status FROM shipments WHERE id = 4")
result = c.fetchone()
print("Shipment Status:", result)
conn.close()
