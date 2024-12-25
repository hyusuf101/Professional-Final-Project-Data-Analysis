import unittest
import pandas as pd
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from data_cleaning import clean_data

class TestCleanData(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing with specified date columns
        self.test_data = pd.DataFrame({
            'A': ['Crime1', 'Crime2', None],
            'B': ['Sub1', 'Sub2', 'Sub3'],
            'BoroughName': ['Borough1', 'Borough2', 'Borough3'],
            '202308': [10, 20, 30],
            '202309': [15, 25, 35]
        })

        self.expected_data = pd.DataFrame({
            'Crime Category': ['Crime1', 'Crime2'],
            'Subcategory': ['Sub1', 'Sub2'],
            'Borough': ['Borough1', 'Borough2'],
            '2023-08': [10, 20],
            '2023-09': [15, 25]
        })

    def test_clean_data(self):
        # Test if the data is cleaned correctly
        cleaned_data = clean_data(self.test_data)
        pd.testing.assert_frame_equal(cleaned_data.reset_index(drop=True), self.expected_data)

if __name__ == '__main__':
    unittest.main(exit=False)



