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
                // Recupera los detalles del producto desde el conjunto de resultados
                int cantidad = resultSet.getInt("cantidad");
                double precio = resultSet.getDouble("precio");

                // Modifica el producto (puedes agregar tu lógica aquí)
                // Por ejemplo:
                // cantidad += 10;
                // precio *= 1.1;

                // Actualiza el producto modificado en la base de datos
                PreparedStatement updateStatement = conexion.prepareStatement("UPDATE productos SET cantidad = ?, precio = ? WHERE nombre = ?");
                updateStatement.setInt(1, cantidad);
                updateStatement.setDouble(2, precio);
                updateStatement.setString(3, nombre);
                updateStatement.executeUpdate();

                System.out.println("Producto modificado correctamente.");
            } else {
                System.out.println("El producto no está en la lista.");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        GestorProductos gestor = new GestorProductos();
        // Puedes llamar a los métodos aquí según lo que necesites
        // gestor.ingresarProducto();
        // gestor.buscarProducto();
        // gestor.modificarProducto();
        gestor.cerrarConexion();
    }
}
