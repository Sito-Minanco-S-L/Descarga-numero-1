import pandas as pd
import numpy as np
import sqlite3



#Patron de diseño------>Factor method

def file_extension(file):
    """
    Obtiene la extensión de un archivo a partir de su nombre.

    Parameters:
    - file (str): Nombre del archivo.

    Returns:
    - str: Extensión del archivo.
    """
    # Divide el nombre del archivo y retorna la última parte como extensión
    L = file.split('.')
    return L[-1]


class FileReaderFactory:
    @staticmethod
    def create_file_reader(extension):
        """
        Crea un lector de archivos según la extensión dada.

        Parameters:
        - extension (str): Extensión del archivo.

        Returns:
        - FileReader: Instancia del lector de archivos correspondiente.
        """
        if extension == 'xlsx':
            return ExcelFileReader()
        elif extension == 'csv':
            return CsvFileReader()
        elif extension == 'db':
            return DbFileReader()
        else:
            raise ValueError(f'Unsupported file extension: {extension}')

class ExcelFileReader:
    def read_file(self, selected_file, dfs):
        """
        Lee un archivo de Excel(xlsx) y almacena las columnas numéricas en un diccionario.

        Parameters:
        - selected_file (str): Ruta del archivo seleccionado.
        - dfs (dict): Diccionario que almacena los DataFrames resultantes.

        Returns:
        - None
        """
        df = pd.read_excel(selected_file)#Crea un DataFrame a partir del archivo seleccionado
        df_numeric = df.select_dtypes(include=[np.number])#Se crea un DataFrame solo con datos numericos
        dfs[selected_file] = df_numeric # Asigna el DataFrame resultante a la variable dfs[selected_file] en el diccionario de DataFrames

class CsvFileReader:
    def read_file(self, selected_file, dfs):
        """
        Lee un archivo CSV y almacena las columnas numéricas en un diccionario.

        Parameters:
        - selected_file (str): Ruta del archivo seleccionado.
        - dfs (dict): Diccionario que almacena los DataFrames resultantes.

        Returns:
        - None
        """
        df = pd.read_csv(selected_file)#Crea un DataFrame a partir del archivo seleccionado
        df_numeric = df.select_dtypes(include=[np.number])#Se crea un DataFrame solo con datos numericos
        dfs[selected_file] = df_numeric # Asigna el DataFrame resultante a la variable dfs[selected_file] en el diccionario de DataFrames

class DbFileReader:
    def read_file(self, selected_file, dfs):
        """
        Lee una base de datos SQLite y almacena las columnas numéricas en un diccionario.

        Parameters:
        - selected_file (str): Ruta del archivo seleccionado.
        - dfs (dict): Diccionario que almacena los DataFrames resultantes.

        Returns:
        - None
        """
        conexion = sqlite3.connect('housing.db')# Establece una conexión a la base de datos SQLite llamada 'housing.db'
        cursor = conexion.cursor() # Crea un cursor para ejecutar consultas SQL en la base de datos
        search_sql = 'SELECT * FROM california_housing_dataset' # Define la consulta SQL para seleccionar todos los registros de la tabla 'california_housing_dataset'
        cursor.execute(search_sql) # Ejecuta la consulta SQL
        results = cursor.fetchall() # Obteniene todos los resultados de la consulta
        columns_names = [depiction[0] for depiction in cursor.description] # Obtiene los nombres de las columnas de la tabla mediante la descripción del cursor
        df = pd.DataFrame(results, columns=columns_names) # Crea un DataFrame de pandas con los resultados de la consulta y los nombres de las columnas
        df_numeric = df.select_dtypes(include=[np.number])#Se crea un data frame solo con datos numericos
        dfs[selected_file] = df_numeric # Asigna el DataFrame resultante a la variable dfs[selected_file] en el diccionario de DataFrames
        conexion.close() # Cierra la conexión a la base de datos
 

def read_file(selected_file, dfs, extension):
    """
    Lee un archivo según su extensión y almacena las columnas numéricas en un diccionario.

    Parameters:
    - selected_file (str): Ruta del archivo seleccionado.
    - dfs (dict): Diccionario que almacena los DataFrames resultantes.
    - extension (str): Extensión del archivo.

    Returns:
    - None
    """
    file_reader = FileReaderFactory.create_file_reader(extension) # Utiliza una fábrica para crear un lector de archivos según la extensión del archivo seleccionado
    file_reader.read_file(selected_file, dfs) # Lee el archivo seleccionado y cargar los datos en el diccionario dfs





