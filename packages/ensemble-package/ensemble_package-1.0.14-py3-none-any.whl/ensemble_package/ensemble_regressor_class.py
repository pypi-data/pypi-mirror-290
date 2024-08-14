# project_software_entwicklung_2\ensemble_package\ensemble_regressor_class.py
# Author: Florian Meier


import numpy as np

from .regressor_class import Regressor

# Ensemble-Klasse

class Ensemble():
    '''Diese Klasse soll ein Ensemble aus mehreren einzelnen Regressoren bilden.
    Die möglichen Regressoren sind:
    - linear_regressor
    - nearest_neighbor_regressor
    - ridge_regressor
    
    Die verfügbaren Funktionen sind:
    fit()
    predict()
    fit_predict()
    score()'''


    def __init__(self, input_list):
        self.ensemble = [Regressor(regressor) for regressor in input_list]

    def fit(self, X, y):
        for regressor in self.ensemble:
            regressor.fit(X , y)

    def predict(self, X):
        predictions = np.array([regressor.predict(X) for regressor in self.ensemble])
        return np.mean(predictions, axis=0)

    def fit_predict(self, X, y, Z):
        for regressor in self.ensemble:
            regressor.fit(X , y)
        
        predictions = np.array([regressor.predict(Z) for regressor in self.ensemble])
        return np.mean(predictions, axis=0)

    def score(self, X, y):
        single_scores = np.array([regressor.score(X, y) for regressor in self.ensemble])
        return np.mean(single_scores, axis=0)
    
