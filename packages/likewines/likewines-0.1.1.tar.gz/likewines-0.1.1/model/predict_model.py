"""
Created on Tue Jan 23 2024

@author: nmngo
@version: 0.1.1
"""

from tensorflow.keras.models import load_model


class PredictModel:
    def __init__(self, path_cnn_model: str):
        """
        Constructor
        :param path_cnn_model:
        """
        self.cnn_model = load_model(path_cnn_model)

    def predict(self, time_series_input, numerical_input):
        """
        Predict the data
        :param time_series_input:
        :param numerical_input:
        :return: list_predict_rating
        """
        predictions = self.cnn_model.predict([time_series_input, numerical_input])
        # Return the prediction
        list_predict_rating = predictions.tolist()
        list_predict_rating = [item for sublist in list_predict_rating for item in sublist]
        list_predict_rating = [float(item) for item in list_predict_rating]
        return list_predict_rating
