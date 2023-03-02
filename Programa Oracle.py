import cx_Oracle

#Establecer la conexión con la base de datos Oracle
conn = cx_Oracle.connect('usuario/contraseña@localhost:puerto/SID')

#Esta función muestra una lista de sueldos distintos en la tabla "personal" y cuántos registros de personal tienen cada uno de esos sueldos. Para lograr esto, la función construye una consulta SQL que realiza una agregación por el campo "Sueldo" y cuenta la cantidad de registros que tienen cada sueldo. Luego, los resultados se ordenan por sueldo y se imprimen en la consola.
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

#En esta función, pedimos al usuario que ingrese un color para buscar y construimos una consulta SQL que filtra la tabla "trajes" por ese color. Luego, ejecutamos la consulta y mostramos los resultados en la consola, o informamos al usuario si no se encontraron resultados. Note que la consulta utiliza interpolación de strings para incluir la variable color en la consulta SQL.
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


def buscar_informacion_relacionada(dni):
    # Crear un cursor para ejecutar las consultas
    cursor = connection.cursor()

    try:
        # Obtener la información del personal con el DNI especificado
        cursor.execute("SELECT * FROM personal WHERE dni_personal = :dni", {'dni': dni})
        personal = cursor.fetchone()

        # Si el personal existe, obtener los trajes que ha utilizado y los clientes que los han comprado
        if personal is not None:
            cursor.execute("SELECT trajes.codigo_trajes, trajes.material, trajes.talla, trajes.color, trajes.disenador, trajes.cif_proveedor, trajes.numero_de_sede FROM trajes INNER JOIN usados ON trajes.codigo_trajes = usados.codigo_trajes WHERE usados.dni_personal = :dni", {'dni': dni})
            trajes = cursor.fetchall()

            cursor.execute("SELECT clientes.codigo_cliente, clientes.direccion, clientes.email, clientes.telefono FROM clientes INNER JOIN compras ON clientes.codigo_cliente = compras.codigo_cliente WHERE compras.codigo_trajes IN (SELECT codigo_trajes FROM usados WHERE dni_personal = :dni)", {'dni': dni})
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

    except cx_Oracle.Error as error:
        print(f"Error al buscar la información relacionada: {error}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

#Esta función pide al usuario que ingrese los datos del nuevo personal que se desea insertar en la tabla "personal" de la base de datos. Luego, se ejecuta una consulta SQL INSERT para agregar el nuevo registro a la tabla. Finalmente, se confirman los cambios y se imprime un mensaje de éxito
def insertar_personal(conn):
    cursor = conn.cursor()

    # Pedir datos del nuevo personal
    dni = input("Ingrese el DNI del nuevo personal: ")
    nombre = input("Ingrese el nombre del nuevo personal: ")
    fecha = input("Ingrese la fecha de contratación del nuevo personal (en formato dd/mm/yyyy): ")
    sueldo = float(input("Ingrese el sueldo del nuevo personal: "))
    anos_de_experiencia = int(input("Ingrese los años de experiencia del nuevo personal: "))

    # Insertar el nuevo personal en la tabla
    query = "INSERT INTO personal (DNI_Personal, Nombre, Fecha, Sueldo, Anos_de_experiencia) VALUES (:dni, :nombre, TO_DATE(:fecha, 'DD/MM/YYYY'), :sueldo, :anos)"
    cursor.execute(query, {'dni': dni, 'nombre': nombre, 'fecha': fecha, 'sueldo': sueldo, 'anos': anos_de_experiencia})

    # Confirmar cambios
    conn.commit()
    print("Se ha insertado correctamente el nuevo personal.")

#Esta función solicita al usuario que ingrese el DNI del personal que desea borrar de la tabla "personal" de la base de datos. Luego, se ejecuta una consulta SQL DELETE para eliminar el registro correspondiente de la tabla. Antes de realizar el borrado, se verifica que el personal exista en la tabla. Finalmente, se confirman los cambios y se imprime un mensaje de éxito.
def borrar_personal(conn):
    cursor = conn.cursor()

    # Pedir datos para identificar al personal que se quiere borrar
    dni = input("Ingrese el DNI del personal que desea borrar: ")

    # Verificar que el personal exista
    query = "SELECT DNI_Personal FROM personal WHERE DNI_Personal = :dni"
    cursor.execute(query, {'dni': dni})
    result = cursor.fetchone()
    if result is None:
        print("No se encontró el personal con el DNI ingresado.")
        return

    # Borrar al personal de la tabla
    query = "DELETE FROM personal WHERE DNI_Personal = :dni"
    cursor.execute(query, {'dni': dni})

    # Confirmar cambios
    conn.commit()
    print("Se ha borrado correctamente al personal con el DNI ingresado.")

#Esta función solicita al usuario que ingrese el DNI del personal que desea actualizar en la tabla "personal" de la base de datos. Luego, se verifica que el personal exista en la tabla. Si el personal existe, se le solicita al usuario que ingrese los nuevos datos que desea actualizar en el registro. La función construye dinámicamente una consulta SQL UPDATE en función de los datos proporcionados y luego la ejecuta para actualizar el registro en la tabla. Finalmente, se confirman los cambios y se imprime un mensaje de éxito.
def actualizar_personal(conn):
    cursor = conn.cursor()

    # Pedir datos para identificar al personal que se quiere actualizar
    dni = input("Ingrese el DNI del personal que desea actualizar: ")

    # Verificar que el personal exista
    query = "SELECT DNI_Personal FROM personal WHERE DNI_Personal = :dni"
    cursor.execute(query, {'dni': dni})
    result = cursor.fetchone()
    if result is None:
        print("No se encontró el personal con el DNI ingresado.")
        return

    # Pedir nuevos datos para actualizar al personal
    print("Ingrese los nuevos datos para actualizar al personal (deje en blanco si no desea actualizar):")
    nombre = input("Nombre: ")
    fecha = input("Fecha de contratación (en formato dd/mm/yyyy): ")
    sueldo = input("Sueldo: ")
    anos_de_experiencia = input("Años de experiencia: ")

    # Construir la consulta SQL para actualizar los datos
    set_clause = []
    params = {'dni': dni}
    if nombre:
        set_clause.append("Nombre = :nombre")
        params['nombre'] = nombre
    if fecha:
        set_clause.append("Fecha = TO_DATE(:fecha, 'DD/MM/YYYY')")
        params['fecha'] = fecha
    if sueldo:
        set_clause.append("Sueldo = :sueldo")
        params['sueldo'] = float(sueldo)
    if anos_de_experiencia:
        set_clause.append("Anos_de_experiencia = :anos")
        params['anos'] = int(anos_de_experiencia)
    set_clause = ", ".join(set_clause)

    # Actualizar al personal en la tabla
    query = f"UPDATE personal SET {set_clause} WHERE DNI_Personal = :dni"
    cursor.execute(query, params)

    # Confirmar cambios
    conn.commit()
    print("Se ha actualizado correctamente al personal con el DNI ingresado.")
