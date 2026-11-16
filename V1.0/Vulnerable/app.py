from flask import Flask, templates, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES ('Playstation 5 Edition', 1500.0, 5)")
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES ('Pasta con arroz', 4.0, 10)")
        conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    busqueda = request.args.get('q', '')
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    
    # Consulta vulnerable a propósito para tus pruebas de Inyección SQL más adelante
    query = f"SELECT * FROM productos WHERE nombre LIKE '%{busqueda}%'"
    cursor.execute(query)
    
    productos = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', productos=productos, busqueda=busqueda)

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
