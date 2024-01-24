"""
Created on Tue Jan 23 2024

@author: nmngo
@version: 0.1.1
"""

import pandas as pd


class CompareDataProcessor:
    def __init__(self, path_pertinent_wine_ratings: str,
                 path_normalized_wine_data: str,
                 path_pertinent_ratings_non_null: str,
                 path_aggregated_doc_vector: str):
        """
        Constructor
        :param path_pertinent_wine_ratings:
        :param path_normalized_wine_data:
        :param path_pertinent_ratings_non_null:
        :param path_aggregated_doc_vector:
        """
        self.pertinent_wine_ratings = pd.read_parquet(path_pertinent_wine_ratings)
        self.normalized_wine_data = pd.read_parquet(path_normalized_wine_data)
        self.pertinent_ratings_non_null = pd.read_parquet(path_pertinent_ratings_non_null)
        self.aggregated_doc_vector = pd.read_csv(path_aggregated_doc_vector)

    def process_data(self, wine_id: int, vintage: int):
        """
        Process the data
        :param wine_id: Identifier of the wine from X-Wines dataset
        :param vintage:
        :return: tuple of input_wine_composition_and_weather, input_wine_text_review
        """
        checked_exist_df = self.pertinent_wine_ratings[(self.pertinent_wine_ratings['WineID'] == wine_id) &
                                                       (self.pertinent_wine_ratings['Vintage'] == vintage)]
        if checked_exist_df.empty:
            raise Exception('wine_id and vintage must be valid')
        reference_wine_composition_and_weather = self.normalized_wine_data[
            (self.normalized_wine_data['WineID'] == wine_id) &
            (self.normalized_wine_data['Vintage'] == vintage)]
        input_wine_composition_and_weather = reference_wine_composition_and_weather.drop(
            ['WineID', 'Vintage', 'WineName'],
            axis=1).to_numpy().reshape(1, -1)
        checked_review_df = self.pertinent_ratings_non_null[(self.pertinent_ratings_non_null['WineID'] == wine_id) &
                                                            (self.pertinent_ratings_non_null['Vintage'] == vintage)]

        if not checked_review_df.empty:
            # There is at least one text review
            reference_wine_text_review = self.aggregated_doc_vector[(self.aggregated_doc_vector['WineID'] == wine_id) &
                                                                    (self.aggregated_doc_vector['Vintage'] == vintage)]

            input_wine_text_review = reference_wine_text_review.drop(['WineID', 'Vintage'], axis=1).to_numpy().reshape(
                1, -1)
        else:
            # There is no text review
            input_wine_text_review = None
        return input_wine_composition_and_weather, input_wine_text_review
