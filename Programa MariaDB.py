import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tu_usuario",
  password="tu_contraseña",
  database="tu_base_de_datos"
)

mycursor = mydb.cursor()

def listar_personal_por_sueldo(conn):
    cursor = conn.cursor()

    # Consultar la tabla personal para obtener la información deseada
    query = """
        SELECT Sueldo, COUNT(*) AS Cantidad
        FROM personal
        GROUP BY Sueldo
        ORDER BY Sueldo
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Imprimir los resultados
    print("Sueldo\tCantidad")
    for row in results:
        print(f"{row[0]}\t{row[1]}")

def buscar_trajes_por_color(conn):
    cursor = conn.cursor()

    # Pedir al usuario que ingrese un color para buscar
    color = input("Ingrese el color de los trajes a buscar: ")

    # Construir la consulta SQL que filtra por color
    query = f"""
        SELECT codigo_trajes, material, talla, disenador, cif_proveedor, numero_de_sede
        FROM trajes
        WHERE color = '{color}'
    """

    # Ejecutar la consulta y mostrar los resultados
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        print("Resultados de la búsqueda:")
        print("Código\tMaterial\tTalla\tDiseñador\tProveedor\tSede")
        for row in results:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")
    else:
        print("No se encontraron trajes con el color especificado.")

def buscar_informacion_relacionada(conn):
    cursor = conn.cursor()

    try:
        # Pedir al usuario que ingrese un DNI para buscar
        dni = input("Ingrese el DNI del personal para buscar la información relacionada: ")

        # Obtener la información del personal con el DNI especificado
        query = """
            SELECT *
            FROM personal
            WHERE dni_personal = %s
        """
        cursor.execute(query, (dni,))
        personal = cursor.fetchone()

        # Si el personal existe, obtener los trajes que ha utilizado y los clientes que los han comprado
        if personal is not None:
            query = """
                SELECT trajes.codigo_trajes, trajes.material, trajes.talla, trajes.color, trajes.disenador, trajes.cif_proveedor, trajes.numero_de_sede
                FROM trajes
                INNER JOIN usados ON trajes.codigo_trajes = usados.codigo_trajes
                WHERE usados.dni_personal = %s
            """
            cursor.execute(query, (dni,))
            trajes = cursor.fetchall()

            query = """
                SELECT clientes.codigo_cliente, clientes.direccion, clientes.email, clientes.telefono
                FROM clientes
                INNER JOIN compras ON clientes.codigo_cliente = compras.codigo_cliente
                WHERE compras.codigo_trajes IN (
                    SELECT codigo_trajes FROM usados WHERE dni_personal = %s
                )
            """
            cursor.execute(query, (dni,))
            clientes = cursor.fetchall()

            # Mostrar la información del personal, trajes y clientes obtenidos
            print("Información del personal:")
            print(f"DNI: {personal[0]}")
            print(f"Nombre: {personal[1]}")
            print(f"Fecha de nacimiento: {personal[2]}")
            print(f"Sueldo: {personal[3]}")
            print(f"Años de experiencia: {personal[4]}")

            print("\nTrajes utilizados:")
            for traje in trajes:
                print(f"Código: {traje[0]}")
                print(f"Material: {traje[1]}")
                print(f"Talla: {traje[2]}")
                print(f"Color: {traje[3]}")
                print(f"Diseñador: {traje[4]}")
                print(f"CIF del proveedor: {traje[5]}")
                print(f"Número de sede: {traje[6]}")
                print("")

            print("\nClientes que han comprado los trajes:")
            for cliente in clientes:
                print(f"Código: {cliente[0]}")
                print(f"Dirección: {cliente[1]}")
                print(f"Email: {cliente[2]}")
                print(f"Teléfono: {cliente[3]}")
                print("")

        else:
            print(f"No se ha encontrado personal con el DNI '{dni}'")

    except mysql.connector.Error as error:
        print(f"Error al buscar la información relacionada: {error}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()


def borrar_personal():
    dni_personal = input("Introduce el DNI del personal que quieres borrar: ")

    sql = "DELETE FROM personal WHERE DNI_Personal = %s"
    val = (dni_personal, )

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "registro(s) borrado(s).")

def actualizar_personal():
    dni_personal = input("Introduce el DNI del personal que quieres actualizar: ")

    print("Introduce los nuevos datos:")
    nombre = input("Nombre: ")
    fecha = input("Fecha de contratación (YYYY-MM-DD): ")
    sueldo = input("Sueldo: ")
    anos_de_experiencia = input("Años de experiencia: ")

    sql = "UPDATE personal SET Nombre = %s, Fecha = %s, Sueldo = %s, Anos_de_experiencia = %s WHERE DNI_Personal = %s"
    val = (nombre, fecha, sueldo, anos_de_experiencia, dni_personal)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "registro(s) actualizado(s).")

def actualizar_datos():
    #Pedimos al usuario que introduzca el DNI del personal a actualizar
    dni = input("Introduce el DNI del personal a actualizar: ")
    
    #Pedimos al usuario que introduzca los nuevos datos
    nombre = input("Introduce el nuevo nombre del personal: ")
    fecha = input("Introduce la nueva fecha de incorporación (YYYY-MM-DD): ")
    sueldo = input("Introduce el nuevo sueldo del personal: ")
    experiencia = input("Introduce los nuevos años de experiencia del personal: ")
    
    #Ejecutamos la consulta para actualizar los datos del personal
    sql = "UPDATE personal SET Nombre = %s, Fecha = %s, Sueldo = %s, Anos_de_experiencia = %s WHERE DNI_Personal = %s"
    valores = (nombre, fecha, sueldo, experiencia, dni)
    cursor.execute(sql, valores)
    
    #Confirmamos los cambios en la base de datos
    conexion.commit()
    
    #Mostramos un mensaje de éxito
    print(cursor.rowcount, "registros actualizados exitosamente.")

    #Cerramos la conexión con la base de datos
    cursor.close()
    conexion.close()