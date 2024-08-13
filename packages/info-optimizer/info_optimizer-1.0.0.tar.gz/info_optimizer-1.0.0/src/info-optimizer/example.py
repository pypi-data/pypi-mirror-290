@author: Iman Ahmadianfar
"""
# test_script.py  

# Import the INFO function from the optimizer module  
from info_optimizer import INFO

import numpy as np

# Define the objective function (for minimization)  
def objective_function(x):  
    return np.sum(x**2)  # This returns the sum of squares as a scalar


# Set parameters for the INFO optimizer  
lb = -100    # Lower bound  
ub = 100     # Upper bound  
dim = 30    # Number of dimensions  
nP = 30     # Number of particles  
MaxIt = 500 # Maximum number of iterations  

# Run the INFO optimizer  
result = INFO(lb=lb, ub=ub, dim=dim, nP=nP, MaxIt=MaxIt, fobj=objective_function)