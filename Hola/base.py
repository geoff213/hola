from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conexion = sqlite3.connect('tu_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conexion.close()
    return render_template('otra.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
