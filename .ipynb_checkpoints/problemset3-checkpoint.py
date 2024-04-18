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
    return None

# Exercise 2
import pandas as pd
# takes list argument of years and returns a concatenated dataframe of
# corresponding tabs in the parent company excel sheet and
# adds variable year that references year which data is pulled as well
# as removing any row that is entirely null values
def import_parent_companies(years: list) -> pd.DataFrame:
    return None

# Exercise 3
# takes a dataframe and column name argument, and returns an integer
# corresponding to the number of null values in that column
def n_null(df: pd.DataFrame, col: str) -> int:
    return None

# Exercise 4
# takes a concatenated dataframe of emission sheets and a concatenated
# dataframe of parent companies and returns a dataframe produced from
# left joining parent company data onto the EPA data using year and
# Facility ID key variables, subsetting the data to specific variables
# Facility Id, year, State, Industry Type (sectors), Total reported direct
# emissions, PARENT CO. STATE, PARENT CO. PERCENT OWNERSHIP, making them
# all lowercase
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    return None

# Exercise 5
# takes dataframe input with schema from clean_data and list of variables, producing
# minimum, median, mean, and maximum values for the variables, total reported direct
# emissions, and parent co. percent ownership. returns the data sorted by highest to
# lowest mean total reported direct emissions
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    return None