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

#Added population density values from GOV census
population_density = pd.DataFrame({
    'Borough': [
        'City of London', 'Westminster', 'Camden', 'Islington', 'Hackney', 
        'Tower Hamlets', 'Southwark', 'Lambeth', 'Wandsworth', 'Hammersmith and Fulham', 
        'Brent', 'Ealing', 'Haringey', 'Newham', 'Waltham Forest', 'Lewisham', 
        'Greenwich', 'Bexley', 'Bromley', 'Croydon', 'Sutton', 'Merton', 
        'Kingston upon Thames', 'Richmond upon Thames', 'Havering', 'Barking and Dagenham', 
        'Redbridge', 'Hillingdon', 'Harrow', 'Enfield', 'Barnet', 'Hounslow', 'Kensington and Chelsea'
    ],
    'Density': [
        4790, 11200, 12800, 13300, 16200, 15800, 9800, 10700, 10900, 
        11500, 8900, 8700, 10600, 10500, 9600, 9300, 8800, 6500, 
        6300, 7200, 5800, 6700, 5900, 5600, 5400, 6800, 6200, 5500, 
        5700, 5600, 5800, 6000, 14800 
    ]
})

