import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker


def make_heatmap_panda(temp_panda):
    heatmap_panda_dict={
        'exact_mass':temp_panda['exact_mass'].astype(float).to_list(),
        'dot_product':temp_panda['dot_product'].astype(float).to_list()
    }
    heatmap_input_panda=pd.DataFrame.from_dict(heatmap_panda_dict)
    return heatmap_input_panda


def make_heatmap(input_panda):
    my_histogram, x_edges, y_edges = np.histogram2d(
        input_panda['dot_product'].astype(float), input_panda['exact_mass'].astype(float), bins=[x_direction_bin_count, y_direction_bin_count]
    )   
    my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=1).reshape(-1,1))

    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    # create figure from out histogram
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    plt.title(str('my title'))
    plt.ylabel("...")
    plt.xlabel("dot product")
    tick_spacing = 2
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    cax = divider.append_axes("right", size="5%", pad=0.05)
    image = ax.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma"#, vmin=0, vmax=1
    )
    fig.colorbar(image, cax=cax, orientation="vertical")
    plt.show()


if __name__=="__main__":
    
    x_direction_bin_count=20
    y_direction_bin_count=50

    adduct='[M+H]+'
    instrument='hcd'
    cohort_cleaned_input_address=f'../../../../results/compound_exploration/{adduct}_{instrument}_cohort_fingerprints.bin'
    molar_mass_input_address='../../../../results/compound_exploration/molar_mass/nist20_positive_masses.bin'
    


    cohort_panda=pd.read_pickle(cohort_cleaned_input_address)
    molar_mass_panda=pd.read_pickle(molar_mass_input_address)
    
    print(molar_mass_panda)
    print(cohort_panda)

    cohort_panda=cohort_panda.set_index('inchikey')
    print(cohort_panda)
    #join pandas
    #make heatmap panda
    #make heatmap

    combined_panda=molar_mass_panda.join(
        other=cohort_panda,
        on='inchikey',
        how='inner'
    )

    print(combined_panda)

    heatmap_panda=make_heatmap_panda(combined_panda)

    # heatmap_panda.dot_product.hist()
    # plt.show()
    # heatmap_panda.exact_mass.hist()
    # plt.show()
    print(heatmap_panda)
    make_heatmap(heatmap_panda)