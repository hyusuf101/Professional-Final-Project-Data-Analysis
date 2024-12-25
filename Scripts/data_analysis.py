import pandas as pd
import numpy as np
import geopandas as gpd

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

import seaborn as sns

from scipy import stats

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

# Create a dictionary of London borough populations (2021 census data)
population_data = {
    'Barking and Dagenham': 212906,
    'Barnet': 395869,
    'Bexley': 247258,
    'Brent': 339800,
    'Bromley': 330795,
    'Camden': 270029,
    'City of London': 10938,
    'Croydon': 386710,
    'Ealing': 367100,
    'Enfield': 333869,
    'Greenwich': 286186,
    'Hackney': 281120,
    'Hammersmith and Fulham': 183544,
    'Haringey': 266357,
    'Harrow': 261348,
    'Havering': 259552,
    'Hillingdon': 309300,
    'Hounslow': 288234,
    'Islington': 245827,
    'Kensington and Chelsea': 156864,
    'Kingston upon Thames': 177507,
    'Lambeth': 318000,
    'Lewisham': 305309,
    'Merton': 206186,
    'Newham': 352005,
    'Redbridge': 303858,
    'Richmond upon Thames': 198019,
    'Southwark': 318830,
    'Sutton': 206349,
    'Tower Hamlets': 319056,
    'Waltham Forest': 276983,
    'Wandsworth': 329677
}

gdf_path = os.path.join(root_dir, 'statistical-gis-boundaries-london', 'ESRI', 'London_Borough_Excluding_MHW.shp')

# Load the GeoDataFrame
gdf = gpd.read_file(gdf_path)

# Heatmap for Population Density by borough
fig, ax3 = plt.subplots(1, 1, figsize=(5, 5))

# Plot: Population Density
london_density = gdf.merge(population_density, on='Borough', how='left')
density_plot = london_density.plot(column='Density', 
                                   ax=ax3,
                                   legend=True,
                                   legend_kwds={'label': 'Population Density (people per sq km)'},
                                   cmap='YlOrRd',
                                   missing_kwds={'color': 'lightgrey'})
ax3.set_axis_off()
ax3.set_title('Population Density by Borough', pad=20)



# Print statistics
print("Top 5 Boroughs by Population Density:")
print(population_density.nlargest(5, 'Density')[['Borough', 'Density']])

# Filter the dataset for theft-related crimes and aggregate by borough
theft_data = crime[crime['Crime Category'] == 'THEFT'].groupby('Borough')[crime.columns[-1]].sum().reset_index()
theft_data.columns = ['Borough', 'TheftCount']

# Create figure for Theft Occurrences
fig, ax4 = plt.subplots(1, 1, figsize=(5, 5))

# Plot 2: Theft Occurrences
london_theft = gdf.merge(theft_data, on='Borough', how='left')
theft_plot = london_theft.plot(column='TheftCount', 
                               ax=ax4,
                               legend=True,
                               legend_kwds={'label': 'Number of Theft Incidents'},
                               cmap='YlOrRd',
                               missing_kwds={'color': 'lightgrey'})
# ctx.add_basemap(ax4, source=ctx.providers.CartoDB.Positron, crs=gdf.crs.to_string(), alpha=0.5, verify=False)
ax4.set_axis_off()
ax4.set_title('Theft Occurrences by Borough', pad=20)


# Print statistics
print("Top 5 Boroughs by Theft Occurrences:")
print(theft_data.nlargest(5, 'TheftCount')[['Borough', 'TheftCount']])


# Merge density and theft data correctly
analysis_df = pd.merge(population_density, theft_data, on='Borough', how='inner')

# Exclude Westminster from the analysis
analysis_df = analysis_df[analysis_df['Borough'] != 'Westminster']

# Calculate correlation coefficient and p-value
correlation, p_value = stats.pearsonr(analysis_df['Density'], analysis_df['TheftCount'])

# Create scatter plot with regression line
plt.figure(figsize=(12, 8))
sns.regplot(data=analysis_df, x='Density', y='TheftCount', scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})

# Add borough labels for top theft locations
for idx, row in analysis_df.nlargest(5, 'TheftCount').iterrows():
    plt.annotate(row['Borough'], 
                (row['Density'], row['TheftCount']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=9)

# Add correlation information to plot
plt.title('Correlation between Population Density and Theft Incidents')
plt.xlabel('Population Density (people per sq km)')
plt.ylabel('Number of Theft Incidents')
plt.text(0.05, 0.95, f'Correlation coefficient: {correlation:.2f}\n\
p-value: {p_value:.4f}', 
         transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

# Print p-value and correlation coefficient separately
print(f"Correlation coefficient: {correlation:.2f}")
print(f"p-value: {p_value:.4f}")

# Convert population data to DataFrame
population_df = pd.DataFrame(list(population_data.items()), columns=['Borough', 'Population'])

# Merge population data with existing analysis_gdf
analysis_gdf = gdf.merge(theft_data, on='Borough', how='left')
analysis_gdf = analysis_gdf.merge(population_df, on='Borough', how='left')

# Calculate theft per capita
analysis_gdf['TheftPerCapita'] = (analysis_gdf['TheftCount'] / analysis_gdf['Population']) * 1000  # per 1000 residents
top_10_per_capita = analysis_gdf.nlargest(10, 'TheftPerCapita')

# Create the horizontal bar chart
plt.figure(figsize=(12, 8))
bars = plt.barh(top_10_per_capita['Borough'], top_10_per_capita['TheftPerCapita'])
plt.title('Top 10 Boroughs - Theft Incidents per 1,000 Residents')
plt.xlabel('Theft Incidents per 1,000 Residents')
plt.ylabel('Borough')

# Add value labels on the bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, 
             f'{width:.1f}', 
             ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.show()

# Print statistics
print("Correlation between Population and Theft Incidents:")
print(analysis_gdf['Population'].corr(analysis_gdf['TheftCount']))

print("Top 5 Boroughs by Theft per 1,000 Residents:")
print(top_10_per_capita[['Borough', 'TheftPerCapita']].head().to_string())

# Merge density and theft data correctly
analysis_df = pd.merge(population_density, theft_data, on='Borough', how='inner')
analysis_df = pd.merge(analysis_df, population_df, on='Borough', how='inner')

# Exclude Westminster from the analysis
analysis_df = analysis_df[analysis_df['Borough'] != "Westminster"]

# Perform linear regression analysis using scikit-learn
X = analysis_df[['Density']].values.reshape(-1, 1)
y = analysis_df['TheftCount'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Get the model coefficients
coefficient = model.coef_[0][0]
intercept = model.intercept_[0]

# Print the model summary
print(f"Coefficient: {coefficient}")
print(f"Intercept: {intercept}")

# Make predictions using the model
predictions = model.predict(X)

# Print predictions
print("Predictions:", predictions.flatten())