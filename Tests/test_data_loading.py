import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from data_loading import load_data

class TestLoadData(unittest.TestCase):

    def setUp(self):
        # Create a sample CSV file for testing
        self.test_file = 'test_data.csv'
        self.test_data = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': ['A', 'B', 'C']
        })
        self.test_data.to_csv(self.test_file, index=False)

    def tearDown(self):
        # Remove the test CSV file after tests are done
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_data(self):
        # Test if the data is loaded correctly
        loaded_data = load_data(self.test_file)
        pd.testing.assert_frame_equal(loaded_data, self.test_data)

    def test_file_not_found(self):
        # Test if the function handles non-existing file correctly
        with self.assertRaises(FileNotFoundError):
            load_data('non_existent_file.csv')

if __name__ == '__main__':
    unittest.main()
