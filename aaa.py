from tkinter import *
from tkinter import messagebox, simpledialog
from datetime import datetime
import sqlite3

class Producto:
    def __init__(self, id, cantidad, nombre, precio):
        self.id = id
        self.cantidad = cantidad
        self.nombre = nombre
        self.precio = precio

class Venta:
    def __init__(self, id, id_producto, cantidad, fecha):
        self.id = id
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.fecha = fecha

class BaseDeDatos:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                    id INTEGER PRIMARY KEY,
                                    cantidad INTEGER,
                                    nombre TEXT,
                                    precio REAL
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                                    id INTEGER PRIMARY KEY,
                                    id_producto INTEGER,
                                    cantidad INTEGER,
                                    fecha DATE,
                                    FOREIGN KEY(id_producto) REFERENCES productos(id)
                                )''')
        self.conexion.commit()

    def ejecutar_consulta(self, consulta, parametros=()):
        self.cursor.execute(consulta, parametros)
        self.conexion.commit()

    def obtener_todos_los_productos(self):
        try:
            self.cursor.execute('''SELECT * FROM productos''')
            productos = self.cursor.fetchall()
            return productos
        except sqlite3.Error as e:
            print("Error al obtener productos:", e)
            return []

    # Métodos similares para obtener, agregar, modificar y eliminar productos y ventas.

class GestorProductosUI:
    def __init__(self, root):
        self.base_de_datos = BaseDeDatos('productos.db')
        self.root = root
        self.root.title("Gestión de Productos")
        self.setup_ui()

    def setup_ui(self):
        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        Label(frame, text="Gestión de Productos", font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)

        Button(frame, text="Añadir Producto", command=self.añadir_producto, width=20, bg="#4CAF50", fg="white").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Stock", command=self.ver_stock, width=20, bg="#9C27B0", fg="white").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        # Agregar más botones y funciones según sea necesario.

    def añadir_producto(self):
        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad del producto:")
        if cantidad is None:
            return
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del producto:")
        if nombre is None:
            return
        precio = simpledialog.askfloat("Precio", "Ingrese el precio del producto:")
        if precio is None:
            return

        self.base_de_datos.agregar_producto(cantidad, nombre, precio)
        messagebox.showinfo('Información', 'Producto añadido correctamente.')

    def ver_stock(self):
        productos = self.base_de_datos.obtener_todos_los_productos()
        if productos:
            stock_window = Toplevel(self.root)
            stock_window.title("Stock de Productos")
            
            stock_text = Text(stock_window, wrap="none")
            scrollbar_y = Scrollbar(stock_window, orient='vertical', command=stock_text.yview)
            scrollbar_x = Scrollbar(stock_window, orient='horizontal', command=stock_text.xview)
            stock_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            stock_text.pack(side="left", fill="both", expand=True)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            
            stock_info = '-' * 45 + '\n'
            stock_info += '{:<10} {:<20} {:<10} {:<10}\n'.format('ID', 'Producto', 'Cantidad', 'Precio')
            stock_info += '-' * 45 + '\n'
            for producto in productos:
                stock_info += '{:<10} {:<20} {:<10} {:<10}\n'.format(producto[0], producto[2], producto[1], producto[3])
            stock_info += '-' * 45 + '\n'
            stock_text.insert('1.0', stock_info)
            stock_text.configure(state='disabled')
        else:
            messagebox.showinfo('Información', 'No hay productos en el stock.')

def main():
    root = Tk()
    gestor_ui = GestorProductosUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()



def calcular_estadisticas_ventas(self):
    self.cursor.execute('''SELECT COUNT(id) AS total_ventas, 
                                  SUM(cantidad) AS cantidad_total, 
                                  SUM(cantidad * (SELECT precio FROM productos WHERE productos.id = ventas.id)) AS monto_total 
                           FROM ventas
                           WHERE estado = 'completa' ''')  # Filtramos solo las ventas completadas
    estadisticas = self.cursor.fetchone()
    if estadisticas:
        total_ventas = estadisticas['total_ventas']
        cantidad_total = estadisticas['cantidad_total']
        monto_total = estadisticas['monto_total']
    else:
        total_ventas = 0
        cantidad_total = 0
        monto_total = 0
    return {'total_ventas': total_ventas, 'cantidad_total': cantidad_total, 'monto_total': monto_total}
