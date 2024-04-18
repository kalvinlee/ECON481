# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 2

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset2.py"

# Exercise 1
import numpy as np
# returns 1000 simulated observations via data generating process
# yi = 5 + 3xi1 + 2xi2 + 6xi3 + εi where
# xi1, xi2, xi3 ~ N(0,2) and εi ~ N(0,1)
# takes int argument seed which sets a seed, returning a tuple of two
# elements, (y,X) where y is a 1000 x 1 array and X is a 1000 x 3 array
def simulate_data(seed: int = 481) -> tuple:
    np.random.seed(seed)
    # generates x values
    x_1 = np.random.normal(0, np.sqrt(2), 1000)
    x_2 = np.random.normal(0, np.sqrt(2), 1000)
    x_3 = np.random.normal(0, np.sqrt(2), 1000)
    # generates error values
    e = np.random.normal(0, 1, 1000)
    # generates X array
    X = np.column_stack((x_1, x_2, x_3))
    # generates y values
    y = 5 + 3*x_1 + 2*x_2 + 6*x_3 + e
    return y,X

# Exercise 2
import numpy as np
import scipy as sp
# estimates MLE parameters beta_hat MLE for simulated data where assumed
# model is y = beta_0 + beta_1 * xi1 + beta_2 * xi2 + beta_3 * xi3 + εi
# where εi ~ N(0,1)
# function should take arguments of a 1000 x 1 array and 1000 x 3 array
# and return a 4 x 1 array with coefficients beta_0, 1, 2, 3 in order
def estimate_mle(y: np.array, X: np.array) -> np.array:
    # helper function that solves for negative log likelihood
    def negll(beta: np.array, y: np.array, X: np.array):
        beta0, beta1, beta2, beta3 = beta # initializes each beta
        n = len(y) # number of observations
        sigsq = 1 # varaiance of error = 1
        # solves for yhat regression
        yhat = beta0 + beta1 * X[:, 0] + beta2 * X[:, 1] + beta3 * X[:, 2]
        # finds log likelihood
        log_l = -(n/2) * np.log(2 * np.pi * sigsq) - (1/(2 * sigsq)) * np.sum((y - yhat)**2)
        return -log_l
    initial_b = np.zeros(4) # initializes guess for parameters
    #minimize log likelihood to find MLE parameters
    result_b = sp.optimize.minimize(negll, initial_b, args=(y,X), method = 'Nelder-Mead')
    return result_b.x

# Exercise 3
import numpy as np
import scipy as sp
# estimates OLS coefficients for simulated data that does not use the closed form solution
# takes arguments X as a 1000x3 array and y as a 1000x1 array returning a 4x1 array with
# coefficients beta_0, 1, 2, 3 in order
def estimate_ols(y: np.array, X: np.array) -> np.array:
    # helper function that solves for error sum of squares
    def sse(beta: np.array, X: np.array, y: np.array):
        return np.sum((y - (X @ beta)) ** 2)
    # adds column to beginning matrix X as intercept term
    X = np.concatenate((np.ones((X.shape[0], 1)), X), axis = 1)
    # initializes guess for parameters
    b_initial = np.zeros(4)
    # finds OLS parameters
    b_result = sp.optimize.minimize(sse, b_initial, args = (X, y), method = 'Nelder-Mead')
    return b_result.x