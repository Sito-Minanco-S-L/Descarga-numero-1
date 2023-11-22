def regression_interface(dfs, selected_file):
    """
    Interfaz gráfica para realizar una regresión lineal múltiple.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    - selected_file (str): Nombre del archivo seleccionado.
    """
    df = dfs[selected_file]
    columnas = list(df.columns)

    sg.theme('DarkGrey2')

    layout = [
        [sg.Text('Regresión Lineal Múltiple', font=('Helvetica', 20), justification='center')],
        [sg.Text('Seleccione las variables predictoras:', font=('Helvetica', 12), size=(25, 1)),
         sg.Listbox(values=columnas, select_mode='extended', size=(20, len(columnas)), key='predictoras')],#para poder poner el desplegable abierto y seleccionar varios a la vez
        [sg.Text('Seleccione la variable a predecir:', font=('Helvetica', 12), size=(25, 1)),
         sg.InputCombo(values=columnas, key='predecir')],
        [sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green')),
         sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],
    ]

    window = sg.Window('Regresión Lineal Múltiple', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
        elif event == 'Realizar Regresión Lineal':
            predictoras = values['predictoras']
            predecir = values['predecir']

            X = df[predictoras]
            Y = df[predecir]

            X_train, X_test, y_train, y_test = train_test_split(X,
                                                                Y,
                                                                test_size=0.2,
                                                                random_state=1234,
                                                                shuffle=True)
            X_train = sm.add_constant(X_train, prepend=True)
            modelo = sm.OLS(endog=y_train, exog=X_train)
            modelo = modelo.fit()

            mostrar_resultados(modelo)

    window.close()