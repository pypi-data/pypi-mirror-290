# project_software_entwicklung_2\ensemble_package\unit_testing.py
# Author: Florian Meier

import unittest
import numpy as np

from .regressor_class import Regressor


'''Dieses FIle enthält die in der Aufgabe definierten fünf unterschiedlichen Unit-Tests.
Die einzelnen Tests sind der Regressor-Klasse zugeordnet.
Die Tests sind im einzelnen:
- Exsixtieren die eingegebenen Regressor-Klassen-Namen? -> falschen reg.-Namen übergeben
- Werden nur numerische Input-Daten zugelassen? -> nicht-numerische Werte übergeben
- Werden nur Daten für X in Form eines Array zugelassen? -> tuple oder dict übergeben
- Funktioniert die Funktion predict() korrekt? -> predict anhand von Vorgabewerten testen (Fernseherpreis zu Bildschirmdiagonale)
- Funktioniert die Funktion score() korrekt? -> score anhand von Vorgabewerten testen (Fernseherpreis zu Bildschirmdiagonale)'''


class test_regressor(unittest.TestCase):

# set up the class for later use
    def setUp(self):
        reg_type = 'linear_regressor'
        self.reg_model = Regressor(reg_type)

        X_train = np.array([[32, 1], [40, 1], [43, 1], [43, 1], [55, 1], [55, 1]])  # Beispielwerte für Bildschirmdiagonale
        y_train = np.array([361.90, 209.99, 259.99, 349, 459, 449])                 # Beispielwerte für Fernseherpreis
        self.reg_model.fit(X_train, y_train)


# test 1: check wether choosen regressor is available
    def test_input_string(self):
        self.assertEqual(str(self.reg_model.model), 'LinearRegression()', 'The given name is not a possible regressor')


# test 2: check a non-numerical input
    def test_non_numerical_input(self):
        input_X = [1, 2, 3]
        y = [1, 2 , 3]
        with self.assertRaises(ValueError):
            self.reg_model.fit(input_X, y)


# test 3: check a unregular input (dict)
    def test_irregular_input(self):
        input_dict = {'car': 'Ford Mondeo', 'mileage': 100000, 'prize': 42000}
        y = [1, 2 , 3]
        
        with self.assertRaises(ValueError):
            self.reg_model.fit(input_dict, y)

# test 4: check predicted output
    def test_predict_function(self):
        X_test = np.array([[40, 1], [55, 1], [65, 1]])  # Beispielwerte für Bildschirmdiagonale
        pred = self.reg_model.predict(X_test)
        self.assertEqual(len(pred), len(X_test), 'The predictions have an error')


# test 5: check wether score is working
    def test_score_function(self):
        X_test = np.array([[32, 1], [40, 1], [43, 1]])  # Beispielwerte für Bildschirmdiagonale
        y_test = np.array([361.90, 209.99, 259.99])  # Beispielwerte für Bildschirmdiagonale
        score = self.reg_model.score(X_test, y_test)
        in_boundaries = score <= 1
        self.assertTrue(in_boundaries, 'The score seems to be irregular')


if __name__ == '__main__':
    unittest.main()