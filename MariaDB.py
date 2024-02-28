import pymysql

# Ejemplo de conexión a MySQL/MariaDB
connection = pymysql.connect(host='localhost',
                             user='alejandro',
                             password='alejandro',
                             database='proyecto',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)

def listar_usuarios_y_libros():
    """
    Lista los nombres de usuarios y la cantidad de libros comprados por cada usuario en la tabla "Usuario".
    """
    cursor = connection.cursor()
    cursor.execute("""
        SELECT u.Nombre, COUNT(c.Cod_documento) AS Num_libros_comprados
        FROM Usuario u
        LEFT JOIN Compra c ON u.DNI = c.DNI
        GROUP BY u.Nombre
    """)
    usuarios_libros = cursor.fetchall()
    print("Usuarios y la cantidad de libros comprados:")
    for usuario, num_libros in usuarios_libros:
        print(f"{usuario}: {num_libros} libros")

def buscar_usuario_por_dni():
    """
    Busca un usuario en la tabla "Usuario" por su DNI.
    """
    dni = int(input("Ingrese el DNI del usuario a buscar: "))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE DNI = :dni", {"dni": dni})
    usuario = cursor.fetchone()
    if usuario:
        print("Usuario encontrado:")
        print(usuario)
    else:
        print("No se encontró ningún usuario con ese DNI.")

def buscar_libro_por_titulo():
    """
    Busca un libro en la tabla "Libro" por su título.
    """
    titulo = input("Ingrese el título del libro a buscar: ")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM Libro
        WHERE Titulo = :titulo
    """, {"titulo": titulo})
    libro = cursor.fetchone()
    if libro:
        print("Libro encontrado:")
        print(libro)
    else:
        print("No se encontró ningún libro con ese título.")

def insertar_libro():
    """
    Inserta un nuevo libro en la tabla "Libro".
    """
    titulo = input("Ingrese el título del libro: ")
    fecha_publicacion = input("Ingrese la fecha de publicación (YYYY-MM-DD): ")
    editorial = input("Ingrese la editorial del libro: ")
    isbn = input("Ingrese el ISBN del libro: ")
    serie = input("Ingrese el número de serie del libro: ")
    edicion = input("Ingrese la edición del libro: ")
    volumen = input("Ingrese el volumen del libro: ")
    sinapsis = input("Ingrese la sinopsis del libro: ")

    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Libro (Titulo, Fecha_publicacion, Editorial, ISBN, Serie, Edicion, Volumen, Sinapsis)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (titulo, fecha_publicacion, editorial, isbn, serie, edicion, volumen, sinapsis))
    connection.commit()
    print("Libro insertado con éxito.")

def borrar_autor():
    """
    Elimina un autor de la tabla "Autor" por su código.
    """
    cod_autor = int(input("Ingrese el código del autor a eliminar: "))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Autor WHERE Cod_autor = :cod_autor", {"cod_autor": cod_autor})
    connection.commit()
    print("Autor eliminado con éxito.")

def actualizar_autor():
    """
    Actualiza la edad de un autor en la tabla "Autor".
    """
    cod_autor = int(input("Ingrese el código del autor: "))
    nueva_edad = int(input("Ingrese la nueva edad del autor: "))
    cursor = connection.cursor()
    cursor.execute("UPDATE Autor SET Edad = :nueva_edad WHERE Cod_autor = :cod_autor",
                   {"nueva_edad": nueva_edad, "cod_autor": cod_autor})
    connection.commit()
    print("Edad del autor actualizada con éxito.")

# Llamadas a las funciones según las necesidades del usuario
listar_usuarios_y_libros()
buscar_usuario_por_dni()
buscar_libro_por_titulo()
insertar_libro()
borrar_autor()
actualizar_autor()

# Cerrar la conexión a la base de datos
connection.close()