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

    def ingresar_numero(self, mensaje):
        while True:
            try:
                valor = input(mensaje)
                return int(valor)
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def ingresar_nombre(self, mensaje):
        while True:
            valor = input(mensaje)
            if valor.strip():
                return valor
            print("Por favor, ingrese un nombre válido.")

    def ingresar_precio(self, mensaje):
        while True:
            try:
                valor = input(mensaje)
                return float(valor)
            except ValueError:
                print("Por favor, ingrese un precio válido.")

    def ingresar_producto(self):
        cantidad = self.ingresar_numero('Ingrese la cantidad del producto: ')
        nombre = self.ingresar_nombre('Ingrese el nombre del producto: ')
        precio = self.ingresar_precio('Ingrese el precio del producto: ')
        
        self.cursor.execute('''INSERT INTO productos (cantidad, nombre, precio) 
                               VALUES (?, ?, ?)''', (cantidad, nombre, precio))
        self.conexion.commit()
        print('Producto añadido correctamente.')

    def buscar_producto(self):
        nombre = self.ingresar_nombre('Ingrese el nombre del producto: ')
        self.cursor.execute('''SELECT cantidad, precio FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            print(f'Cantidad: {producto[0]}')
            print(f'Precio: {producto[1]}')
        else:
            print('El producto no está en la lista.')

    def modificar_producto(self):
        nombre = self.ingresar_nombre('Ingrese el nombre del producto que quiera modificar: ')
        self.cursor.execute('''SELECT * FROM productos WHERE nombre = ?''', (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            cantidad = self.ingresar_numero('Ingrese la nueva cantidad del producto: ')
            precio = self.ingresar_precio('Ingrese el nuevo precio del producto: ')
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
            gestor.ingresar_producto()
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
