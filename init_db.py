import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup TEXT,
    delivery TEXT,
    weight REAL,
    status TEXT,
    amount REAL,
    payment TEXT
)''')
c.execute("INSERT INTO shipments (pickup, delivery, weight, status, amount, payment) VALUES (?, ?, ?, ?, ?, ?)",
          ('Kurla', 'Ghatkopar', 10.0, 'Pending', 100.0, 'Unpaid'))
conn.commit()
conn.close()
