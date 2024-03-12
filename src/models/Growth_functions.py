"""
Forest Growth Functions

This script contains different forest growth functions implemented by Mika Erdmann during an internship at Aarhus University ENVS under the supervision of Katarina Elofsson. The script models forest growth using various approaches and parameters for different countries.

Author: Mika Erdmann
Supervisor: Katarina Elofsson
Started: 07.03.2024

Functions:
- read_params_one_country_Thomas: Read country-specific data for Thomas model.
- Growth_Thomas_t: Calculate growth using the Thomas model for one timestep.
- Growth_Katarina2016_t: Calculate growth using the Katarina 2016 model for one timestep.
- average_age_t: Calculate the average age for the Katarina 2016 model.
- optimise_age_t: Optimize age for the Katarina 2016 model.
- Growth_Katarina2018: Calculate growth using the Katarina 2018 model for one timestep.

"""
import numpy as np
import pandas as pd
import scipy.special

path_data = "C:\\Users\\mikae\\Documents\\Aarhus Internship\\model\\data\\raw"
# This script includes the different forest growth functions

# Thomas

# Read in parameters
def read_params_one_country_Thomas(country):
    """
       Read country-specific data for the Thomas model.

       Parameters:
           country (str): Name of the country.

       Returns:
           tuple: Tuple containing species shares, gross increment, and species-specific gross increment.
       """
    # This function reads in all of the country-specific data (species shares and gross incremement)
    data = pd.read_excel(path_data+"\\Data Thomas.xlsx", sheet_name=1, decimal=',')
    data_c = data[data["Country"] == country]
    Species_area_c = data_c.loc[:,'Total':'Other']
    areas_shares = np.asarray(Species_area_c.loc[:,"Beech":"Other"])/np.asarray(Species_area_c.loc[:,'Total'])
    # I calulate the shares by calculating the share of each species of the Total area
    # TODO: How to deal with the "other"? Is it the rest to 100%?
    Species_Shares_c = pd.DataFrame({"Species": Species_area_c.loc[:,"Beech":"Other"].columns.tolist(), "Shares": areas_shares.reshape(8)})
    # Now I calculate the species shares of the gross increment
    V_gross_c = float(data_c.loc[:, 'Gross'])  # TODO find a way to do this wihtout the future warning
    V_gross_species_c = pd.DataFrame(
        {"Species": Species_area_c.loc[:, "Beech":"Other"].columns.tolist(), "Gross": areas_shares.reshape(8) * V_gross_c})
    return Species_Shares_c, V_gross_c, V_gross_species_c

# Growth in one timestep
def Growth_Thomas_t(V_t, country):
    """
        Calculate growth using the Thomas model for one timestep.

        Parameters:
            V_t (float): National current stock.
            country (str): Name of the country.

        Returns:
            tuple: Tuple containing national aggregate growth and species-specific growth as a ndarray.
        """
    # This function has as input the national current stock and the name of the country. It reads the national parameters
    # gross increment and shares
    Species_Shares_c, V_gross_c, V_gross_species_c = read_params_one_country_Thomas(country)
    # Read in the calculated parameters V:pot and V_lim (species specific)
    # TODO: Make sure the species are sorted consistently!
    # TODO: Solve Issue with missing "Other" species in area shares and with missing species between estimated Params (V-pot) and species shares!
    data_pot_lim = pd.read_excel(path_data + "\\Data Thomas.xlsx", sheet_name=0, decimal=',')
    V_pot_c =data_pot_lim[["Species", "A"]]
    V_lim_c =V_pot_c.copy()
    V_lim_c["Lim"] = V_lim_c["A"] * 0.83
    V_pot_c_array = np.asarray(V_pot_c["A"])
    V_lim_c_array = np.asarray(V_lim_c["Lim"])
    # The function calculates the growth in one country in one year
    # First, create an empty Array that will hold every species growth
    G_t_i = np.zeros(len(Species_Shares_c))
    # Now I loop over all of the species to calculate species-specific growth in one country
    for i in range(0, len(Species_Shares_c)-1): # TODO: delete -1 when all species available
        V_t_i = Species_Shares_c["Shares"][i] * V_t          # Here I use the shares of each species in the country to get the current species volume

        G_t_i[i] = V_gross_species_c["Gross"][i] * (V_pot_c_array[i] - V_t_i)/(V_pot_c_array[i] - V_lim_c_array[i])

    # Then, I add it together to calculate national growth
    G_t = sum(G_t_i)
    return G_t, G_t_i


# Katarina 2016

def Growth_Katarina2016_t(V_t, country):
    """
        Calculate growth using the Katarina 2016 model for one timestep.

        Parameters:
            V_t (float): National current stock.
            country (str): Name of the country.

        Returns:
            float: National growth.
        """
    data = pd.read_excel(path_data + "\\Data Katarina 2016.xlsx", sheet_name=0, decimal=',')
    # extract parameters from data for the right country
    params_c = data[data["Country"] == country]
    m = params_c.m
    n = params_c.n
    k = params_c.k

    y_t = average_age_t(V_t, country, m, n, k)
    G_t = m*(V_t/y_t) - n*V_t

    return G_t
def average_age_t(V_t, m, n, k):
    """
        Calculate the average age for the Katarina 2016 model.

        Parameters:
            V_t (float): National current stock.
            m (float): Parameter m.
            n (float): Parameter n.
            k (float): Parameter k.

        Returns:
            float: Average age.
        """
    y_t= -(m * scipy.special.lambertw(-(n*(V_t/k)**(-1/m))/m))/n
    return y_t

def optimise_age_t(V_t, m,n,k):
    """
       Optimize age for the Katarina 2016 model.

       Parameters:
           V_t (float): National current stock.
           m (float): Parameter m.
           n (float): Parameter n.
           k (float): Parameter k.

       Returns:
           None
       """
    # this function must be put in optimiser, let y vary and restricted to positive numbers
    def func(Z_t, m, n, k):
        return k**(y)**m * np.exp(-n*y) - Z_t
    y = scipy.optimize.minimize(func, x0 = 100, bounds=(0))





# Katarina 2018

def Growth_Katarina2018(V_t, country):
    """
       Calculate growth using the Katarina 2018 model for one timestep.

       Parameters:
           V_t (float): National current stock.
           country (str): Name of the country.

       Returns:
           float: National growth.
       """
    SC_list = ["Sweden", "Finland"]
    ME_list = ["Portugal", "Spain", "France", "Italy", "Greece", "Slovenia"]
    if country in SC_list:
        SC = 1
        ME = 0
    if country in ME_list:
        ME = 1
        SC = 0
    else:
        ME = 0
        SC = 0

    G_t = 0.05881* V_t - 0.00011044* V_t**2 - 1.32664 * SC - 0.96349*ME
    return G_t


# test read_params_one_country()
country = "Belgium"
sp, Vgc, VgSc= read_params_one_country_Thomas(country)

# Test Growth_Thomas_t()
G, G_i = Growth_Thomas_t(2100, country)

