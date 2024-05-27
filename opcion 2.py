import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog
from datetime import datetime

class GestorProductos:
    def __init__(self, root):
        self.conexion = sqlite3.connect('productos.db')
        self.cursor = self.conexion.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                    id INTEGER PRIMARY KEY,
                                    cantidad INTEGER,
                                    nombre TEXT,
                                    precio REAL
                                )''')
        # Create ventas table for sales tracking
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                                    id INTEGER PRIMARY KEY,
                                    id_producto INTEGER,
                                    cantidad INTEGER,
                                    fecha DATE,
                                    FOREIGN KEY(id_producto) REFERENCES productos(id)
                                )''')
        self.conexion.commit()
        
        self.root = root
        self.root.title("Gestión de Productos")
        
        self.setup_ui()
        
    def __del__(self):
        self.conexion.close()

    def setup_ui(self):
        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        Label(frame, text="Gestión de Productos", font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)

        Button(frame, text="Añadir Producto", command=self.añadir_producto, width=20, bg="#4CAF50", fg="white").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Buscar Producto", command=self.buscar_producto, width=20, bg="#2196F3", fg="white").grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Modificar Producto", command=self.modificar_producto, width=20, bg="#FFC107", fg="white").grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Eliminar Producto", command=self.eliminar_producto, width=20, bg="#F44336", fg="white").grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        #Button(frame, text="Ver Productos", command=self.ver_productos, width=20, bg="#9C27B0", fg="white").grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Productos Sin Stock", command=self.productos_sin_stock, width=20, bg="#00BCD4", fg="white").grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ingresar Venta", command=self.ingresar_venta, width=20, bg="#FF9800", fg="white").grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Ventas", command=self.ver_ventas, width=20, bg="#8BC34A", fg="white").grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        Button(frame, text="Ver Stock", command=self.ver_stock, width=20, bg="#E91E63", fg="white").grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        Button(frame, text="Eliminar Venta", command=self.eliminar_venta, width=20, bg="#795548", fg="white").grid(row=5, column=1, sticky="ew", padx=5, pady=5)

    def añadir_producto(self):
        nombre = self.solicitar_texto('Ingrese el nombre del producto:')
        if nombre is None:
            return
        if not nombre:
            messagebox.showerror('Error', 'El nombre del producto no puede estar vacío.')
            return
        cantidad = self.validar_entero('Ingrese la cantidad del producto:')
        if cantidad is None:
            return
        precio = self.validar_float('Ingrese el precio del producto:')
        if precio is None:
            return
        
        self.cursor.execute('''INSERT INTO productos (cantidad, nombre, precio) 
                               VALUES (?, ?, ?)''', (cantidad, nombre, precio))
        self.conexion.commit()
        messagebox.showinfo('Información', 'Producto añadido correctamente.')

    def buscar_producto(self):
        nombre = self.solicitar_texto('Ingrese el nombre del producto:')
        if nombre is None:
            return
        if not nombre:
            messagebox.showerror('Error', 'El nombre del producto no puede estar vacío.')
            return
        self.cursor.execute('''SELECT cantidad, precio FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            messagebox.showinfo('Producto Encontrado', f'Cantidad: {producto[0]}\nPrecio: {producto[1]}')
        else:
            messagebox.showerror('Error', 'El producto no está en la lista.')

    def modificar_producto(self):
        nombre = self.solicitar_texto('Ingrese el nombre del producto que quiera modificar:')
        if nombre is None:
            return
        if not nombre:
            messagebox.showerror('Error', 'El nombre del producto no puede estar vacío.')
            return
        self.cursor.execute('''SELECT * FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            cantidad = self.validar_entero('Ingrese la nueva cantidad del producto:')
            if cantidad is None:
                return
            precio = self.validar_float('Ingrese el nuevo precio del producto:')
            if precio is None:
                return
            self.cursor.execute('''UPDATE productos SET cantidad = ?, precio = ? WHERE nombre = ?''',
                                (cantidad, precio, nombre))
            self.conexion.commit()
            messagebox.showinfo('Información', 'Producto modificado correctamente.')
        else:
            messagebox.showerror('Error', 'El producto no está en la lista.')

    def ver_productos(self):
        self.cursor.execute('''SELECT * FROM productos''')
        productos = self.cursor.fetchall()
        if productos:
            productos_info = '-' * 45 + '\n'
            productos_info += '{:<10} {:<20} {:<10} {:<10}\n'.format('ID', 'Producto', 'Cantidad', 'Precio')
            productos_info += '-' * 45 + '\n'
            for producto in productos:
                productos_info += '{:<10} {:<20} {:<10} {:<10}\n'.format(producto[0], producto[2], producto[1], producto[3])
            productos_info += '-' * 45 + '\n'
            messagebox.showinfo('Lista de Productos', productos_info)
        else:
            messagebox.showinfo('Información', 'No hay productos en el stock.')

    def eliminar_producto(self):
        nombre = self.solicitar_texto('Ingrese el nombre del producto que desea eliminar:')
        if nombre is None:
            return
        if not nombre:
            messagebox.showerror('Error', 'El nombre del producto no puede estar vacío.')
            return
        self.cursor.execute('''DELETE FROM productos WHERE nombre = ?''', (nombre,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            messagebox.showinfo('Información', 'Producto eliminado correctamente.')
        else:
            messagebox.showerror('Error', 'El producto no está en la lista.')

    def productos_sin_stock(self):
        self.cursor.execute('''SELECT * FROM productos WHERE cantidad = 0''')
        productos = self.cursor.fetchall()
        if productos:
            productos_info = 'Productos sin stock:\n'
            for producto in productos:
                productos_info += f'Producto: {producto[2]}, Cantidad: {producto[1]}, Precio: {producto[3]}\n'
            messagebox.showinfo('Productos Sin Stock', productos_info)
        else:
            messagebox.showinfo('Información', 'No hay productos sin stock.')

    def ingresar_venta(self):
        nombre_producto = self.solicitar_texto('Ingrese el nombre del producto vendido:')
        if nombre_producto is None:
            return
        if not nombre_producto:
            messagebox.showerror('Error', 'El nombre del producto no puede estar vacío.')
            return
        cantidad = self.validar_entero('Ingrese la cantidad vendida:')
        if cantidad is None:
            return
        fecha = datetime.now().strftime('%Y-%m-%d')

        # Check if the product exists in the database
        self.cursor.execute('''SELECT id FROM productos WHERE nombre = ?''', (nombre_producto,))
        producto = self.cursor.fetchone()
        if producto:
            id_producto = producto[0]
            # Update product quantity
            self.cursor.execute('''UPDATE productos SET cantidad = cantidad - ? WHERE id = ?''',
                                (cantidad, id_producto))
            # Record sale
            self.cursor.execute('''INSERT INTO ventas (id_producto, cantidad, fecha) VALUES (?, ?, ?)''',
                                (id_producto, cantidad, fecha))
            self.conexion.commit()
            messagebox.showinfo('Información', 'Venta registrada correctamente.')
        else:
            messagebox.showerror('Error', 'El producto no está en la lista.')

    def ver_ventas(self):
        self.cursor.execute('''SELECT ventas.id, ventas.id_producto, productos.nombre, ventas.cantidad, ventas.fecha 
                               FROM ventas JOIN productos ON ventas.id_producto = productos.id''')
        ventas = self.cursor.fetchall()
        if ventas:
            ventas_info = '-' * 62 + '\n'
            ventas_info += '{:<10} {:<12} {:<20} {:<10} {:<10}\n'.format('ID Venta', 'ID Producto', 'Producto', 'Cantidad', 'Fecha')
            ventas_info += '-' * 62 + '\n'
            for venta in ventas:
                ventas_info += '{:<10} {:<12} {:<20} {:<10} {:<10}\n'.format(venta[0], venta[1], venta[2], venta[3], venta[4])
            ventas_info += '-' * 62 + '\n'
            messagebox.showinfo('Lista de Ventas', ventas_info)
        else:
            messagebox.showinfo('Información', 'No hay ventas registradas.')

    def ver_stock(self):
        self.cursor.execute('''SELECT * FROM productos''')
        productos = self.cursor.fetchall()
        if productos:
            stock_window = Toplevel(self.root)
            stock_window.title("Stock de Productos")
            
            # Create a Text widget with a Scrollbar
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

    def eliminar_venta(self):
        id_venta = self.validar_entero('Ingrese el ID de la venta que desea eliminar:')
        if id_venta is None:
            return
        # Check if the sale exists
        self.cursor.execute('''SELECT * FROM ventas WHERE id = ?''', (id_venta,))
        venta = self.cursor.fetchone()
        if venta:
            id_producto = venta[1]
            cantidad = venta[2]
            # Revert the sale by adding back the sold quantity to the product's stock
            self.cursor.execute('''UPDATE productos SET cantidad = cantidad + ? WHERE id = ?''', (cantidad, id_producto))
            # Delete the sale record
            self.cursor.execute('''DELETE FROM ventas WHERE id = ?''', (id_venta,))
            self.conexion.commit()
            messagebox.showinfo('Información', 'Venta eliminada correctamente.')
        else:
            messagebox.showerror('Error', 'La venta no existe.')

    def solicitar_texto(self, mensaje):
        valor = simpledialog.askstring("Entrada", mensaje)
        return valor  # Permitir que el valor sea None si se cierra la ventana

    def validar_entero(self, mensaje):
        while True:
            valor = simpledialog.askinteger("Entrada", mensaje)
            if valor is None:
                return None
            return valor

    def validar_float(self, mensaje):
        while True:
            valor = simpledialog.askfloat("Entrada", mensaje)
            if valor is None:
                return None
            return valor

def main():
    root = Tk()
    gestor = GestorProductos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
