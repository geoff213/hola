import sqlite3

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
        self.conexion.commit()

    def __del__(self):
        self.conexion.close()

    def añadir_producto(self):
        cantidad = int(input('Ingrese la cantidad del producto: '))
        nombre = input('Ingrese el nombre del producto: ')
        precio = float(input('Ingrese el precio del producto: '))
        
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
            cantidad = int(input('Ingrese la nueva cantidad del producto: '))
            precio = float(input('Ingrese el nuevo precio del producto: '))
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

    def cantidad_ventas_producto(self):
        nombre = input('Ingrese el nombre del producto para ver la cantidad de ventas: ')
        self.cursor.execute('''SELECT SUM(cantidad) FROM ventas WHERE nombre_producto = ?''', (nombre,))
        cantidad_ventas = self.cursor.fetchone()[0]
        if cantidad_ventas:
            print(f'Cantidad de ventas del producto "{nombre}": {cantidad_ventas}')
        else:
            print(f'El producto "{nombre}" no ha sido vendido.')

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
        (7) Cantidad de ventas por producto
        (8) Salir
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
            gestor.cantidad_ventas_producto()
        elif respuesta == '8':
            break
        else:
            print('Opción no válida. Intente de nuevo.')

if __name__ == "__main__":
    print('Bienvenido'.center(60, '-'))
    main()
