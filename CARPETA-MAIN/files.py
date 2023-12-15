import pandas as pd
import numpy as np
import sqlite3
import PySimpleGUI as sg

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
        nombres_columnas = [descripcion[0] for descripcion in cursor.description]
        df = pd.DataFrame(results, columns=nombres_columnas)
                        
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        conexion.close()
        print(sg.popup_auto_close('¡Archivo cargado con éxito!'))




'''
Patrones de Diseño----->

class FileReaderFactory:
    @staticmethod
    def create_file_reader(extension):
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
        df = pd.read_excel(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        print(sg.popup_auto_close('¡Archivo de Excel cargado con éxito!'))

class CsvFileReader:
    def read_file(self, selected_file, dfs):
        df = pd.read_csv(selected_file)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        print(sg.popup_auto_close('¡Archivo CSV cargado con éxito!'))

class DbFileReader:
    def read_file(self, selected_file, dfs):
        conexion = sqlite3.connect('housing.db')
        cursor = conexion.cursor()
        search_sql = 'SELECT * FROM california_housing_dataset'
        cursor.execute(search_sql)
        results = cursor.fetchall()
        nombres_columnas = [descripcion[0] for descripcion in cursor.description]
        df = pd.DataFrame(results, columns=nombres_columnas)
        df_numeric = df.select_dtypes(include=[np.number])
        dfs[selected_file] = df_numeric
        conexion.close()
        print(sg.popup_auto_close('¡Archivo de Base de Datos cargado con éxito!'))

def read_file(selected_file, dfs, extension):
    file_reader = FileReaderFactory.create_file_reader(extension)
    file_reader.read_file(selected_file, dfs)
    '''