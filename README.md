# proyecto_BD
En este programa en Python, realizaremos operaciones DML sobre una base de datos Oracle que contiene tres tablas: personal, trajes y clientes. A continuación se describen las funciones que se implementarán en este programa:

Listar información: La función listar_info(tabla, campo) muestra cierta información de una tabla y el total de veces que aparece dicha información. Recibe dos parámetros: el nombre de la tabla y el campo de la tabla del que se desea obtener la información.

Buscar o filtrar información: La función buscar_info(tabla, campo, valor) busca los registros en una tabla que contengan el valor especificado en un campo de la tabla. Recibe tres parámetros: el nombre de la tabla, el nombre del campo y el valor que se desea buscar.

Buscar información relacionada: La función buscar_relacion(tabla1, tabla2, campo1, campo2, valor) busca los registros en una tabla que contengan el valor especificado en un campo de la tabla1 y muestra información relacionada de la tabla2. Recibe cinco parámetros: el nombre de la tabla1, el nombre de la tabla2, el nombre del campo1, el nombre del campo2 y el valor que se desea buscar.

Insertar información: La función insertar_info(tabla, datos) inserta un nuevo registro en la tabla especificada con los datos proporcionados. Recibe dos parámetros: el nombre de la tabla y los datos a insertar en forma de diccionario.

Borrar información: La función borrar_info(tabla, campo, valor) elimina los registros en una tabla que contengan el valor especificado en un campo de la tabla. Recibe tres parámetros: el nombre de la tabla, el nombre del campo y el valor que se desea buscar.

Actualizar información: La función actualizar_info(tabla, campo, valor, nuevos_datos) actualiza los registros en una tabla que contengan el valor especificado en un campo de la tabla con los nuevos datos proporcionados. Recibe cuatro parámetros: el nombre de la tabla, el nombre del campo, el valor que se desea buscar y los nuevos datos en forma de diccionario.
