"""
Forest Growth Simulation

This script simulates the growth of forests using different growth functions and approaches.
It was developed by Mika Erdmann during an internship at Aarhus University ENVS under the supervision of Katarina Elofsson.
The simulation aims to generate country-specific growth paths based on various starting conditions and growth models.

Author: Mika Erdmann
Supervisor: Katarina Elofsson
Started: 07.03.2024

Functions:
- Growth: Calculate growth using specified approach for one timestep.
- current_stock_i: Calculate current stock for one timestep.
- stock_over_time_i: Calculate stock over time for a given country and timeframe.
- read_initial_values: Read initial values for the models.
- recreate_model: Recreate growth paths with initial values from each approach's paper.

"""

import numpy as np
import scipy as sci
import pandas as pd

# import functions
import Growth_functions as fc

def Growth(V_t, approach, country, y= 0):
    """
        Calculate growth using specified approach for one timestep.

        Parameters:
            V_t (float): Current stock.
            approach (str): Growth approach (Thomas, Katarina2016, Katarina2018).
            country (str): Name of the country.
            y (float): Additional parameter (used only for Katarina2016 approach).

        Returns:
            function: Growth function for the timestep.
        """
    if approach == "Thomas":
        return fc.Growth_Thomas_t(V_t, country)
    if approach == "Katarina2016":
        return fc.Growth_Katarina2016_t(V_t, country, y)
    if approach == "Katarina2018":
        return fc.Growth_Katarina2018(V_t,country)


def current_stock_i(V_t, country):
    """
        Calculate current stock for one timestep.

        Parameters:
            V_t (float): Current stock.
            country (str): Name of the country.

        Returns:
            float: Current stock for the timestep.
        """
    V_t = V_t + Growth(V_t, approach, country )
    return V_t


def stock_over_time_i(country, T, V0, y_0 = 0):
    """
        Calculate stock over time for a given country and timeframe.

        Parameters:
            country (str): Name of the country.
            T (int): Timeframe.
            V0 (float): Initial stock.
            y_0 (float): Additional parameter (used only for Katarina2016 approach).

        Returns:
            numpy.ndarray: Array containing stock over time.
        """
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
    """
        Read initial values for the models.

        Parameters:
            approach (str): Growth approach (Thomas, Katarina2016, Katarina2018).

        Returns:
            pandas.DataFrame: DataFrame with country and initial volume.
        """
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
    """
        Recreate growth paths with initial values from each approach's paper.

        Parameters:
            y_0 (float): Additional parameter (used only for Katarina2016 approach).
            T (int): Timeframe.

        Returns:
            pandas.DataFrame: DataFrame containing growth paths for each country.
        """
    # Hence, the outcomes should be simulating the same results as reported in the papers
    V_0_i= read_initial_values(approach=approach)
    # Create an empty array which will be filled with each country's path. It has as columns the countrys and
    # as rows the time steps
    V_i = []
    # Now for each country, using the initial Volume for this country, the stock over time (volume/growth path) is generated
    for i in range(0, len(V_0_i)):
        c = V_0_i["Country"][i]
        V0 = V_0_i["Volume"][i]
        # V will be a column in the Dataframe with the column name c
        V = stock_over_time_i(country= c,T=T, V0=V0)
        V_i.append(V.tolist())
    V_i_df = pd.DataFrame(V_i)
    V_i_df[0] = V_0_i["Country"]
    V_i_df = V_i_df.transpose()
    return V_i_df


# Set the approach
path_data = "C:\\Users\\mikae\\Documents\\Aarhus Internship\\model\\data\\raw"
approaches = ["Katarina2016", "Katarina2018", "Thomas"]
approach = approaches[1]


V_path  = recreate_model()

