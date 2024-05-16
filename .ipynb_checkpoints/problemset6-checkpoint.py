# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 6

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset6.py"

# Exercise 1
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, outputting a table that has two columns: itemId and std, only including 
    # bids for which the unbiased standard deviation can be calculated which follows the
    # equation s={\sqrt {\frac {\sum _{i=1}^{n}(x_{i}-{\overline {x}})^{2}}{n-1}}}
def std() -> str:
    
    return None

# Exercise 2
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, that outputs a table wil four columns of bidderName, total_spend, total_bids
    # spend_frac
def bidder_spend_frac() -> str:

    return None

# Exercise 3
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, that outputs a table that has one column, freq, which represents the fraction
    # of bids that are exactly the minimum bid increment above the previous high bid, excluding items
    # where isBuyNowUsed = 1
def min_increment_freq() -> str:

    return None

# Exercise 4
    # takes no arguments, and returns a string containing a SQL query that can be run against the
    # auctions database that outputs a table that has two columns, timestamp_bin: normalize the
    # bid timestamp and classify it as one of ten bins. ex: 1 corresponds to 0-0.1, 2 to 0.1-0.2 etc.
    # and win_perc: the frequency with which a bid placed with this timestamp bin won the auction
def win_perc_by_timestamp() -> str:

    return None