import pandas as pd
import numpy as np
import sqlite3
import PySimpleGUI as sg


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
        df = pd.read_excel(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric

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
        df = pd.read_csv(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        print(sg.popup_auto_close('¡Archivo CSV cargado con éxito!'))

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
        conexion = sqlite3.connect('housing.db')
        cursor = conexion.cursor()
        search_sql = 'SELECT * FROM california_housing_dataset'
        cursor.execute(search_sql)
        results = cursor.fetchall()
        columns_names = [depiction[0] for depiction in cursor.description]
        df = pd.DataFrame(results, columns=columns_names)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        conexion.close()
        print(sg.popup_auto_close('¡Archivo de Base de Datos cargado con éxito!'))

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
    file_reader = FileReaderFactory.create_file_reader(extension)
    file_reader.read_file(selected_file, dfs)






'''
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

def read_file(selected_file, dfs:dict, extension):
   
    if extension == 'xlsx': #para leer archivos .xlsx
        df = pd.read_excel(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        file_content = df_numeric.to_string(index=False)
        dfs[selected_file] = df_numeric
        print(sg.popup_auto_close('¡Archivo cargado con éxito!'))
   
    if extension == 'csv': #para leer archivos .csv
        df = pd.read_csv(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        file_content = df_numeric.to_string(index=False)
        dfs[selected_file] = df_numeric
        print(sg.popup_auto_close('¡Archivo cargado con éxito!'))
    
    if extension == 'db': #para leer archivos .db
        conexion = sqlite3.connect('housing.db')
        cursor = conexion.cursor()
        search_sql = 'SELECT * FROM california_housing_dataset'
        cursor.execute(search_sql)
        results = cursor.fetchall()
        columns_names = [depiction[0] for depiction in cursor.description]
        df = pd.DataFrame(results, columns=columns_names)
                        
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        conexion.close()
        print(sg.popup_auto_close('¡Archivo cargado con éxito!'))
'''