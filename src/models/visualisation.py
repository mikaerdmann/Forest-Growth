"""


"""
import matplotlib
import pandas as pd
import numpy as np
matplotlib.use('TkAgg') # This is needed because of some Pycharm + pyplot bug (figureCanvas attribute error).
import matplotlib.pyplot as plt

import simulation as sim
import Growth_functions as fc
path_data = "C:\\Users\\mikae\\Documents\\Aarhus Internship\\model\\data\\raw"
T_lim = 200


# visualize comparisons
V_path_compare_K2016, V_path_compare_K2018, V_path_compare_Thomas = sim.run_compare_all(T = T_lim)

fig, axes = plt.subplots(nrows=3, ncols=1)

axes[0].plot(V_path_compare_K2016, linewidth = 1)
axes[0].set_ylabel('Time step')  # Add a y-label to the axes.
axes[0].set_title('Katarina 2016')

axes[1].plot(V_path_compare_K2018, linewidth = 1)
axes[1].set_ylabel('Time step')  # Add a y-label to the axes.
axes[1].set_title('Katarina 2018')

axes[2].plot(V_path_compare_Thomas, linewidth = 1)
axes[2].set_xlabel('Volume')  # Add an x-label to the axes.
axes[2].set_ylabel('Time step')  # Add a y-label to the axes.
axes[2].set_title('Thomas')

plt.show()


# Visualize Last Values (Maximum Capacities)

K2018_max = V_path_compare_K2018.loc[T_lim-1]
Thomas_max = V_path_compare_Thomas.loc[T_lim-1]
# TODO: Add Katarina 2016 when issue is solved
Maxs = pd.DataFrame({"Katarina2018": K2018_max,
                     "Thomas": Thomas_max})
#Maxs = Maxs.transpose()
fig, ax = plt.subplots(layout = "constrained")
approaches = ["Katarina2018", "Thomas"]
countries = Maxs.index.values
width = 0.08
multiplier = 0
x = np.arange(len(countries))  # the label locations

for country, measurement in Maxs.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=country)
    ax.bar_label(rects, padding=1, fontsize = 7)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Max Potential')
ax.set_xlabel("Country", fontsize = 10)
ax.set_title('Maximum Potential by Approach')
ax.set_xticks(x + width, countries, fontsize = 7)
ax.legend(loc='upper left', ncols=2)

plt.show()
