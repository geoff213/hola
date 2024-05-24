import sqlite3
from datetime import datetime

class GestorProductos:
    def __init__(self):
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
                                    nombre_producto TEXT,
                                    cantidad INTEGER,
                                    fecha DATE
                                )''')
        self.conexion.commit()

    def __del__(self):
        self.conexion.close()

    def añadir_producto(self):
        nombre = input('Ingrese el nombre del producto: ')
        cantidad = self.validar_entero('Ingrese la cantidad del producto: ')
        precio = self.validar_float('Ingrese el precio del producto: ')
        
        self.cursor.execute('''INSERT INTO productos (cantidad, nombre, precio) 
                               VALUES (?, ?, ?)''', (cantidad, nombre, precio))
        self.conexion.commit()
        print('Producto añadido correctamente.')

    def buscar_producto(self):
        nombre = input('Ingrese el nombre del producto: ')
        self.cursor.execute('''SELECT cantidad, precio FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            print(f'Cantidad: {producto[0]}')
            print(f'Precio: {producto[1]}')
        else:
            print('El producto no está en la lista.')

    def modificar_producto(self):
        nombre = input('Ingrese el nombre del producto que quiera modificar: ')
        self.cursor.execute('''SELECT * FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            cantidad = self.validar_entero('Ingrese la nueva cantidad del producto: ')
            precio = self.validar_float('Ingrese el nuevo precio del producto: ')
            self.cursor.execute('''UPDATE productos SET cantidad = ?, precio = ? WHERE nombre = ?''',
                                (cantidad, precio, nombre))
            self.conexion.commit()
            print('Producto modificado correctamente.')
        else:
            print('El producto no está en la lista.')

    def ver_productos(self):
        self.cursor.execute('''SELECT * FROM productos''')
        productos = self.cursor.fetchall()
        for producto in productos:
            print(f'Producto: {producto[2]}, Cantidad: {producto[1]}, Precio: {producto[3]}')

    def eliminar_producto(self):
        nombre = input('Ingrese el nombre del producto que desea eliminar: ')
        self.cursor.execute('''DELETE FROM productos WHERE nombre = ?''', (nombre,))
        self.conexion.commit()
        print('Producto eliminado correctamente.')

    def productos_sin_stock(self):
        self.cursor.execute('''SELECT * FROM productos WHERE cantidad = 0''')
        productos = self.cursor.fetchall()
        if productos:
            print('Productos sin stock:')
            for producto in productos:
                print(f'Producto: {producto[2]}, Cantidad: {producto[1]}, Precio: {producto[3]}')
        else:
            print('No hay productos sin stock.')

    def ingresar_venta(self):
        nombre_producto = input('Ingrese el nombre del producto vendido: ')
        cantidad = self.validar_entero('Ingrese la cantidad vendida: ')
        fecha = datetime.now().strftime('%Y-%m-%d')
        
        # Update product quantity
        self.cursor.execute('''UPDATE productos SET cantidad = cantidad - ? WHERE nombre = ?''',
                            (cantidad, nombre_producto))
        # Record sale
        self.cursor.execute('''INSERT INTO ventas (nombre_producto, cantidad, fecha) VALUES (?, ?, ?)''',
                            (nombre_producto, cantidad, fecha))
        self.conexion.commit()
        print('Venta registrada correctamente.')

    def ver_ventas(self):
        self.cursor.execute('''SELECT * FROM ventas''')
        ventas = self.cursor.fetchall()
        if ventas:
            print('Registro de ventas:')
            for venta in ventas:
                print(f'Producto: {venta[1]}, Cantidad: {venta[2]}, Fecha: {venta[3]}')
        else:
            print('No hay ventas registradas.')

    @staticmethod
    def validar_entero(mensaje):
        while True:
            try:
                valor = int(input(mensaje))
                return valor
            except ValueError:
                print('Error: Por favor, ingrese un número entero válido.')

    @staticmethod
    def validar_float(mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print('Error: Por favor, ingrese un número decimal válido.')

def main():
    gestor = GestorProductos()

    while True:
        print("""
        (1) Añadir productos
        (2) Buscar Productos
        (3) Modificar productos
        (4) Eliminar Producto
        (5) Ver Productos
        (6) Productos sin stock
        (7) Ingresar Venta
        (8) Ver Ventas
        (9) Salir
        """)

        respuesta = input('Ingrese su opción: ')
        if respuesta == '1':
            gestor.añadir_producto()
        elif respuesta == '2':
            gestor.buscar_producto()
        elif respuesta == '3':
            gestor.modificar_producto()
        elif respuesta == '4':
            gestor.eliminar_producto()
        elif respuesta == '5':
            gestor.ver_productos()
        elif respuesta == '6':
            gestor.productos_sin_stock()
        elif respuesta == '7':
            gestor.ingresar_venta()
        elif respuesta == '8':
            gestor.ver_ventas()
        elif respuesta == '9':
            break
        else:
            print('Opción no válida. Intente de nuevo.')

if __name__ == "__main__":
    print('Bienvenido'.center(60, '-'))
    main()
