# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 1

#exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset1.py"

#exercise 1
    # opened terminal and typed pip3 install <packagename> for
    # numpy, pandas, scipy, matplotlib, seaborn

#exercise 2
    # takes a natural number n and returns a dictionary with two keys "evens" and "odds".
    # "evens" prints the sum of all even natural numbers less than n
    # "odds" prints the sum of all odd natural numbers less than n
    def evens_and_odds(n: int) -> dict:
        # defining variables
        e_sum = 0
        o_sum = 0
    
        # loops n times and adds the odds and evens to respective groups
        for i in range(n):
            if i % 2 == 0:
                e_sum += i
            else: # i % 2 == 1
                o_sum += i
                
        # returns dictionary of sums of evens and odds respectively
        return {'evens': e_sum, 'odds': o_sum}

#exercise 3
    from typing import Union
    from datetime import datetime, date, time, timedelta
    
    # takes two strings in format 'YYYY-MM-DD' and a keyword 'float' or 'string'
    # returns time between two dates in days
    # if out keyword is not specificed, assumed to be 'float' output
    # implements datetime package
    def time_diff(date_1: str, date_2: str, out: str = "float") -> Union[str,float]:
        # puts inputted dates into format to find delta
        d1 = datetime.strptime(date_1, "%Y-%m-%d")
        d2 = datetime.strptime(date_2, "%Y-%m-%d")
        
        # computes difference between days
        n_days = abs(d2 - d1).days
    
        # determines output based on inputted, returning difference in correct format
        if out == "string":
            return "There are " + str(n_days) + " days between the two dates"
        else:
            return n_days

#exercise 4
    # takes list parameter and returns a list of the arguments in reverse order
    def reverse(in_list: list) -> list:
        # creates list and arranges the inputted list in reverse order
        new_list = [in_list[-(x+1)] for x in range(len(in_list))]
    
        # returns this reversed list
        return new_list

#exercise 5
    # takes two natural numbers n and k, and returns probability of getting
    # k heads from n flips, from 50/50 coin flips
    def prob_k_heads(n: int, k: int) -> float:
        # defining p-variable as prob to get heads on a flip
        p = 0.5
        # helper function that reduces redundancy that calculates factorials recursively
        def factorial(x):
            # base case to get out of recursive loop
            if x == 0:
                return 1
            else:
            # multiplies current value and gets next value from 
                return x * factorial(x-1)
    
        # calculates n chooses k using the factorial helper function
        n_choose_k = factorial(n) / (factorial(k) * factorial(n - k))
    
        # calculates probability based on binomial function
        prob = n_choose_k * (p) ** k * (1 - p) ** (n - k)
        return prob