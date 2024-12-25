import unittest
import pandas as pd
import numpy as np
import geopandas as gpd
from sklearn.linear_model import LinearRegression
from scipy import stats
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import data_loading
import data_cleaning

class TestScript(unittest.TestCase):

    def setUp(self):
        # Setup sample data for testing
        self.sample_crime_data = pd.DataFrame({
            'Crime Category': ['THEFT', 'THEFT', 'BURGLARY'],
            'Subcategory': ['Sub1', 'Sub2', 'Sub3'],
            'BoroughName': ['Borough1', 'Borough2', 'Borough3'],
            '202308': [10, 20, 30],
            '202309': [15, 25, 35]
        })
        self.sample_population_density = pd.DataFrame({
            'Borough': ['Borough1', 'Borough2', 'Borough3'],
            'Density': [10000, 15000, 12000]
        })
        self.sample_theft_data = pd.DataFrame({
            'Borough': ['Borough1', 'Borough2'],
            'TheftCount': [25, 45]
        })
        self.sample_population_data = {
            'Borough1': 100000,
            'Borough2': 150000,
            'Borough3': 120000
        }
    
    def test_load_and_clean_data(self):
        # Mock data loading and cleaning process
        crime = self.sample_crime_data
        crime_clean = data_cleaning.clean_data(crime)
        self.assertIn('Crime Category', crime_clean.columns)
        self.assertIn('2023-08', crime_clean.columns)

    def test_merge_density_theft(self):
        # Test merging population density and theft data
        analysis_df = pd.merge(self.sample_population_density, self.sample_theft_data, on='Borough', how='inner')
        self.assertEqual(len(analysis_df), 2)
        self.assertIn('Density', analysis_df.columns)
        self.assertIn('TheftCount', analysis_df.columns)

    def test_correlation(self):
        # Test correlation calculation
        analysis_df = pd.merge(self.sample_population_density, self.sample_theft_data, on='Borough', how='inner')
        correlation, p_value = stats.pearsonr(analysis_df['Density'], analysis_df['TheftCount'])
        self.assertIsInstance(correlation, float)
        self.assertIsInstance(p_value, float)
    
    def test_linear_regression(self):
        # Test linear regression model
        analysis_df = pd.merge(self.sample_population_density, self.sample_theft_data, on='Borough', how='inner')
        X = analysis_df[['Density']].values.reshape(-1, 1)
        y = analysis_df['TheftCount'].values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(predictions.shape, y.shape)

if __name__ == '__main__':
    unittest.main(exit=False)
