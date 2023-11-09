import sqlite3
import pandas 

# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('housing.db')

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Ejemplo de consulta SQL para leer datos de la tabla y convertirlos en un DataFrame de pandas
consulta_sql = 'SELECT * FROM california_housing_dataset'

# Ejecutar la consulta y obtener los resultados como una lista de tuplas
cursor.execute(consulta_sql)
resultados = cursor.fetchall()

# Obtener los nombres de las columnas a partir de la descripción del cursor
nombres_columnas = [descripcion[0] for descripcion in cursor.description]

# Crear un DataFrame de pandas a partir de los resultados y los nombres de las columnas
df = pandas.DataFrame(resultados, columns=nombres_columnas)

# Mostrar el DataFrame
print('DataFrame de usuarios:')
print(df)

# Cerrar la conexión
conexion.close()





def cargar_basededatos(file_name):
    conexion = sqlite3.connect('housing.db')
    cursor = conexion.cursor()


    consulta_sql = 'SELECT * FROM california_housing_dataset'
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()


    nombres_columnas = [descripcion[0] for descripcion in cursor.description]

    df = pandas.DataFrame(resultados, columns=nombres_columnas)


    print('DataFrame de usuarios:')
    print(df)

    conexion.close()