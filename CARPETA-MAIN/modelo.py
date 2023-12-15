from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pickle


def load_model(pickle_file_name):
    with open(pickle_file_name, "rb") as f:
        model = pickle.load(f)
    return model


class Model():
    def __init__(self, x_name, y_name,x ,y) -> None:
        self.x_name = x_name
        self.y_name = y_name
        self.x = x
        self.y = y
        self.model = self.make_model()

    def make_model(self):
        x_train, x_test, y_train, y_test = train_test_split(self.x,self.y,test_size=0.2,random_state=1234, shuffle=True)
        x_train = sm.add_constant(x_train)
        model = sm.OLS(end_og=y_train, execute_og=x_train)
        model = model.fit()
        return model
    
    def get_x_data(self):
        return self.x
    
    def get_y_data(self):
        return self.y
    
    def get_x_name(self):
        return self.x_name
    
    def get_y_name(self):
        return self.y_name
    
    def save_model(self, file_name:str):
        with open(file_name+'.pickle', 'wb') as f:
            pickle.dump(self, f)

    def get_model(self):
        return self.model

