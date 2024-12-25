import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression

import data_loading
import data_cleaning
import os #for directory filepath


# Get the root directory of the project
root_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data file
data_path = os.path.join(root_dir, 'data', 'MPS Borough Level Crime (most recent 24 months).csv')

# Load data
crime = data_loading.load_data(data_path)

# Clean data
clean_data = data_cleaning.clean_data(crime)

