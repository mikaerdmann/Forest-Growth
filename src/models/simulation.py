# Forest Growth Functions
# Mika Erdmann, Intern at Aarhus University ENVS
# Supervisor Katarina Elofsson
# Started 07.03.2024

# This script runs the simulation of the growth functions.
# It takes as inputs the functions and starting conditions.
# The output is a matrix of country-specific growth paths

import numpy as np
import scipy as sci
import pandas as pd

# import functions
import Growth_functions as fc

def Growth(V_t, approach, country, y= 0):
    if approach == "Thomas":
        return fc.Growth_Thomas_t(V_t, country)
    if approach == "Katarina2016":
        return fc.Growth_Katarina2016_t(V_t, country, y)
    if approach == "Katarina2018":
        return fc.Growth_Katarina2018(V_t,country)
def current_stock_i(V_t, country):
    V_t = V_t + Growth(V_t, approach, country )
    return V_t

def stock_over_time_i(country, T, V0, y_0 = 0):
    V_t = V0
    V_path = np.zeros(T)
    V_path[0] = V_t
    for t in range(0,T):
        V_t = current_stock_i(V_t, country)
        V_path[t] = V_t
    return V_path



# TODO:
# Read in starting stocks for each country and create country loop

def read_initial_values(approach):
    # This function reads in the initial Values needed for the models. Here, these initial values are not yet
    # consistent, this means the initial values for Volume may vary between the approaches
    if approach == "Katarina2018":
        data = pd.read_excel(path_data + "\\Data Katarina 2018.xlsx", sheet_name=1, decimal=',')
    if approach == "Katarina2016":
        data = pd.read_excel(path_data + "\\Data Katarina 2016.xlsx", sheet_name=1, decimal=',')
    if approach == "Thomas":
        data = pd.read_excel(path_data + "\\Data Thomas.xlsx", sheet_name=1, decimal=',')
    # return a df with two colums: Country and Volume
    V_0_i = data.loc[:, ["Country", "Volume"]]
    return V_0_i

def recreate_model(y_0 = 0, T = 100):
    # This function recreates the Growth Paths with the initial values from each approaches paper. Hence, the outcomes
    # Should be simulating the same results as reported in the papers
    V_0_i= read_initial_values(approach=approach)
    # Create an empty array which will be filled with each country's path. It has as columns the countrys and
    # as rows the time steps
    V_i = np.zeros(T, len(V_0_i))
    # Now for each country, using the initial Volume for this country, the stock over time (volume/growth path) is generated
    for i in range(0, len(V_0_i)):
        c = V_0_i["Country"][i]
        V0 = V_0_i["Volume"][i]
        # V will be a column in the Dataframe with the column name c
        V = stock_over_time_i(country= c,T=T, V0=V0)
        V_i[i] = V
    V_i = pd.DataFrame()
    return V_i

#
# Set the approach
path_data = "C:\\Users\\mikae\\Documents\\Aarhus Internship\\model\\data\\raw"
approaches = ["Katarina2016", "Katarina2018", "Thomas"]
approach = approaches[1]


V_path  = recreate_model()

