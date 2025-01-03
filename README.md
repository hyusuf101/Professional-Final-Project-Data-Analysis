# London Borough Crime Analysis

This project analyses crime data in London boroughs, focusing on theft incidents and their relationship with population density and population size. The analysis uses Python libraries for data manipulation, statistical analysis, and visualisation.

## Project Overview

This project aims to:
1. Load and clean crime data.
2. Visualise population density and theft occurrences by borough.
3. Analyse the relationship between population density and theft incidents.
4. Calculate theft incidents per capita.
5. Perform linear regression to predict theft incidents based on population density.

## Setup Instructions

### Prerequisites
To run this analysis, you need to have the following Python libraries installed:

- pandas
- numpy
- geopandas
- matplotlib
- seaborn
- scipy
- scikit-learn 
- fiona==1.8.21

You can install these libraries using pip:
```sh
pip install pandas numpy geopandas matplotlib seaborn scipy scikit-learn
```
### Clone Repository

1. Clone the repository to your local machine:
```sh
    git clone https://github.com/github_username/Professional-Final-Project-Data-Analysis.git
```

2. Change to directory
```sh
    cd Professional-Final-Project-Data-Analysis/data
```
 
3. Run analysis 
```sh
    python data_analysis.py
 ```

This script will:

1. Load and clean the crime data.

2. Merge population density and crime data.

3. Perform statistical analysis.

3. Generate visualizations.

## Data Sources
1. Crime Data: Metropolitan Police Service

2. Population Density: UK Government Census

3. GeoData: London Borough Boundaries (GIS)

