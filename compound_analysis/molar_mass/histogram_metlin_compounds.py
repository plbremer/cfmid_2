import pandas as pd
import matplotlib.pyplot as plt


if __name__=="__main__":
    molar_mass_input_address='../../../../results/compound_exploration/molar_mass/metlin_positive_masses.bin'
    molar_mass_panda=pd.read_pickle(molar_mass_input_address)

    molar_mass_panda['exact_mass'].astype(float).hist(bins=50)
    plt.show()