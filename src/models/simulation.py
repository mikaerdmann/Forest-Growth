# Forest Growth Functions
# Mika Erdmann, Intern at Aarhus University ENVS
# Supervisor Katarina Elofsson
# Started 07.03.2024

# This script runs the simulation of the growth functions.
# It takes as inputs the functions and starting conditions.
# The output is a matrix of country-specific growth paths

import numpy as np
import scipy as sci

# import functions
import functions.py as fc

def Growth(V_t, function):


def current_stock_i(V_t):
    V_t = V_t + Growth(V_t)
    return V_t

def stock_over_time_i(T, V0, y_0):
    V_t = V0
    V_path = np.zeros(T)
    V_path[0] = V_t
    for t in range(0,T):
        V_t = current_stock_i(V_t)
        V_path[t] = V_t
    return V_path





