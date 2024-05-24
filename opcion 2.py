import pyodbc

class GestorProductos:
    def __init__(self):
        self.conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=tu_servidor;DATABASE=nombre_base_de_datos;UID=usuario;PWD=contraseña')
        self.cursor = self.conexion.cursor()

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
            print(f'Producto: {producto.nombre}, Cantidad: {producto.cantidad}, Precio: {producto.precio}')

def main():
    gestor = GestorProductos()

    while True:
        print("""
        (1) Añadir productos
        (2) Buscar Productos
        (3) Modificar productos
        (4) Ver Productos
        (5) Salir
        """)

        respuesta = input('Ingrese su opción: ')
        if respuesta == '1':
            gestor.añadir_producto()
        elif respuesta == '2':
            gestor.buscar_producto()
        elif respuesta == '3':
            gestor.modificar_producto()
        elif respuesta == '4':
            gestor.ver_productos()
        elif respuesta == '5':
            break
        else:
            print('Opción no válida. Intente de nuevo.')

if __name__ == "__main__":
    print('Bienvenido'.center(60, '-'))
    main()