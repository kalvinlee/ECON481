# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 4

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset4.py"

# Exercise 1
import pandas as pd
# accesses file on Tesla stock price history and returns that data as a dataframe
def load_data() -> pd.DataFrame:
    # saves file then returns it as dataframe
    url = "https://lukashager.netlify.app/econ-481/data/TSLA.csv"
    return pd.read_csv(url)

# Exercise 2
import matplotlib.pyplot as plt
# takes output from load_data as well as an optional start and end date
# formatted as 'YYYY-MM-DD' and plots the closing price of stock between dates
# as a line graph, including the data range in the title of the graph
def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    # collects dates from the dataset in date format
    df['Date'] = pd.to_datetime(df['Date'])
    # filters out based on inputted dates to locate range of data
    df_filter = df.loc[(df['Date'] >= start) & (df['Date'] <= end)]
    # plots the data points
    ax = df_filter.plot(x = 'Date', y = 'Close', color = 'purple')
    # labels
    ax.set_title(f"Tesla Stock Closing Price ({start} to {end})")
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')    
    
# Exercise 3
import statsmodels.api as sm
# takes a dataframe and returns the t statistic on beta_hat0 from the regression 
# Δx_t = beta0 * Δx_t-1 + εi, where x_t is the close price at time t and Δx_t = x_t - x_t-1
def autoregress(df: pd.DataFrame) -> float:
    # sets dates column in date format
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    # finds the differences between close dates
    df['Deltax'] = df['Close'].diff()
    # lags the dataset to compare consecutive days
    df['close_diff_lag'] = df['Deltax'].shift(1)
    # drops all none consecutive na days
    df.dropna(subset = ['close_diff_lag', 'Deltax'], inplace = True)
    X = df['close_diff_lag']
    y = df['Deltax']
    # OLS models and returns t-value
    model = sm.OLS(y,X).fit(cov_type = 'HC1')
    return model.tvalues['close_diff_lag']

# Exercise 4
# takes a single dataframe argument and returns the t statistic on beta_hat0 from the regression
# {P}(Δx_t > 0) = {exp(beta_0 * Δx_{t-1})}/{1 + exp(beta_0 * Δx_{t-1})}
def autoregress_logit(df: pd.DataFrame) -> float:
    # sets dates column in date format
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    # finds difference between close dates
    df['Deltax'] = df['Close'].diff()
    # creates outcome where y is the positive changes in x
    df['y'] = (df['Deltax'] > 0).astype(int)
    # creates lag dataset by one day
    df['Delta_lag'] = df['Deltax'].shift(1)
    df.dropna(subset = ['Delta_lag', 'y'], inplace = True)
    X = df['Delta_lag']
    y = df['y']
    logit_model = sm.Logit(y,X).fit()
    return logit_model.tvalues['Delta_lag']

# Exercise 5
# takes a signle dataframe argument and plots Δx_t for the full dataset
def plot_delta(df: pd.DataFrame) -> None:
    df['delta_x'] = df['Close'].diff()
    ax = df.plot(y = 'delta_x', color = 'purple')
    ax.set_title('Tesla Stock Change in Close Price')
    ax.set_ylabel('Change in Price ($)')