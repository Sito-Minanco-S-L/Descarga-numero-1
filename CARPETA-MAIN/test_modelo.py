import modelo
from modelo import Modelo
import pytest
import os

def test_load_model():
    
    directorio = 'c:\****\****\******\*****'#ruta del directorio donde se encuentran los archivos
    archivo1 = 'modelo1.flp.pickle'
    ruta = os.path.join(directorio, archivo1)
    assert os.path.isfile(ruta) and modelo.load_model(archivo1) != None
    
    archivo2 = 'modelo2.flp.pickle'
    ruta = os.path.join(directorio, archivo2)
    assert os.path.isfile(ruta) and modelo.load_model(archivo2) != None



@pytest.mark.parametrize(
    "dirigida, directora, x, y",

    [
        ("dirigida", "directora", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ("dirigida", "directora", [1.2, 3.5, 4.6, 7.99, 0], [1.2, 3.5, 4.6, 7.99, 0]),
        ("dirigida", "directora", [1.2, 0], [1.2, 0.9]),
        ("dirigida", "directora", [1], [1])

    ]
)

def test_make_model(dirigida, directora, x, y):
    modelo_ = Modelo(dirigida, directora, x, y)
    model = modelo_.make_model()
    assert model != None
    
#con este test llegamos a que es necesario meter una condición para cuando 
#las variables seleccionadas contengan menos de 2 valores.


modelo1 = Modelo("dirigida", "directora", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
modelo2 = Modelo("dirigida", "directora", [1.2, 3.5, 4.6, 7.99, 0], [1.2, 3.5, 4.6, 7.99, 0]) 
modelo3 = Modelo("dirigida", "directora", [1.2, 0], [1.2, 0])


@pytest.mark.parametrize(
    "model, x",

    [
        (modelo1, [0]),
        (modelo2, [1.2]),
        #(modelo3, [1.2, 0]), mirar de testear con modelo de 3 variables

    ]
)

def test_make_prediction(model, x):
    
    assert modelo.make_prediction(model, x) is not None
#testing de las predicciones