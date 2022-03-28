import numpy as np
import pandas as pd
import scipy.spatial.distance
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker

def flatten_inchikeys(temp_panda):
    temp_panda['inchikey_flattened']=temp_panda['inchikey'].str.split(pat='-').str.get(0)+'-UHFFFAOYSA-N'
    return temp_panda

def remove_redundant_inchikeys(temp_panda):
    '''
    strategy
    make the inchikey the index
    the 
    '''
    temp_panda.set_index(keys='inchikey_flattened',inplace=True)
    temp_panda.drop_duplicates(keep='first',inplace=True)
    #temp_panda.reset_index(inplace=True)
    return temp_panda

def join_cohort_and_nist(temp_panda,nist_panda):
    combined_panda=nist_panda.join(other=temp_panda,on='InChIKey',how='inner')
    return combined_panda

def remove_failed_fingerprints(temp_panda):
    return temp_panda.loc[~pd.isna(temp_panda['cactvs_fingerprint'])]


def string_to_numpy(temp_string):
    return(np.array([int(element) for element in temp_string]))

def calculate_similarity_matrix(x_axis_array,y_axis_array,metric):
    return scipy.spatial.distance.cdist(
        x_axis_array,
        y_axis_array,
        metric=metric
    )

def calculate_input_for_heatmap(similarity_panda,combined_panda,combination_style):
    result_dict={
        'inchikey_from_similarity':similarity_panda.columns.to_list(),
        'inchikey_from_combined':combined_panda['InChIKey'].to_list(),
        'dot_product':combined_panda['dot_product'].to_list(),
        'metlin_similarity':None
    }
    if combination_style=='max':
        result_dict['metlin_similarity']=similarity_panda.max(axis='index')#similarity_panda.apply(max,axis='index').to_list()
    elif combination_style=='avg':
        result_dict['metlin_similarity']=similarity_panda.mean(axis='index')#similarity_panda.apply(np.mean(),axis='index').to_list()

    result_panda=pd.DataFrame(result_dict)
    return result_panda
    

def create_heatmap(input_panda,x_direction_bin_count,y_direction_bin_count,output_address):
    my_histogram, x_edges, y_edges = np.histogram2d(
        input_panda['dot_product'], input_panda['metlin_similarity'], bins=[x_direction_bin_count, y_direction_bin_count]
    )
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=1).reshape(-1,1))
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    # my_histogram=np.divide(
    #     my_histogram,
    #     np.add.outer(
    #         np.sum(my_histogram,axis=1),
    #         np.sum(my_histogram,axis=0)
    #     )
    # )

    print(my_histogram)
    print(x_edges)
    print(y_edges)
    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    print('extent!!!!')
    print(extent)
    # create figure from out histogram
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    plt.title("Experimental Collision Energy vs. Jaccard Similarity to Training Set")
    plt.ylabel("Jaccard Similarity")
    plt.xlabel("dot product")
    tick_spacing = 2
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    for i in range(len(my_histogram)):
        print(f'i is {i}')
        for j in range(len(my_histogram[0])):
            print(f'j is {j}')
            location_x=(((extent[1]-extent[0])/len(my_histogram))*i)+extent[0]+0.5*((extent[1]-extent[0])/len(my_histogram))
            location_y=(((extent[3]-extent[2])/len(my_histogram[0]))*j)+extent[2]+0.5*((extent[3]-extent[2])/len(my_histogram[2]))
            text=ax.text(
                location_x,location_y,str(my_histogram[i,j])[0:4],
                #location_x,location_y,'hi',
                #0,location_x,my_histogram[i,j],
                #location_x,location_y,
                ha="center",va="center",color='w'
            )

    cax = divider.append_axes("right", size="5%", pad=0.05)
    image = ax.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma"
    )
    fig.colorbar(image, cax=cax, orientation="vertical")

    
    plt.show()
    #plt.savefig(output_address)

if __name__=="__main__":
    x_direction_bin_count=20
    y_direction_bin_count=10
    adduct='[M+H]+'
    instrument='hcd'

    metlin_cleaned_output_address=f'../../../results/compound_exploration/{adduct}_metlin_fingerprints.bin'
    cohort_cleaned_output_address=f'../../../results/compound_exploration/{adduct}_{instrument}_cohort_fingerprints.bin'
    figure_max_output_address=f'../../../results/compound_exploration/{adduct}_{instrument}_max_similarity.png'

    experimental_inchikeys_to_include_address=f'../../../results/compound_exploration/{adduct}_{instrument}_relevant_inchikeys.bin'
    nist_fingerprint_address='../../../resources/starting_files/nist/fingerprints/fingerprints_nist20_inchikey.txt'
    metlin_fingerprint_address=f'../../../resources/starting_files/metlin/fingerprints/fingerprints_metlin_inchikey_{adduct}.txt'
    input_panda=pd.read_pickle(experimental_inchikeys_to_include_address)
    input_panda=flatten_inchikeys(input_panda)
    input_panda=remove_redundant_inchikeys(input_panda)
    print(input_panda)
    nist_fingerprint_panda=pd.read_csv(nist_fingerprint_address,sep='¬',index_col=0)
    #nist_fingerprint_panda.join(other=input_panda,on='inchikey_flattened')
    combined_panda=join_cohort_and_nist(input_panda,nist_fingerprint_panda)
    metlin_fingerprint_panda=pd.read_csv(metlin_fingerprint_address,sep='¬',index_col=0)
    combined_panda=remove_failed_fingerprints(combined_panda)
    metlin_fingerprint_panda=remove_failed_fingerprints(metlin_fingerprint_panda)

    combined_panda['fingerprint_array']=combined_panda['cactvs_fingerprint'].apply(string_to_numpy)
    metlin_fingerprint_panda['fingerprint_array']=metlin_fingerprint_panda['cactvs_fingerprint'].apply(string_to_numpy)

    # combined_panda=combined_panda.loc[0:502,:]
    # metlin_fingerprint_panda=metlin_fingerprint_panda.loc[0:502,:]

    similarity_panda=pd.DataFrame(
        #note the 1 minus to turn jaccard distnace to jaccard similarity
        data=1-calculate_similarity_matrix(
            np.array(metlin_fingerprint_panda['fingerprint_array'].to_list()),
            np.array(combined_panda['fingerprint_array'].to_list()),
            'jaccard'
        ),
        columns=combined_panda['InChIKey'].to_list(),
        index=metlin_fingerprint_panda['InChIKey']
    )
    
    print(similarity_panda)
    print(similarity_panda.apply(min,axis='index'))

    result_panda=calculate_input_for_heatmap(
        similarity_panda,
        combined_panda,
        'max'
    )
    create_heatmap(result_panda,x_direction_bin_count,y_direction_bin_count,figure_max_output_address)
    metlin_fingerprint_panda.to_pickle(metlin_cleaned_output_address)
    combined_panda.to_pickle(cohort_cleaned_output_address)
    
    # result_panda=calculate_input_for_heatmap(
    #     similarity_panda,
    #     combined_panda,
    #     'avg'
    # )
    # create_heatmap(result_panda,x_direction_bin_count,y_direction_bin_count,figure_max_output_address)