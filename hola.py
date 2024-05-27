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

    def __del__(self):
        self.conexion.close()

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

    def obtener_producto_por_nombre(self, nombre):
        self.cursor.execute('''SELECT * FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            return Producto(*producto)
        return None

    def obtener_producto_por_id(self, id):
        self.cursor.execute('''SELECT * FROM productos WHERE id = ?''', (id,))
        producto = self.cursor.fetchone()
        if producto:
            return Producto(*producto)
        return None

    def agregar_producto(self, cantidad, nombre, precio):
        self.cursor.execute('''INSERT INTO productos (cantidad, nombre, precio) VALUES (?, ?, ?)''', (cantidad, nombre, precio))
        self.conexion.commit()
    def obtener_todas_ventas(self):
        self.cursor.execute('''SELECT * FROM ventas''')
        ventas = self.cursor.fetchall()
        if ventas:
            return [Venta(*venta) for venta in ventas]
        return []

    def obtener_ventas_por_fecha(self, fecha):
        self.cursor.execute('''SELECT * FROM ventas WHERE fecha = ?''', (fecha,))
        ventas = self.cursor.fetchall()
        if ventas:
            return [Venta(*venta) for venta in ventas]
        return []
    def calcular_estadisticas_ventas(self):
        self.cursor.execute('''SELECT COUNT(id) AS total_ventas, 
                                  SUM(cantidad) AS cantidad_total, 
                                  SUM(cantidad * (SELECT precio FROM productos WHERE productos.id = ventas.id)) AS monto_total 
                           FROM ventas''')
        estadisticas=self.cursor.fetchone()
        if estadisticas:
                 total_ventas:['total_ventas']
                 cantidad_total: ['cantidad_total']
                 monto_total: ['monto_total'] 
        else:
            total_ventas=0
            cantidad_total =0
            monto_total=0
        return {'total_ventas': 0, 'cantidad_total': 0, 'monto_total': 0}
    
    def ingresar_stock(self, id_producto, cantidad):
        producto = self.obtener_producto_por_id(id_producto)
        if producto:
            nueva_cantidad = producto.cantidad + cantidad
            self.cursor.execute('''UPDATE productos SET cantidad = ? WHERE id = ?''', (nueva_cantidad, id_producto))
            self.conexion.commit()
            return True
        return False

    def registrar_venta(self, id_producto, cantidad):
        producto = self.obtener_producto_por_id(id_producto)
        if producto and producto.cantidad >= cantidad:
            nueva_cantidad = producto.cantidad - cantidad
            self.cursor.execute('''UPDATE productos SET cantidad = ? WHERE id = ?''', (nueva_cantidad, id_producto))
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute('''INSERT INTO ventas (id_producto, cantidad, fecha) VALUES (?, ?, ?)''', (id_producto, cantidad, fecha))
            self.conexion.commit()
            return True
        return False

    def modificar_producto(self, id_producto, nueva_cantidad, nuevo_nombre, nuevo_precio):
        self.cursor.execute('''UPDATE productos SET cantidad = ?, nombre = ?, precio = ? WHERE id = ?''', (nueva_cantidad, nuevo_nombre, nuevo_precio, id_producto))
        self.conexion.commit()

    def obtener_todos_los_productos(self):
        try:
            self.cursor.execute('''SELECT * FROM productos''')
            productos = self.cursor.fetchall()
            return productos
        except sqlite3.Error as e:
            print("Error al obtener productos:", e)
            return []
    def productos_sin_stock(self):
        try:
            self.cursor.execute('''SELECT * FROM productos WHERE cantidad = 0''')
            productos = self.cursor.fetchall()
            return productos
        except sqlite3.Error as e:
            print("Error al obtener productos sin stock:", e)
            return []

    


    # Métodos similares para modificar, eliminar y obtener productos, y para manejar ventas

class GestorProductosUI:
    def __init__(self, root):
        self.base_de_datos = BaseDeDatos('productos.db')
        self.root = root
        self.root.title("Gestión de Productos")
        self.setup_ui()

    def setup_ui(self):
        # Crear la interfaz de usuario
        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(padx=10, pady=10)
        def setup_ui(self):
    
          
         Label(frame, text="Gestión de Productos", font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        Button(frame, text="Ver Stock", command=self.ver_stock, width=20, bg="#9C27B0", fg="white").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Añadir Producto", command=self.añadir_producto, width=20, bg="#4CAF50", fg="white").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Ventas por Fecha", command=self.ver_ventas_por_fecha, width=20, bg="#00BCD4", fg="white").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Todas las Ventas", command=self.ver_todas_ventas, width=20, bg="#FFC107", fg="white").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Estadísticas de Ventas", command=self.estadisticas_ventas, width=20, bg="#E91E63", fg="white").grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ingresar Stock", command=self.ingresar_stock, width=20, bg="#2196F3", fg="white").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Registrar Venta", command=self.registrar_venta, width=20, bg="#FF9800", fg="white").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Modificar Producto", command=self.modificar_producto, width=20, bg="#F44336", fg="white").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Producto sin stock", command=self.productos_sin_stock, width=20, bg="#F44336", fg="white").grid(row=4, column=1, sticky="ew", padx=5, pady=5)


       
   
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

    def ver_todas_ventas(self):
        ventas = self.base_de_datos.obtener_todas_ventas()
        if ventas:
            ventas_info = "Todas las ventas:\n\n"
            for venta in ventas:
                ventas_info += f"ID: {venta.id}\nID Producto: {venta.id_producto}\nCantidad: {venta.cantidad}\nFecha: {venta.fecha}\n\n"
            messagebox.showinfo("Todas las Ventas", ventas_info)
        else:
            messagebox.showinfo("Todas las Ventas", "No hay ventas registradas.")

    def ver_ventas_por_fecha(self):
        fecha = simpledialog.askstring("Fecha", "Ingrese la fecha (YYYY-MM-DD):")
        if fecha is None:
            return

        ventas = self.base_de_datos.obtener_ventas_por_fecha(fecha)
        if ventas:
            ventas_info = f"Ventas del {fecha}:\n\n"
            for venta in ventas:
                ventas_info += f"ID: {venta.id}\nID Producto: {venta.id_producto}\nCantidad: {venta.cantidad}\nFecha: {venta.fecha}\n\n"
            messagebox.showinfo(f"Ventas del {fecha}", ventas_info)
        else:
            messagebox.showinfo(f"Ventas del {fecha}", f"No hay ventas registradas para la fecha {fecha}.")

    def estadisticas_ventas(self):
        estadisticas = self.base_de_datos.calcular_estadisticas_ventas()
        if estadisticas:
            messagebox.showinfo("Estadísticas de Ventas", f"Total de Ventas: {estadisticas['total_ventas']}\nMonto Total Vendido: {estadisticas['monto_total']}")
        else:
            messagebox.showinfo("Estadísticas de Ventas", "No hay ventas registradas.")
    def ingresar_stock(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto:")
        if id_producto is None:
            return
        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad a añadir al stock:")
        if cantidad is None:
            return

        if self.base_de_datos.ingresar_stock(id_producto, cantidad):
            messagebox.showinfo('Información', 'Stock ingresado correctamente.')
        else:
            messagebox.showerror('Error', 'Producto no encontrado.')

    def registrar_venta(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto:")
        if id_producto is None:
            return
        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad vendida:")
        if cantidad is None:
            return

        if self.base_de_datos.registrar_venta(id_producto, cantidad):
            messagebox.showinfo('Información', 'Venta registrada correctamente.')
        else:
            messagebox.showerror('Error', 'Producto no encontrado o stock insuficiente.')

    def modificar_producto(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto a modificar:")
        if id_producto is None:
            return
        nueva_cantidad = simpledialog.askinteger("Nueva Cantidad", "Ingrese la nueva cantidad del producto:")
        if nueva_cantidad is None:
            return
        nuevo_nombre = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre del producto:")
        if nuevo_nombre is None:
            return
        nuevo_precio = simpledialog.askfloat("Nuevo Precio", "Ingrese el nuevo precio del producto:")
        if nuevo_precio is None:
            return

        self.base_de_datos.modificar_producto(id_producto, nueva_cantidad, nuevo_nombre, nuevo_precio)
        messagebox.showinfo('Información', 'Producto modificado correctamente.')

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

    def productos_sin_stock(self):
        productos_sin_stock = self.base_de_datos.productos_sin_stock()
        if productos_sin_stock:
            productos_info = 'Productos sin stock:\n'
            for producto in productos_sin_stock:
                productos_info += f'Producto: {producto[2]}, Cantidad: {producto[1]}, Precio: {producto[3]}\n'
            messagebox.showinfo('Productos Sin Stock', productos_info)
        else:
            messagebox.showinfo('Información', 'No hay productos sin stock.')










    



def main():
    root = Tk()
    gestor_ui = GestorProductosUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()