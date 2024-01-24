"""
Created on Tue Jan 23 2024

@author: nmngo
@version: 0.1.1
"""

import pandas as pd
import joblib
import numpy as np


class PredictDataProcessor:
    def __init__(self, wine,
                 rating_year: int,
                 path_forecast_df: str,
                 batch_vintage: list,
                 path_minmax_scaler: str,
                 path_standard_scaler: str):
        """
        Constructor
        :param wine:
        :param rating_year:
        :param path_forecast_df:
        :param batch_vintage:
        :param path_minmax_scaler:
        :param path_standard_scaler:
        """
        self.wine = wine
        self.rating_year = rating_year
        forecast_df = pd.read_parquet(path_forecast_df)
        region = self.wine.region
        self.forecast_df = forecast_df[forecast_df['RegionID'] == region.region_id]
        self.batch_vintage = batch_vintage
        with open(path_minmax_scaler, 'rb') as f:
            self.minmax_scaler = joblib.load(f)
        with open(path_standard_scaler, 'rb') as f:
            self.standard_scaler = joblib.load(f)

    def process_data(self):
        """
        Process the data
        :return: time_series_input, numerical_input
        """
        length = len(self.batch_vintage) * 12
        column_minmax = ['ABV', 'Body', 'Acidity',
                         'avg_temperature', 'avg_sunshine_duration',
                         'avg_precipitation', 'avg_humidity',
                         'avg_soil_temperature', 'avg_soil_moisture']
        minmax_df = pd.DataFrame(columns=column_minmax)
        minmax_df['ABV'] = [self.wine.abv] * length
        minmax_df['Body'] = [self.wine.body] * length
        minmax_df['Acidity'] = [self.wine.acidity] * length
        minmax_df['avg_temperature'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_temperature'].tolist()
        minmax_df['avg_sunshine_duration'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_sunshine_duration'].tolist()
        minmax_df['avg_precipitation'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_precipitation'].tolist()
        minmax_df['avg_humidity'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_humidity'].tolist()
        minmax_df['avg_soil_temperature'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_soil_temperature'].tolist()
        minmax_df['avg_soil_moisture'] = self.forecast_df[self.forecast_df['year'].isin(self.batch_vintage)][
            'avg_soil_moisture'].tolist()

        acid_dict = {'Low': 1, 'Medium': 2, 'High': 3}
        body_dict = {'Light-bodied': 1, 'Medium-bodied': 2, 'Full-bodied': 3, 'Very full-bodied': 4}

        minmax_df['Acidity'] = minmax_df['Acidity'].map(acid_dict)
        minmax_df['Body'] = minmax_df['Body'].map(body_dict)
        # Duplicate each element in batch_vintage 12 times
        list_vintage = np.repeat(self.batch_vintage, 12)
        list_delta_time_rating = np.array(self.rating_year - np.array(list_vintage))
        # Convert list_delta_time_rating to list
        list_delta_time_rating = list_delta_time_rating.tolist()

        scaled_minmax_df = self.minmax_scaler.transform(minmax_df)
        scaled_list_delta_time_rating = self.standard_scaler.transform(np.array(list_delta_time_rating).reshape(-1, 1))

        list_all = []
        for i in range(0, length, 12):
            time_series_array = np.array([scaled_minmax_df[:, 3][i:i + 12],
                                          scaled_minmax_df[:, 4][i:i + 12],
                                          scaled_minmax_df[:, 5][i:i + 12],
                                          scaled_minmax_df[:, 6][i:i + 12],
                                          scaled_minmax_df[:, 7][i:i + 12],
                                          scaled_minmax_df[:, 8][i:i + 12]])
            numerical_array = np.array([scaled_minmax_df[:, 0][i], scaled_minmax_df[:, 1][i],
                                        scaled_minmax_df[:, 2][i],
                                        scaled_list_delta_time_rating[i][0]])
            list_all.append((time_series_array, numerical_array))

        # Input data for CNN model
        time_series_input = np.array([element[0] for element in list_all])
        time_series_input = time_series_input.reshape(time_series_input.shape[0], time_series_input.shape[1],
                                                      time_series_input.shape[2], 1)
        numerical_input = np.array([element[1] for element in list_all])
        return time_series_input, numerical_input
