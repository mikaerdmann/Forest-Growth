# Forest Growth Functions
# Mika Erdmann, Intern at Aarhus University ENVS
# Supervisor Katarina Elofsson
# Started 07.03.2024

import numpy as np
import pandas as pd

path_data = "C:\\Users\\mikae\\Documents\\Aarhus Internship\\model\\data\\raw"
# This script includes the different forest growth functions

# Thomas

# Read in parameters as an object

class Params_Thomas:
    # I create an object that contains all of the parameters used in Thomas function. V_gross etc. contain all species.
    # In the first column, all variables have the names of the species.
    def __init__(self, V_gross, Species_Shares, country_name):
        self.V_gross = V_gross[1,]
       # self.V_pot = V_pot[1,]
       # self.V_lim = V_lim[1,]
        self.Species_Shares = Species_Shares[1,]
        self.Species_names = Species_Shares[0,]
        self.country = country_name

def read_params_one_country(country):
    # This function reads in all of the country-specific data (species shares and gross incremement)
    data = pd.read_excel(path_data+"\\Data Thomas.xlsx", sheet_name=1, decimal=',')
    data_c = data[data["Country"] == country]
    Species_area_c = data_c.loc[:,'Total':'Other']
    areas_shares = np.asarray(Species_area_c.loc[:,"Beech":"Other"])/np.asarray(Species_area_c.loc[:,'Total'])
    # I calulate the shares by calculating the share of each species of the Total area
    # TODO: How to deal with the "other"? Is it the rest to 100%?
    Species_Shares_c = pd.DataFrame({"Species": Species_area_c.loc[:,"Beech":"Other"].columns.tolist(), "shares": areas_shares.reshape(8)})
    # Now I calculate the species shares of the gross increment
    V_gross_c = float(data_c.loc[:, 'Gross'])
    V_gross_species_c = pd.DataFrame(
        {"Species": Species_area_c.loc[:, "Beech":"Other"].columns.tolist(), "shares": areas_shares.reshape(8) * V_gross_c})
    return Species_Shares_c, V_gross_c, V_gross_species_c


def Growth_Thomas_t(V_t, country):
    # This function has as input the national current stock and the name of the country. It reads the national parameters
    # gross increment and shares
    Species_Shares_c, V_gross_c = read_params_one_country(country)
    # create object with data for the country
    Thomas = Params_Thomas(V_gross=V_gross_c, Species_Shares=Species_Shares_c, country_name=country)

    # Read in the calculated parameters V:pot and V_lim (species specific
    data_pot_lim = pd.read_excel(path_data + "\\Data Thomas.xlsx", sheet_name=0, decimal=',')
    V_pot_c =np.asarray(data_pot_lim["Species", "A"])
    V_lim_c =np.asarray([V_pot_c["Species"], V_pot_c["A"] * 0.83])

    # The function calculates the growth in one country in one year
    # First, create an empty Array that will hold every species growth
    G_t_i = np.zeros(len(Thomas.Species_Shares))
    # Now I loop over all of the species to calculate species-specific growth in one country
    for i in range(0, len(Thomas.Species_names)):
        V_t_i = Thomas.Species_Shares[i] * V_t          # Here I use the shares of each species in the country to get the current species volume

        G_t_i[i] = Thomas.V_gross[i] * (V_pot_c[i] - V_t_i)/(V_pot_c[i] - V_lim_c[i])

    # Then, I add it together to calculate national growth
    G_t = sum(G_t_i)
    return G_t


# test
country = "Belgium"

sp, Vgc, VgSc= read_params_one_country(country)