print('Bienvenido'.center(60, '-'))
cantidad = []
producto = []
precio = []

# Función para guardar los datos en un archivo
def guardar_datos():
    with open('productos.txt', 'w') as archivo:
        for i in range(len(producto)):
            archivo.write(f"{cantidad[i]},{producto[i]},{precio[i]}\n")

# Función para cargar los datos desde un archivo
def cargar_datos():
    try:
        with open('productos.txt', 'r') as archivo:
            for linea in archivo:
                datos = linea.strip().split(',')
                cantidad.append(int(datos[0]))
                producto.append(datos[1])
                precio.append(float(datos[2]))
    except FileNotFoundError:
        print("No se encontró el archivo de datos.")

# Cargar datos existentes al inicio
cargar_datos()

while True:
    print("""
    (1) Añadir productos
    (2) Buscar Productos
    (3) Modificar productos
    (4) Ver Productos
    (5) Salir
    """)

    respuesta = int(input('Ingrese su opción: '))
    if respuesta == 1:
        ac = int(input('Ingrese la cantidad del producto: '))
        ap = input('Ingrese el nombre del producto: ')
        apre = float(input('Ingrese el precio del producto: '))

        cantidad.append(ac)
        producto.append(ap)
        precio.append(apre)

        guardar_datos()  # Guardar datos después de añadir un producto
    elif respuesta == 2:
        buscador = input('Ingrese el nombre del producto: ')
        if buscador in producto:
            posicion = producto.index(buscador)
            print('La cantidad del producto es:', cantidad[posicion])
            print('El nombre del producto es:', producto[posicion])
            print('El precio del producto es:', precio[posicion])
        else:
            print('El producto no está en la lista.')
    elif respuesta == 3:
        buscador = input('Ingrese el nombre del producto que quiera modificar: ')
        if buscador in producto:
            posicion = producto.index(buscador)
            ac = int(input('Ingrese la nueva cantidad del producto: '))
            ap = input('Ingrese el nuevo nombre del producto: ')
            apre = float(input('Ingrese el nuevo precio del producto: '))
            cantidad[posicion] = ac
            producto[posicion] = ap
            precio[posicion] = apre
            guardar_datos()  # Guardar datos después de modificar un producto
            print('Producto modificado exitosamente.')
        else:
            print('El producto no está en la lista.')
    elif respuesta == 4:
        print('La cantidad es:', cantidad)
        print('El nombre es:', producto)
        print('El precio es:', precio)
    elif respuesta == 5:
        guardar_datos()  # Guardar datos antes de salir
        break
    else:
        print('Opción no válida. Intente de nuevo.')