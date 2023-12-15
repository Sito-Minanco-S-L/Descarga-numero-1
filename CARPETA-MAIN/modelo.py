from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pickle


def cargar_modelo(pickle_file_name):
    with open(pickle_file_name, "rb") as f:
        modelo = pickle.load(f)
    return modelo


class Modelo():
    def __init__(self, x_name, y_name,x ,y) -> None:
        self.x_name = x_name
        self.y_name = y_name
        self.x = x
        self.y = y
        self.modelo = self.make_modelo()

    def make_modelo(self):
        x_train, x_test, y_train, y_test = train_test_split(self.x,self.y,test_size=0.2,random_state=1234, shuffle=True)
        x_train = sm.add_constant(x_train)
        modelo = sm.OLS(endog=y_train, exog=x_train)
        modelo = modelo.fit()
        return modelo
    
    def get_x_data(self):
        return self.x
    
    def get_y_data(self):
        return self.y
    
    def get_x_name(self):
        return self.x_name
    
    def get_y_name(self):
        return self.y_name
    
    def guardar(self, file_name:str):
        with open(file_name+'.pickle', 'wb') as f:
            pickle.dump(self, f)

    def get_modelo(self):
        return self.modelo

