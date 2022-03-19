
import numpy
import pandas
import matplotlib.pyplot
import regex as re

def transform_collision_energy_column(temp_panda,temp_instrument,temp_instrument_brand,temp_lumos_use_eV):
    if (temp_instrument=='qtof'):
        return temp_panda, 'Collision_energy'
    
    elif (temp_instrument=='itft'):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_itft',value=35)
        return temp_panda, 'Collision_energy_itft'

    elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Orbitrap Fusion Lumos') and (temp_lumos_use_eV==True)):
        #hold=input('hi')
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_hcd_lumos_eV_only',value=-1)

        for index,row in temp_panda.iterrows():
            #if the collision energy column contains eV, skip it
            #if 'eV' not in row['Collision_energy']:
            #    continue
            if ('Orbitrap Fusion Lumos' not in row['Instrument']) or ('eV' not in row['Collision_energy']):
                continue
            else:
                temp_panda.at[index,'Collision_energy_hcd_lumos_eV_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])
                #temp_panda.at[index,'Collision_energy_hcd_lumos_eV_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[1])
                #print((re.findall(r'[0-9]+',row['Collision_energy']))[1])

        temp_panda=temp_panda.loc[temp_panda['Collision_energy_hcd_lumos_eV_only'] != -1]

        temp_panda['Collision_energy_hcd_lumos_eV_only']=temp_panda['Collision_energy_hcd_lumos_eV_only'].multiply(temp_panda['PrecursorMZ'])

        return temp_panda, 'Collision_energy_hcd_lumos_eV_only'

    elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Orbitrap Fusion Lumos') and (temp_lumos_use_eV==False)):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_hcd_lumos_NCE_only',value=-1)

        for index,row in temp_panda.iterrows():
            #if the collision energy column contains eV, skip it
            if ('Orbitrap Fusion Lumos' not in row['Instrument']) or ('eV'  in row['Collision_energy']):
                continue
            else:
                temp_panda.at[index,'Collision_energy_hcd_lumos_NCE_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])

        
        temp_panda=temp_panda.loc[temp_panda['Collision_energy_hcd_lumos_NCE_only'] != -1]

        #############################if lumos and hcd##################################
        #divide column by precursor mz to figure out normalization
        ##############################################################################        
        temp_panda['Collision_energy_hcd_lumos_NCE_only']=temp_panda['Collision_energy_hcd_lumos_NCE_only'].multiply(temp_panda['PrecursorMZ'])
    
        return temp_panda, 'Collision_energy_hcd_lumos_NCE_only'

    elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Thermo Finnigan Elite Orbitrap')):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_hcd_Thermo_eV_only',value=-1)

        for index,row in temp_panda.iterrows():
            #temp_panda.at[index,'Collision_energy_hcd_Thermo_eV_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])

            if ('Thermo Finnigan Elite Orbitrap' not in row['Instrument']):
                continue
            else:
            
                #print(temp_panda.at[index,'Collision_energy'])
                temp_panda.at[index,'Collision_energy_hcd_Thermo_eV_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])
                #temp_panda.at[index,'Collision_energy_hcd_Thermo_eV_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[1])

        temp_panda=temp_panda.loc[temp_panda['Collision_energy_hcd_Thermo_eV_only'] != -1]
        temp_panda['Collision_energy_hcd_Thermo_eV_only']=temp_panda['Collision_energy_hcd_Thermo_eV_only'].multiply(temp_panda['PrecursorMZ'])

        
        return temp_panda, 'Collision_energy_hcd_Thermo_eV_only'

def bin_column(temp_panda, temp_column_name, temp_bin_count):
    column_bin_integers=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count,labels=False)
    column_bin_edges=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count)
    
    #print(column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bins',value=column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bin_edges',value=column_bin_edges)
    return temp_panda[temp_column_name+'_bin_edges'].cat.categories

# get the averages of each bin
def get_average_of_bin_column(temp_panda,temp_column_name, temp_bin_count,temp_cfmid_energy):
    temp_bin_value_list=list()
    temp_subset_population_list=list()
    
    for i in range(0,temp_bin_count):
        subset_experimental_collision=temp_panda.loc[temp_panda[temp_column_name+'_bins'] == i]
        subset_cfmid_energy=subset_experimental_collision.loc[subset_experimental_collision['energy#'] == temp_cfmid_energy]
        #print(subset_experimental_collision)
        #print(subset_cfmid_energy)
        #hold=input('hold')
        temp_average=subset_cfmid_energy['dot_product'].mean()
        #print(temp_average)
        temp_subset_population=len(subset_cfmid_energy.index)
        ##print(temp_subset_population)
        #hold=input('hold')
        #print(temp_subset_population)
        if numpy.isnan(temp_average):
            temp_average=1.
        if numpy.isnan(temp_subset_population):
            temp_subset_population=0

        #print(temp_average)
        #hold=input('hold')
        temp_bin_value_list.append(1-temp_average)
        temp_subset_population_list.append(temp_subset_population)
    return temp_bin_value_list,temp_subset_population_list

def make_energy_average_figure(label_list,list_of_averages,hist_labels,output_base,adduct,other):
    matplotlib.pyplot.rcParams['font.size'] = 18
    matplotlib.pyplot.rcParams['axes.linewidth'] = 2

    #my_figure = matplotlib.pyplot.figure(figsize=(6, 6))
    #my_figure = matplotlib.pyplot.figure(figsize=(6.69292, 8))
    my_figure = matplotlib.pyplot.figure(figsize=(20, 8))

    matplotlib.pyplot.xlabel('Experimental Collision Energies')
    matplotlib.pyplot.ylabel('Average Dot Product')

    n,bins,patches=matplotlib.pyplot.hist(
        x=[numpy.arange(0,bin_count) for temp in range(0,3)],
        weights=list_of_averages,
        bins=bin_count,
        histtype='step',
        linewidth=3
    )
    my_axes=matplotlib.pyplot.gca()
    print(n)
    print(bins)
    print(len(bins))

    #done because of the way that pandas cut works. adds 1% to range
    #x_tick_spread=(float(hist_labels[-1]1])-float(hist_labels[0][0]))
    #lowest_edge=float(hist_labels[0].split(' ')[0][1:])
    #print(lowest_edge)
    #highest_edge=float(hist_labels[-1].split(' ')[1][:-1])
    #print(lowest_edge)
    #print(highest_edge-lowest_edge)
    #step_size=((highest_edge-lowest_edge)/1.001)/bin_count
    #print(list(numpy.arange(0,bin_count,step_size)))
    #my_axes.set_xticks(numpy.arange(0,bin_count,step_size))
    # #the normal approach
    # offset=((bins[0]-bins[1])/2)
    # my_axes.set_xticks([ bins[i]-offset for i in range(len(bins)-1) ])
    # my_axes.set_xticklabels(hist_labels,rotation=-90)
    # #the normal approach
    offset=((bins[0]-bins[1])/2)
    my_axes.set_xticks([ bins[i]-offset for i in range(0,len(bins)-1,3) ])
    my_axes.set_xticklabels(hist_labels[::3],rotation=-90)    


    my_axes.set_yticks(numpy.arange(0,1.2,0.2))
    y_plot_labels=['0','200','400','600','800','999']
    my_axes.set_yticklabels(y_plot_labels,rotation=0)

    matplotlib.pyplot.legend(label_list,loc='upper center')
    matplotlib.pyplot.tight_layout()
    #matplotlib.pyplot.show()
    total_output=output_base+adduct+'_'+other+'.png'
    matplotlib.pyplot.savefig(total_output)
    total_output=output_base+adduct+'_'+other+'.eps'
    matplotlib.pyplot.savefig(total_output)

def make_population_insert(bin_population_list,output_base,adduct,other):
    my_figure=matplotlib.pyplot.figure(figsize=(3.5,3))
    max_population_value=max(bin_population_list)
    bin_population_list=[bin_population_list[i]/max_population_value for i in range(0,len(bin_population_list))]
    n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,1)],weights=bin_population_list[0:bin_count],bins=int(bin_count),histtype='bar',linewidth=3)

    matplotlib.pyplot.xlabel('Bin')
    matplotlib.pyplot.ylabel('Relative Population')
    matplotlib.pyplot.tight_layout()
    total_output=output_base+'population_'+adduct+'_'+other+'.png'
    matplotlib.pyplot.savefig(total_output)
    total_output=output_base+'population_'+adduct+'_'+other+'.eps'
    matplotlib.pyplot.savefig(total_output)
    #matplotlib.pyplot.show()


if __name__ == "__main__":

    bin_count=200
    adduct='[M-H]-'
    instrument='hcd'
    cfmid_energy_list=['energy0','energy1','energy2']
    if instrument=='hcd':
        #instrument_brand='Orbitrap Fusion Lumos'
        instrument_brand='Thermo Finnigan Elite Orbitrap'
    else:
        instrument_brand='junk'
    lumos_use_eV=True
    #comment='thermo_raw_ev_on_x_axis'
    #comment='lumos_eV_set_raw_eV_on_x_axis'
    #comment='no_comments'
    comment='thermo_nce_times_precursormz_on_x_axis'
    #comment='lumos_eV_set_nce_times_precursormz_on_x_axis'

    input_address='../../results/'+adduct+'/'+instrument+'/precursor_no/binned_distances_'+adduct+'_'+instrument+'_precursor_no.txt'
    base_output_path='../../results/final_figures/energy_exploration/'+instrument+'/'

    

    # column_labels=[
    #     "999 to 950","949 to 900","899 to 850","849 to 800",
    #     "799 to 750","749 to 700","699 to 650","649 to 600",
    #     "599 to 550","549 to 500","499 to 450","449 to 400",
    #     "399 to 350","349 to 300","299 to 250","249 to 200",
    #     "199 to 150","149 to 100","99 to 50","49 to 0"]

    label_list=list()
    list_of_averages=list()
    hist_labels='to_be_replaced'

    for cfmid_energy in cfmid_energy_list:
        input_panda=pandas.read_csv(input_address,sep='¬')

        input_panda,new_collision_energy_name=transform_collision_energy_column(input_panda,instrument,instrument_brand,lumos_use_eV)
        edges=bin_column(input_panda,new_collision_energy_name,bin_count)
        bin_value_list,bin_population_list=get_average_of_bin_column(input_panda,new_collision_energy_name,bin_count,cfmid_energy)

        histo_labels=list()

        # print(edges)
        # hold=input('hold')

        for edge in edges:
            #####################MODIFIED FOR HCD########################
            temp_edge=str(edge)
            first_edge=temp_edge.split(', ')[0]
            second_edge=temp_edge.split(', ')[1]
            first_edge=first_edge[1:]
            second_edge=second_edge[:-1]
            first_edge_rounded=first_edge#round(float(first_edge))
            second_edge_rounded=second_edge#round(float(second_edge))
            #modified to get values for paper for oliver edits
            #        if x_label_counter%5==0:
            histo_labels.append('('+str(first_edge_rounded)+' '+str(second_edge_rounded)+']')
            #        else:
            #        histo_labels.append('')


        # print(histo_labels)
        # hold=input('hold')

        list_of_averages.append(bin_value_list)
        hist_labels=histo_labels
        label_list.insert(0,adduct+' '+instrument+' '+cfmid_energy)

    make_energy_average_figure(label_list,list_of_averages,hist_labels,base_output_path,adduct,comment)

    make_population_insert(bin_population_list,base_output_path,adduct,comment)