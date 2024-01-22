
import imp

# load a source module from a file
file, pathname, description = imp.find_module('src', ['I:\\openclassroom\\projet7\\home-credit-develop\\'])
my_module = imp.load_module('src', file, pathname, description)

import pandas as pd
from src.models import retrieve_fit_model as rfm


def get_predictions(model, file_path):
    """Predict all data from test dataset using given model for classification.

    Keyword arguments:
    model -- chosen model
    file_path -- CSV file path
    """
    loaded_model = rfm.get_fit_mlflow_model(model)
    try:
        test = pd.read_csv(file_path)
        y_pred = loaded_model.predict(test)
        return y_pred
    except Exception:
        print('Given CSV file path ' + file_path + ' not found.')