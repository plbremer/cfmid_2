import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker



def make_heatmap_panda(temp_panda,feature_number):
    #extract feature
    feature_vector=np.array(temp_panda.fingerprint_array.to_list())[:,feature_number]
    heatmap_panda_dict={
        'feature':feature_vector,
        'dot_product':temp_panda['dot_product'].to_list()
    }
    heatmap_input_panda=pd.DataFrame.from_dict(heatmap_panda_dict)
    return heatmap_input_panda

def make_heatmap(input_panda,x_direction_bin_count,y_direction_bin_count,temp_important_feature):
    my_histogram, x_edges, y_edges = np.histogram2d(
        input_panda['dot_product'], input_panda['feature'], bins=[x_direction_bin_count, y_direction_bin_count]
    )
    print(my_histogram)
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=1).reshape(-1,1))

    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    # create figure from out histogram
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    plt.title(str(temp_important_feature))
    plt.ylabel("...")
    plt.xlabel("dot product")
    tick_spacing = 2
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    cax = divider.append_axes("right", size="5%", pad=0.05)
    image = ax.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma", vmin=0, vmax=1
    )
    fig.colorbar(image, cax=cax, orientation="vertical")
    plt.show()

if __name__=="__main__":
    # important_feature_list=[  
    #         1,  20, 374, 696, 712,   2, 186, 643,  19, 600, 528, 697, 392,
    #         15, 257, 699, 364, 185, 437, 628, 391,  12, 143,   3, 335, 346,
    #         345, 607, 688, 656, 593, 449, 192, 540, 645, 248, 672, 451, 535,
    #         452, 440, 338, 516,  24, 665, 376, 341, 638, 685,  16
    #     ]

    important_feature_list=    [  1, 374,   2, 345, 712, 257, 696, 697, 185, 688, 333, 186, 643,
            645, 439, 392, 656,  20, 665, 540, 181, 710, 346, 451, 709, 365,
            449,  11, 143, 516, 391, 287, 818, 452, 356, 600, 611, 672, 528,
             19, 335, 545, 430, 376, 340, 797, 440, 708, 241,  12]
    #important_feature_list=[i for i in range(0,600,20)]
        
    #important_feature_list=[1, 2, 15, 19, 20, 186, 374, 392, 528, 600, 643, 696, 697, 712]
    #important_feature_list=[1, 20, 376, 392, 437, 449, 451, 600, 607, 628, 665, 712]
    #feature_of_interest_number=1
    x_direction_bin_count=20
    y_direction_bin_count=2
    adduct='[M+H]+'
    instrument='hcd'
    cohort_cleaned_output_address=f'../../../results/compound_exploration/{adduct}_{instrument}_cohort_fingerprints.bin'
    cohort_panda=pd.read_pickle(cohort_cleaned_output_address)


    for feature_of_interest_number in important_feature_list:
        heatmap_input_panda=make_heatmap_panda(cohort_panda,feature_of_interest_number)
        make_heatmap(heatmap_input_panda,x_direction_bin_count,y_direction_bin_count,feature_of_interest_number)