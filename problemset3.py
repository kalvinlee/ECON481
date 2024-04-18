# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 3

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset3.py"

# Exercise 1
import pandas as pd
# takes list argument of years and returns a concatenated dataframe of
# direct emitters tab of each of those year's EPA excel sheet and
# adds variable year that references year which data is pulled
def import_yearly_data(years: list) -> pd.DataFrame:
    data = [] # creates empty dataframe to return
    for year in years:
        # saves url depending on year chosen
        url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        # creates dataframe based on year skipping the first 3 rows as specified
        df = pd.read_excel(url, sheet_name = 'Direct Emitters', skiprows = 3, index_col = None)
        # adds year column equates it to year in list
        df['year'] = year
        data.append(df)
    return pd.concat(data)

# Exercise 2
import pandas as pd
# pip install pyxlsb
# takes list argument of years and returns a concatenated dataframe of
# corresponding tabs in the parent company excel sheet and
# adds variable year that references year which data is pulled as well
# as removing any row that is entirely null values
def import_parent_companies(years: list) -> pd.DataFrame:
    data2 = [] # creates empty dataframe to return
    url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"
    for year in years:
        # reads and stores excel sheet based on year
        df = pd.read_excel(url, sheet_name = str(year), engine = 'pyxlsb')
        # adds year column equates it to year in list
        df['year'] = year
        data2.append(df)
    # concatenates dataframe
    concat_data2 = pd.concat(data2)
    # removes any row that is entirely null values
    concat_data2.dropna(how = 'all', inplace = True)
    return concat_data2

# Exercise 3
# takes a dataframe and column name argument, and returns an integer
# corresponding to the number of null values in that column
def n_null(df: pd.DataFrame, col: str) -> int:
    return df[col].isna().sum()

# Exercise 4
# takes a concatenated dataframe of emission sheets and a concatenated
# dataframe of parent companies and returns a dataframe produced from
# left joining parent company data onto the EPA data using year and
# Facility ID key variables, subsetting the data to specific variables
# Facility Id, year, State, Industry Type (sectors), Total reported direct
# emissions, PARENT CO. STATE, PARENT CO. PERCENT OWNERSHIP, making them
# all lowercase
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    # merges data based on keys Facility Id and year
    merge_data = pd.merge(emissions_data, parent_data, left_on = ['year', 'Facility Id'], 
                          right_on = ['year', 'GHGRP FACILITY ID'], how = 'left')
    # subsets the data to specific variables
    sset_data = merge_data[['Facility Id', 'year', 'State', 'Industry Type (sectors)', 
                          'Total reported direct emissions', 'PARENT CO. STATE', 
                          'PARENT CO. PERCENT OWNERSHIP']]
    # sets dataframe to lowercase column names
    sset_data.columns = sset_data.columns.str.lower()
    return sset_data

# Exercise 5
# takes dataframe input with schema from clean_data and list of variables, producing
# minimum, median, mean, and maximum values for the variables, total reported direct
# emissions, and parent co. percent ownership. returns the data sorted by highest to
# lowest mean total reported direct emissions
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    # creates aggregate variables list
    aggregate_vars = ['total reported direct emissions', 'parent co. percent ownership']
    # groups based on inputted list the min, median, mean and max
    aggregate_data = df.groupby(group_vars)[aggregate_vars].agg(['min', 'median', 'mean', 'max'])
    # sorts dataframe from highest to lowest based on mean total reported direct emissions
    sorted_data = aggregate_data.sort_values(by = ('total reported direct emissions', 'mean'), ascending = False)
    return sorted_data