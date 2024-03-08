# Forest Growth Functions
# Mika Erdmann, Intern at Aarhus University ENVS
# Supervisor Katarina Elofsson
# Started 07.03.2024


# This script includes the different forest growth functions

# Thomas

# Read in parameters as an object
class Params_Thomas:
    # I create an object that contains all of the parameters used in Thomas function. V_gross etc. contain all species.
    # In the first column, all variables have the names of the species.
    def __init__(self, V_gross, V_pot, V_lim, Species_Shares ):
        self.V_gross = V_gross[1]
        self.V_pot = V_pot[1]
        self.V_lim = V_lim[1]
        self.Species_Shares = Species_Shares[1]
        self.Species_names = Species_Shares[0]

# TODO: Read in data as variables (maybe somewhere else?)
# create object with data
Thomas = Params_Thomas(V_gross=, V_pot=, V_lim=, Species_Shares=)


def Growth_Thomas_t_s(V_t_s, params):
    G_t_s = V_gross_s * (V_pot_s - V_t)/(V_pot_s - V_lim_s)


