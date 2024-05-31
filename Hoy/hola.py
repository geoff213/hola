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
        return Producto(*producto) if producto else None

    def obtener_producto_por_id(self, id):
        self.cursor.execute('''SELECT * FROM productos WHERE id = ?''', (id,))
        producto = self.cursor.fetchone()
        return Producto(*producto) if producto else None

    def agregar_producto(self, cantidad, nombre, precio):
        self.cursor.execute('''INSERT INTO productos (cantidad, nombre, precio) VALUES (?, ?, ?)''', (cantidad, nombre, precio))
        self.conexion.commit()

    def obtener_todas_ventas(self):
        self.cursor.execute('''SELECT * FROM ventas''')
        ventas = self.cursor.fetchall()
        return [Venta(*venta) for venta in ventas] if ventas else []

    def obtener_ventas_por_fecha(self, fecha):
        self.cursor.execute('''SELECT * FROM ventas WHERE fecha = ?''', (fecha,))
        ventas = self.cursor.fetchall()
        return [Venta(*venta) for venta in ventas] if ventas else []

    def calcular_estadisticas_ventas(self):
        self.cursor.execute('''SELECT COUNT(*), SUM(cantidad * (SELECT precio FROM productos WHERE productos.id = ventas.id_producto)) FROM ventas''')
        total_ventas, monto_total = self.cursor.fetchone()
        return {'total_ventas': total_ventas, 'monto_total': monto_total if monto_total is not None else 0.0}

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
        self.cursor.execute('''SELECT * FROM productos''')
        return self.cursor.fetchall()

    def productos_sin_stock(self):
        self.cursor.execute('''SELECT * FROM productos WHERE cantidad = 0''')
        return self.cursor.fetchall()

    def eliminar_producto(self, id_producto):
        try:
            self.cursor.execute('''DELETE FROM productos WHERE id = ?''', (id_producto,))
            self.conexion.commit()
            return self.cursor.rowcount > 0  
        except sqlite3.Error as e:
            print("Error al eliminar producto:", e)
            return False   

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
        Button(frame, text="Ver Stock", command=self.ver_stock, width=20, bg="#9C27B0", fg="white").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Añadir Producto", command=self.añadir_producto, width=20, bg="#4CAF50", fg="white").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Ventas por Fecha", command=self.ver_ventas_por_fecha, width=20, bg="#00BCD4", fg="white").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Todas las Ventas", command=self.ver_todas_ventas, width=20, bg="#FFC107", fg="white").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Estadísticas de Ventas", command=self.estadisticas_ventas, width=20, bg="#E91E63", fg="white").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ingresar Stock", command=self.ingresar_stock, width=20, bg="#2196F3", fg="white").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Registrar Venta", command=self.registrar_venta, width=20, bg="#FF9800", fg="white").grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Modificar Producto", command=self.modificar_producto, width=20, bg="#F44336", fg="white").grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Producto sin stock", command=self.productos_sin_stock, width=20, bg="#795548", fg="white").grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Eliminar Producto", command=self.eliminar_producto, width=20, bg="#F44336", fg="white").grid(row=5, column=1, sticky="ew", padx=5, pady=5)

    def añadir_producto(self):
        nombre = simpledialog.askstring("Nombre del Producto", "Ingrese el nombre del producto:")
        if not nombre:
            return
        try:
            cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad del producto:")
            if cantidad is None or cantidad < 0:
                raise ValueError("Cantidad inválida")
            precio = simpledialog.askfloat("Precio", "Ingrese el precio del producto:")
            if precio is None or precio < 0:
                raise ValueError("Precio inválido")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.base_de_datos.agregar_producto(cantidad, nombre, precio)
        messagebox.showinfo("Producto Añadido", f"Producto '{nombre}' añadido correctamente.")

    def ver_todas_ventas(self):
        ventas = self.base_de_datos.obtener_todas_ventas()
        if ventas:
            self.mostrar_ventas(ventas, "Todas las Ventas")
        else:
            messagebox.showinfo("Todas las Ventas", "No hay ventas registradas.")

    def ver_ventas_por_fecha(self):
        fecha = simpledialog.askstring("Fecha", "Ingrese la fecha (YYYY-MM-DD):")
        if not fecha:
            return

        ventas = self.base_de_datos.obtener_ventas_por_fecha(fecha)
        if ventas:
            self.mostrar_ventas(ventas, f"Ventas del {fecha}")
        else:
            messagebox.showinfo(f"Ventas del {fecha}", f"No hay ventas registradas para la fecha {fecha}.")

    def estadisticas_ventas(self):
        estadisticas = self.base_de_datos.calcular_estadisticas_ventas()
        messagebox.showinfo("Estadísticas de Ventas", 
                            f"Total de Ventas: {estadisticas['total_ventas']}\n"
                            f"Monto Total Vendido: {estadisticas['monto_total']:.2f}")

    def ingresar_stock(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto:")
        if id_producto is None:
            return
        try:
            cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad a añadir al stock:")
            if cantidad is None or cantidad < 0:
                raise ValueError("Cantidad inválida")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if self.base_de_datos.ingresar_stock(id_producto, cantidad):
            messagebox.showinfo('Información', 'Stock ingresado correctamente.')
        else:
            messagebox.showerror('Error', 'Producto no encontrado.')

    def registrar_venta(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto:")
        if id_producto is None:
            return
        try:
            cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad vendida:")
            if cantidad is None or cantidad < 0:
                raise ValueError("Cantidad inválida")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if self.base_de_datos.registrar_venta(id_producto, cantidad):
            messagebox.showinfo('Información', 'Venta registrada correctamente.')
        else:
            messagebox.showerror('Error', 'Producto no encontrado o stock insuficiente.')

    def modificar_producto(self):
        id_producto = simpledialog.askinteger("ID del Producto", "Ingrese el ID del producto a modificar:")
        if id_producto is None:
            return
        try:
            nueva_cantidad = simpledialog.askinteger("Nueva Cantidad", "Ingrese la nueva cantidad del producto:")
            if nueva_cantidad is None or nueva_cantidad < 0:
                raise ValueError("Cantidad inválida")
            nuevo_nombre = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre del producto:")
            if not nuevo_nombre:
                raise ValueError("Nombre inválido")
            nuevo_precio = simpledialog.askfloat("Nuevo Precio", "Ingrese el nuevo precio del producto:")
            if nuevo_precio is None or nuevo_precio < 0:
                raise ValueError("Precio inválido")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.base_de_datos.modificar_producto(id_producto, nueva_cantidad, nuevo_nombre, nuevo_precio)
        messagebox.showinfo('Información', 'Producto modificado correctamente.')

    def ver_stock(self):
        productos = self.base_de_datos.obtener_todos_los_productos()
        if productos:
            self.mostrar_productos(productos, "Stock de Productos")
        else:
            messagebox.showinfo('Información', 'No hay productos en el stock.')

    def productos_sin_stock(self):
        productos_sin_stock = self.base_de_datos.productos_sin_stock()
        if productos_sin_stock:
            productos_info = 'Productos sin stock:\n'
            for producto in productos_sin_stock:
                productos_info += f'ID: {producto[0]}, Producto: {producto[2]}, Precio: {producto[3]}\n'
            messagebox.showinfo('Productos Sin Stock', productos_info)
        else:
            messagebox.showinfo('Información', 'No hay productos sin stock.')

    def eliminar_producto(self):
        id_producto = simpledialog.askinteger("Eliminar Producto", "Ingrese el ID del producto a eliminar:")
        if id_producto is not None:
            if self.base_de_datos.eliminar_producto(id_producto):
                messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el producto con ID {id_producto}.")
        else:
            messagebox.showwarning("Cancelado", "No se ingresó ningún ID.")

    def mostrar_productos(self, productos, titulo):
        window = Toplevel(self.root)
        window.title(titulo)
        
        text_widget = Text(window, wrap="none")
        scrollbar_y = Scrollbar(window, orient='vertical', command=text_widget.yview)
        scrollbar_x = Scrollbar(window, orient='horizontal', command=text_widget.xview)
        text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        info = '-' * 45 + '\n'
        info += '{:<10} {:<20} {:<10} {:<10}\n'.format('ID', 'Producto', 'Cantidad', 'Precio')
        info += '-' * 45 + '\n'
        for producto in productos:
            info += '{:<10} {:<20} {:<10} {:<10}\n'.format(producto[0], producto[2], producto[1], producto[3])
        info += '-' * 45 + '\n'
        text_widget.insert('1.0', info)
        text_widget.configure(state='disabled')

    def mostrar_ventas(self, ventas, titulo):
        window = Toplevel(self.root)
        window.title(titulo)
        
        text_widget = Text(window, wrap="none")
        scrollbar_y = Scrollbar(window, orient='vertical', command=text_widget.yview)
        scrollbar_x = Scrollbar(window, orient='horizontal', command=text_widget.xview)
        text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        info = '-' * 80 + '\n'
        info += '{:<10} {:<15} {:<10} {:<20}\n'.format('ID', 'ID Producto', 'Cantidad', 'Fecha')
        info += '-' * 80 + '\n'
        for venta in ventas:
            info += '{:<10} {:<15} {:<10} {:<20}\n'.format(venta.id, venta.id_producto, venta.cantidad, venta.fecha)
        info += '-' * 80 + '\n'
        
        text_widget.insert('1.0', info)
        text_widget.configure(state='disabled')

def main():
    root = Tk()
    gestor_ui = GestorProductosUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
