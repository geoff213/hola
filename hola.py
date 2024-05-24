class GestorProductos:
    def __init__(self):
        self.cantidad = []
        self.producto = []
        self.precio = []

    def añadir_producto(self):
        cantidad = int(input('Ingrese la cantidad del producto: '))
        nombre = input('Ingrese el nombre del producto: ')
        precio = float(input('Ingrese el precio del producto: '))
        
        self.cantidad.append(cantidad)
        self.producto.append(nombre)
        self.precio.append(precio)
        print('Producto añadido correctamente.')

    def buscar_producto(self):
        nombre = input('Ingrese el nombre del producto: ')
        try:
            index = self.producto.index(nombre)
            print(f'Cantidad: {self.cantidad[index]}')
            print(f'Precio: {self.precio[index]}')
        except ValueError:
            print('El producto no está en la lista.')

    def modificar_producto(self):
        nombre = input('Ingrese el nombre del producto que quiera modificar: ')
        try:
            index = self.producto.index(nombre)
            cantidad = int(input('Ingrese la nueva cantidad del producto: '))
            precio = float(input('Ingrese el nuevo precio del producto: '))
            
            self.cantidad[index] = cantidad
            self.precio[index] = precio
            print('Producto modificado correctamente.')
        except ValueError:
            print('El producto no está en la lista.')

    def ver_productos(self):
        for i in range(len(self.producto)):
            print(f'Producto: {self.producto[i]}, Cantidad: {self.cantidad[i]}, Precio: {self.precio[i]}')

    def guardar_datos(self):
        with open('productos.txt', 'w') as archivo:
            for i in range(len(self.producto)):
                archivo.write(f"{self.cantidad[i]},{self.producto[i]},{self.precio[i]}\n")

    def cargar_datos(self):
        try:
            with open('productos.txt', 'r') as archivo:
                for linea in archivo:
                    cantidad, nombre, precio = linea.strip().split(',')
                    self.cantidad.append(int(cantidad))
                    self.producto.append(nombre)
                    self.precio.append(float(precio))
        except FileNotFoundError:
            print("No se encontró el archivo de datos.")


def main():
    gestor = GestorProductos()
    gestor.cargar_datos()

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
            gestor.guardar_datos()
        elif respuesta == '2':
            gestor.buscar_producto()
        elif respuesta == '3':
            gestor.modificar_producto()
            gestor.guardar_datos()
        elif respuesta == '4':
            gestor.ver_productos()
        elif respuesta == '5':
            gestor.guardar_datos()
            break
        else:
            print('Opción no válida. Intente de nuevo.')


if __name__ == "__main__":
    print('Bienvenido'.center(60, '-'))
    main()
