import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
from matplotlib.colors import Normalize
import matplotlib.cm as cm


def make_heatmap_panda(temp_panda,feature_number):
    #extract feature
    feature_vector=np.array(temp_panda.fingerprint_array.to_list())[:,feature_number]
    heatmap_panda_dict={
        'feature':feature_vector,
        'dot_product':temp_panda['dot_product'].to_list()
    }
    heatmap_input_panda=pd.DataFrame.from_dict(heatmap_panda_dict)
    return heatmap_input_panda

def make_heatmap(input_panda,x_direction_bin_count,y_direction_bin_count,temp_important_feature,output_base,temp_axes,add_x_ticks):
    my_histogram, x_edges, y_edges = np.histogram2d(
        input_panda['dot_product'], input_panda['feature'], bins=[x_direction_bin_count, y_direction_bin_count]
    )
    print(my_histogram)
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=1).reshape(-1,1))

    #transform to percents
    my_histogram=100*my_histogram
    plt.rcParams['font.family']='Arial'
    #plt.rcParams['font.size']=18
    #######


    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    # create figure from out histogram
    #fig, ax = plt.subplots()
    ##divider = make_axes_locatable(temp_axes)
    #plt.title(str(temp_important_feature))
    #plt.ylabel("Experimental Collision Energy (eV)")
    #plt.xlabel("Dot Product")
    tick_spacing = 2
    temp_axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ##cax = divider.append_axes("right", size="5%", pad=0.05)
    image = temp_axes.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma"#, vmin=0, vmax=1
    )

    #######
    for i in range(1,len(x_edges)-1):
        temp_axes.vlines(
            x=x_edges[i],
            ymin=y_edges[0],
            ymax=y_edges[-1],
            colors='w'
        )
    if add_x_ticks==True:
        temp_axes.set_xticks([ (x_edges[i]-(x_edges[1]/2)) for i in range(2,len(x_edges),2)])
        temp_axes.set_xticklabels([ (str(1000-i*50+25)) for i in range(2,len(x_edges),2)],rotation=-90)  
    #######
    temp_axes.set_yticks([0.25,0.75])
    temp_axes.set_yticklabels(['0','1']) 
    temp_axes.set_title('Bit Number '+str(temp_important_feature))
    #temp_axes.colorbar(image, cax=cax, orientation="vertical",label='Percentage of Compounds')
    #plt.tight_layout()
    #plt.show()
    plt.savefig(output_base+str(feature_of_interest_number)+'.png')
    #return fig
    #return x_edges

if __name__=="__main__":

    #the original list
    # important_feature_list=    [  1, 374,   2, 345, 712, 257, 696, 697, 185, 688, 333, 186, 643,
    #         645, 439, 392, 656,  20, 665, 540, 181, 710, 346, 451, 709, 365,
    #         449,  11, 143, 516, 391, 287, 818, 452, 356, 600, 611, 672, 528,
    #          19, 335, 545, 430, 376, 340, 797, 440, 708, 241,  12]

    ## these were the lists that i sent to oliver the first time
    ## curated good features
    ## important_feature_list=[185,333,356,430,516,688,708,709,710]
    ## curated bad features
    ## important_feature_list=[143,287,340,376,449,545,600,665,672,697]
    ## irrelevant_feature list
    ## important_feature_list=[1, 2, 11, 12, 19, 20, 181, 186, 241, 257, 335, 345, 346, 365, 374, 391, 392, 439, 440, 451, 452, 528, 540, 611, 643, 645, 656, 696, 712, 797, 818]
    
    ## after reviewing, i came up with the following lists
    ## important_feature_list=[185,333,345,356,365,430,516,540,688,708,709,710]
    ## important_feature_list=[19, 143,340,374,376,449,545,600,665]
    ## split irrelevant features into three lists
    # important_feature_list=[1, 2, 11, 12, 20, 181, 186, 241, 257, 287]
    # important_feature_list=[335, 346, 391,392, 439,440, 451, 452, 528, 611]
    important_feature_list=[643, 645, 656,672, 696,697, 712, 797, 818]
    total_feature_count=len(important_feature_list)
    output_address=f'../../../results/compound_exploration/individual_features/features_predicatbility_neither_3.png'


    x_direction_bin_count=20
    y_direction_bin_count=2
    adduct='[M+H]+'
    instrument='hcd'
    cohort_cleaned_output_address=f'../../../results/compound_exploration/{adduct}_{instrument}_cohort_fingerprints.bin'
    #irrelevant
    output_base=f'../../../results/compound_exploration/individual_features/{adduct}_{instrument}_feature_'
    cohort_panda=pd.read_pickle(cohort_cleaned_output_address)

    #total_fig=plt.figure()
    #total_fig, total_ax = plt.subplots((total_feature_count),constrained_layout=True,figsize=(6.69292, 12))
    total_fig, total_ax = plt.subplots((total_feature_count),figsize=(6.69292, 12))
    for i,feature_of_interest_number in enumerate(important_feature_list):
        if i >=total_feature_count:
            continue
        heatmap_input_panda=make_heatmap_panda(cohort_panda,feature_of_interest_number)
        if i==total_feature_count-1:
            make_heatmap(heatmap_input_panda,x_direction_bin_count,y_direction_bin_count,feature_of_interest_number,output_base,total_ax[i],True)
        else:
            make_heatmap(heatmap_input_panda,x_direction_bin_count,y_direction_bin_count,feature_of_interest_number,output_base,total_ax[i],False)

        #total_ax[i].annotate(temp)
        #total_fig.axes.append(temp)
    
    # total_ax[total_feature_count-1].rcParams['font.family']='Arial'
    # total_ax[total_feature_count-1].rcParams['font.size']=24
    # #######   
    # total_ax[total_feature_count-1].set_xticks([ (x_edges[i]-(x_edges[1]/2)) for i in range(2,len(x_edges),2)])
    # total_ax[total_feature_count-1].set_xticklabels([ (str(1000-i*50+25)) for i in range(2,len(x_edges),2)],rotation=-90)  



    total_fig.suptitle('Bits Not Visibly Differentiating Predictability, Group 3')
    total_fig.supylabel('Individual Bits')   
    total_fig.supxlabel('Dot Product')
    #divider = make_axes_locatable(temp_axes)
    #plt.title(str(temp_important_feature))
    #plt.ylabel("Experimental Collision Energy (eV)")
    #plt.xlabel("Dot Product")
    #tick_spacing = 2
    #temp_axes.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #cax = divider.append_axes("right", size="5%", pad=0.05)

    #cax = divider.append_axes("right", size="5%", pad=0.05)
    
    plt.tight_layout()
    normalizer=Normalize(0,100)
    im=cm.ScalarMappable(norm=normalizer,cmap="magma")
    total_fig.colorbar(im,ax=total_ax.ravel().tolist())
    #plt.show()
    plt.savefig(output_address)