# Forest Growth Functions
# Mika Erdmann, Intern at Aarhus University ENVS
# Supervisor Katarina Elofsson
# Started 07.03.2024

import numpy as np


# This script includes the different forest growth functions

# Thomas

# Read in parameters as an object

# TODO: For one country or all at the same time? (Then it would be matrices and not vectors)
class Params_Thomas:
    # I create an object that contains all of the parameters used in Thomas function. V_gross etc. contain all species.
    # In the first column, all variables have the names of the species.
    def __init__(self, V_gross, V_pot, V_lim, Species_Shares, country_name):
        self.V_gross = V_gross[1,]
        self.V_pot = V_pot[1,]
        self.V_lim = V_lim[1,]
        self.Species_Shares = Species_Shares[1,]
        self.Species_names = Species_Shares[0,]
        self.country = country_name

# TODO: Read in data as variables (maybe somewhere else?)

def Growth_Thomas_t(V_t, country):
    # create object with data for the country
    Thomas = Params_Thomas(V_gross=, V_pot=, V_lim=, Species_Shares=, country_name=)

    # The function calculates the growth in one country in one year
    G_t_i = np.zeros(len(Thomas.Species_Shares))
    # Now I loop over all of the species to calculate species-specific growth in one country and add it together afterward
    for i in range(0, len(Thomas.Species_names)):
        V_t_i = Thomas.Species_Shares[i] * V_t          # Here I use the shares of each species in the country
        G_t_i[i] = Thomas.V_gross[i] * (Thomas.V_pot[i] - V_t_i)/(Thomas.V_pot[i] - Thomas.V_lim[i])
    G_t = sum(G_t_i)
    return G_t


