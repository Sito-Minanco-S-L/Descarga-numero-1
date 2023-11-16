import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sqlite3
import PySimpleGUI as sg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import magic


def file_extension(file):
    """
    Obtiene la extensión de un archivo a partir de su nombre.

    Parameters:
    - file (str): Nombre del archivo.

    Returns:
    - str: Extensión del archivo.
    """
    L = file.split('.')
    return L[-1]

def interface(dfs:dict):

    layout1 = [
            [sg.Text('Selecciona un archivo', key='-hoola-')],
            [sg.InputText(key='-Archivo-', disabled=True), sg.FileBrowse('Browse',file_types=(("All Files", "*.*"),))],
            [sg.Button('Cargar Archivo'), sg.Button('Realizar Regresión Lineal'), sg.Button('Salir')],
            [sg.Text(key='--PRUEBA--')],
            [sg.AddMenuItem(key)]
        ]
    
    window = sg.Window('Aplicación de Regresión', layout1, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Archivo':

            window['-hoola-'].update(values['-Archivo-'])

        

           
      

dfs = {}
interface(dfs)
