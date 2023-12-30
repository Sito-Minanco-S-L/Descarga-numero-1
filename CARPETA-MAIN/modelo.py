from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pickle
import os

def load_model(pickle_file_name):
    """
    Carga un modelo previamente guardado desde un archivo pickle.

    Parameters:
    - pickle_file_name (str): Nombre del archivo pickle que contiene el modelo.

    Returns:
    - modelo: Modelo cargado desde el archivo pickle.
    """
    with open(pickle_file_name, "rb") as f:
        modelo = pickle.load(f)
    return modelo


class Modelo():
    def __init__(self, x_name, y_name,x ,y) -> None:
        """
        Inicializa una instancia de la clase Modelo.

        Parameters:
        - x_name (str): Nombre de la variable independiente (característica) en el eje x.
        - y_name (str): Nombre de la variable dependiente en el eje y.
        - x (DataFrame): Datos de la variable independiente.
        - y (Series): Datos de la variable dependiente.
        """
        self.x_name = x_name
        self.y_name = y_name
        self.x = x
        self.y = y
        self.modelo = self.make_model()

    
    def get_x_data(self):       
        return self.x
    
    def get_y_data(self):  
        return self.y
    
    def get_x_name(self):
        return self.x_name
    
    def get_y_name(self):
        return self.y_name
    
    def get_model(self):
        return self.modelo

    def get_coefficients(self):
        return self.modelo.params

    def columns_names(self):
        return self.x.columns.tolist()

    def make_model(self):
        """
        Divide los datos en conjuntos de entrenamiento y prueba, agrega una constante a los datos de entrenamiento
        y ajusta un modelo de regresión lineal a los datos de entrenamiento.

        Returns:
        - model: Modelo de regresión lineal ajustado.
        """
        if len(self.x) < 2 or len(self.y) < 2: #conclusión obtenida de los test realizados
            raise ValueError("Se necesitan al menos dos puntos para ajustar un modelo de regresión lineal.")
        
        x_train, x_test, y_train, y_test = train_test_split(self.x,self.y,test_size=0.2,random_state=1234, shuffle=True)
        x_train = sm.add_constant(x_train)
        model = sm.OLS(endog=y_train, exog=x_train)
        model = model.fit()
        return model

    def save_model(self, file_name:str):
        """
        Guarda el modelo en un archivo pickle.

        Parameters:
        - file_name (str): Nombre del archivo pickle.
        """
        with open(file_name+'.pickle', 'wb') as f:
            pickle.dump(self, f)

    

def make_prediction(modelo, x:list):
    """
    Realiza una predicción utilizando el modelo de regresión lineal.

    Parameters:
    - modelo (Modelo): Objeto de la clase Modelo.
    - x (list): Lista de valores de las variables independientes para hacer una predicción.

    Returns:
    - result: Predicción realizada por el modelo para las variables independientes dadas.
    """
    


    result = modelo.get_coefficients()[0]
    for i in range(len(x)):
        result += ((modelo.get_coefficients()[i+1]) * int(x[i]))
    return result

 
    
    

