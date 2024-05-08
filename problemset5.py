# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 5

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset5.py"

# Exercise 1
import requests
from bs4 import BeautifulSoup
    # takes argument of a url on the course website and returns a string
    # containing all of the python code in the lecture formatted in a way
    # to save it as a python file and run without syntax issues
def scrape_code(url: str) -> str:
    req_obj = requests.get(url)
    bs = BeautifulSoup(req_obj.text)
    blocks = bs.find_all('code', class_ = 'sourceCode python')
    list = []
    for code in blocks:
        line = code.text.strip().split('\n')
        list += line
    string = '\n'.join(list)
    return string