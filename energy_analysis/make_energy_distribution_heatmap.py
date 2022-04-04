import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker

#/home/rictuar/coding_projects/fiehn_work/cfmid/cfmid_redo/results/[M-H]-/hcd/precursor_no/cfmid-collision_[M-H]-_hcd_precursor_no.txt

def make_collision_energy_column(input_panda,instrument):
    if (instrument=='qtof'):
        input_panda['experimental_collision_parsed']=input_panda['Collision_energy']
        return input_panda
    
    elif (instrument=='itft'):
        input_panda.insert(loc=len(input_panda.columns),column='experimental_collision_parsed',value=35)
        return input_panda

    elif (instrument=='hcd'):
        input_panda=input_panda.loc[input_panda['Collision_energy'].str.contains('eV'),input_panda.columns]        
        input_panda['experimental_collision_parsed']=input_panda['Collision_energy'].str.findall(r'[0-9]+').str[1].astype(float)
        return input_panda

def collapse_large_eV(input_panda,max_eV):
    #swap eV greater than some max_eV with the max
    #logic courtesy of https://stackoverflow.com/questions/33769860/pandas-apply-but-only-for-rows-where-a-condition-is-met
    input_panda_mask=(input_panda['experimental_collision_parsed'] > max_eV)
    input_panda_masked=input_panda[input_panda_mask]
    input_panda['experimental_collision_parsed_maxed']=input_panda['experimental_collision_parsed']
    input_panda.loc[input_panda_mask,'experimental_collision_parsed_maxed']=max_eV
    return input_panda

def make_heatmap(input_panda,y_direction_bin_count,output_address):
    my_histogram, x_edges, y_edges = np.histogram2d(
        input_panda['bins'], input_panda['experimental_collision_parsed_maxed'], bins=[20, y_direction_bin_count]
    )
    my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=1).reshape(-1,1))
    #my_histogram=np.divide(my_histogram,np.sum(my_histogram,axis=0))
    # my_histogram=np.divide(
    #     my_histogram,
    #     np.add.outer(
    #         np.sum(my_histogram,axis=1),
    #         np.sum(my_histogram,axis=0)
    #     )
    # )
    #######
    #transform to percents
    my_histogram=100*my_histogram
    plt.rcParams['font.size']=18
    #######

    print(my_histogram)
    print(x_edges)
    print(y_edges)
    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    # create figure from out histogram
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    plt.title("Experimental Collision Energy vs. Similarity Score")
    plt.ylabel("Experimental Collision Energy (eV)")
    plt.xlabel("Similarity Score")
    tick_spacing = 2
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    cax = divider.append_axes("right", size="5%", pad=0.05)
    image = ax.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma"
    )

    #######
    for i in range(1,len(x_edges)-1):
        ax.vlines(
            x=x_edges[i],
            ymin=y_edges[0],
            ymax=y_edges[-1],
            colors='w'
        )
    ax.set_xticks([ (x_edges[i]-(x_edges[1]/2)) for i in range(1,len(x_edges))])
    ax.set_xticklabels([ (str(1000-i*50+25)) for i in range(1,len(x_edges))],rotation=-90)  
    #######

    fig.colorbar(image, cax=cax, orientation="vertical",label='Percentage of Compounds')
    #plt.show()
    output_address=base_output_path+f'heatmap_{adduct}_{instrument}.png'
    plt.savefig(output_address)
    output_address=base_output_path+f'heatmap_{adduct}_{instrument}.eps'
    plt.savefig(output_address)
    


if __name__ == "__main__":
    # max_eV=45
    # y_direction_bin_count=44
    # adduct='[M+H]+'
    # instrument='qtof'
    max_eV=70
    y_direction_bin_count=30
    adduct='[M+H]+'
    instrument='hcd'
    starting_file_address=f"../../../results/{adduct}/{instrument}/precursor_no/cfmid-collision_{adduct}_{instrument}_precursor_no.txt"
    base_output_path='../../../results/energy_exploration/overall_heatmapped/'
    

    input_panda=pd.read_csv(starting_file_address,sep='¬')

    input_panda=make_collision_energy_column(input_panda,instrument)
    input_panda=collapse_large_eV(input_panda,max_eV)
    print(input_panda)
    make_heatmap(input_panda,y_direction_bin_count,base_output_path)
