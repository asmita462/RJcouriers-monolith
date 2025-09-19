from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
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
    conn.commit()
    conn.close()

init_db()

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

# View all shipments
@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM shipments")
    shipments = c.fetchall()
    conn.close()
    return render_template('view.html', shipments=shipments)

# Create a new shipment
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        pickup = request.form['pickup']
        delivery = request.form['delivery']
        weight = float(request.form['weight'])
        status = 'Pending'
        amount = 0.0
        payment = 'Unpaid'

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO shipments (pickup, delivery, weight, status, amount, payment)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (pickup, delivery, weight, status, amount, payment))
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('create.html')

# Track a shipment
@app.route('/track', methods=['GET', 'POST'])
def track():
    result = None
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM shipments WHERE id = ?", (track_id,))
        result = c.fetchone()
        conn.close()
    return render_template('track.html', result=result)

# Update delivery status
@app.route('/update-status', methods=['GET', 'POST'])
def update_status():
    updated = None
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        new_status = request.form.get('status')

        if not track_id or not new_status:
            return render_template('update.html', updated=None)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE shipments SET status = ? WHERE id = ?", (new_status, track_id))
        conn.commit()
        c.execute("SELECT * FROM shipments WHERE id = ?", (track_id,))
        updated = c.fetchone()
        conn.close()
    return render_template('update.html', updated=updated)

# Make a payment
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    paid = None
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        amount = request.form.get('amount')
        method = request.form.get('method')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE shipments SET amount = ?, payment = ? WHERE id = ?",
                  (amount, method, track_id))
        conn.commit()
        c.execute("SELECT * FROM shipments WHERE id = ?", (track_id,))
        paid = c.fetchone()
        conn.close()
    return render_template('payment.html', paid=paid)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
