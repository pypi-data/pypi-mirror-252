"""
Created on Tue Jan 23 2024

@author: nmngo
@version: 0.1.1
"""

import pandas as pd
import joblib


class CompareModel:
    def __init__(self, path_wine_composition_weather_tree: str,
                 path_wine_text_review_tree: str):
        """
        Constructor
        :param path_wine_composition_weather_tree:
        :param path_wine_text_review_tree:
        """
        self.wine_composition_weather_tree = joblib.load(path_wine_composition_weather_tree)
        self.wine_text_review_tree = joblib.load(path_wine_text_review_tree)

    def query_data(self, input_wine_composition_and_weather, len_comp_weather: int,
                   input_wine_text_review=None, len_text_review: int = None):
        """
        Query the data
        :param input_wine_composition_and_weather:
        :param len_comp_weather:
        :param input_wine_text_review:
        :param len_text_review:
        :return: dist_composition_weather, ind_composition_weather, dist_text_review, ind_text_review
        """
        # Query the KD Tree, get the distances and indices of the nearest neighbors
        dist_composition_weather, ind_composition_weather = self.wine_composition_weather_tree.query(
            input_wine_composition_and_weather, k=len_comp_weather
        )
        if input_wine_text_review is not None and len_text_review is not None:
            dist_text_review, ind_text_review = self.wine_text_review_tree.query(
                input_wine_text_review, k=len_text_review
            )
        else:
            dist_text_review, ind_text_review = None, None
        return dist_composition_weather, ind_composition_weather, dist_text_review, ind_text_review
