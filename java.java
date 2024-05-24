import java.sql.*;

import java.util.Scanner;

public class GestorProductos {
    private Connection conexion;
    private Statement statement;

    public GestorProductos() {
        try {
            conexion = DriverManager.getConnection("jdbc:sqlite:productos.db");
            statement = conexion.createStatement();
            statement.execute("CREATE TABLE IF NOT EXISTS productos (" +
                    "id INTEGER PRIMARY KEY," +
                    "cantidad INTEGER," +
                    "nombre TEXT," +
                    "precio REAL)");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void cerrarConexion() {
        try {
            if (statement != null)
                statement.close();
            if (conexion != null)
                conexion.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public int ingresarNumero(String mensaje) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print(mensaje);
            try {
                return Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Por favor, ingrese un número válido.");
            }
        }
    }

    public String ingresarNombre(String mensaje) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print(mensaje);
            String valor = scanner.nextLine().trim();
            if (!valor.isEmpty())
                return valor;
            System.out.println("Por favor, ingrese un nombre válido.");
        }
    }

    public double ingresarPrecio(String mensaje) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print(mensaje);
            try {
                return Double.parseDouble(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Por favor, ingrese un precio válido.");
            }
        }
    }

    public void ingresarProducto() {
        int cantidad = ingresarNumero("Ingrese la cantidad del producto: ");
        String nombre = ingresarNombre("Ingrese el nombre del producto: ");
        double precio = ingresarPrecio("Ingrese el precio del producto: ");

        try {
            PreparedStatement preparedStatement = conexion.prepareStatement("INSERT INTO productos (cantidad, nombre, precio) VALUES (?, ?, ?)");
            preparedStatement.setInt(1, cantidad);
            preparedStatement.setString(2, nombre);
            preparedStatement.setDouble(3, precio);
            preparedStatement.executeUpdate();
            System.out.println("Producto añadido correctamente.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void buscarProducto() {
        String nombre = ingresarNombre("Ingrese el nombre del producto: ");
        try {
            PreparedStatement preparedStatement = conexion.prepareStatement("SELECT cantidad, precio FROM productos WHERE nombre = ?");
            preparedStatement.setString(1, nombre);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                System.out.println("Cantidad: " + resultSet.getInt("cantidad"));
                System.out.println("Precio: " + resultSet.getDouble("precio"));
            } else {
                System.out.println("El producto no está en la lista.");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void modificarProducto() {
        String nombre = ingresarNombre("Ingrese el nombre del producto que quiera modificar: ");
        try {
            PreparedStatement preparedStatement = conexion.prepareStatement("SELECT * FROM productos WHERE nombre = ?");
            preparedStatement.setString(1, nombre);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                int cantidad = ingresarNumero("Ingrese la nueva cantidad del producto: ");
                double precio = ingresarPrecio("Ingrese el nuevo precio del producto: ");
                preparedStatement = conexion.prepareStatement("UPDATE productos SET cantidad = ?, precio = ? WHERE nombre = ?");
                preparedStatement.setInt(1, cantidad);
                preparedStatement.setDouble(2, precio);
                preparedStatement.setString(3, nombre);
                preparedStatement.executeUpdate();
                System.out.println("Producto modificado correctamente.");
            } else {
                System.out.println("El producto no está en la lista.");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void verProductos() {
        try {
            ResultSet resultSet = statement.executeQuery("SELECT * FROM productos");
            while (resultSet.next()) {
                System.out.println("Producto: " + resultSet.getString("nombre") + ", Cantidad: " +
                        resultSet.getInt("cantidad") + ", Precio: " + resultSet.getDouble("precio"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        GestorProductos gestor = new GestorProductos();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("""
                (1) Añadir productos
                (2) Buscar Productos
                (3) Modificar productos
                (4) Ver Productos
                (5) Salir
                """);
            System.out.print("Ingrese su opción: ");
            String respuesta = scanner.nextLine();
            switch (respuesta) {
                case "1":
                    gestor.ingresarProducto();
                    break;
                case "2":
                    gestor.buscarProducto();
                    break;
                case "3":
                    gestor.modificarProducto();
                    break;
                case "4":
                    gestor.verProductos();
                    break;
                case "5":
                    gestor.cerrarConexion();
                    System.exit(0);
                default:
                    System.out.println("Opción no válida. Intente de nuevo.");
            }
        }
    }
}
