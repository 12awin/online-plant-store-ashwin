from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder="project plantation") 

# Database Initialization
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            address TEXT NOT NULL,
                            fuel_type TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            total_price REAL NOT NULL,
                            payment_method TEXT NOT NULL)''')

        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
                ("banana tree", 8),
                ("neem tree", 9),
                ("mango tree", 12)
            ])
        conn.commit()

@app.route('/')
def home():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return render_template('products.html', products=products)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        plant_type = request.form['plant_type']
        quantity = int(request.form['quantity'])
        payment_method = request.form['payment_method']

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM products WHERE name=?", (plant_type))
            price = cursor.fetchone()[0]
            total_price = price * quantity

            cursor.execute("INSERT INTO orders (name, address, fuel_type, quantity, total_price, payment_method) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, address, plant_type, quantity, total_price, payment_method))
            conn.commit()
        
        return redirect(url_for('home'))
    
    return render_template('order.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)