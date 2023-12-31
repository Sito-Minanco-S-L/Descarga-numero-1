import regression
import pytest


def test_convert_text_to_image_multi(): #se testea la conversión de textos a imágenes en formato '.png'.
    text = 'holaholahola*__123'
    assert regression.convert_text_to_image(text).endswith('.png')

    text = ''
    assert regression.convert_text_to_image(text).endswith('.png')

def test_interpret_r_squared(): #se testea la interpretación de resultados de la 'R_squared'.
    result = regression.interpret_r_squared(2)
    assert type(result) == tuple
    result = regression.interpret_r_squared(0.8)
    assert type(result) == tuple
    result = regression.interpret_r_squared(0.9)
    assert type(result) == tuple
    result = regression.interpret_r_squared(0.5)
    assert type(result) == tuple
    result = regression.interpret_r_squared(0.3)
    assert type(result) == tuple
    result = regression.interpret_r_squared(0)
    assert type(result) == tuple
    



