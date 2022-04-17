
import numpy
import pandas
import matplotlib.pyplot
import regex as re
import sys




def transform_collision_energy_column(input_panda,instrument,instrument_brand,use_entries_with_eV,put_eV_on_x_axis):
    if (instrument=='qtof'):
        return input_panda, 'Collision_energy'
    
    elif (instrument=='itft'):
        input_panda.insert(loc=len(input_panda.columns),column='Collision_energy_itft',value=35)
        return input_panda, 'Collision_energy_itft'

    elif (instrument=='hcd'):
        #input_panda.insert(loc=len(input_panda.columns),column='Collision_energy_hcd',value=-1)
        
        #subset the panda
        if  (instrument_brand=='Thermo_Finnigan_Elite_Orbitrap') and (use_entries_with_eV==True):
            input_panda=input_panda.loc[
                ((input_panda['Instrument']=='Thermo Finnigan Elite Orbitrap') & 
                (input_panda['Collision_energy'].str.contains('eV'))),
                input_panda.columns
            ]
        elif  (instrument_brand=='Thermo_Finnigan_Elite_Orbitrap') and (use_entries_with_eV==False):
            input_panda=input_panda.loc[
                (input_panda['Instrument']=='Thermo Finnigan Elite Orbitrap') & 
                (~(input_panda['Collision_energy'].str.contains('eV'))),
                input_panda.columns
            ]
        elif (instrument_brand=='Orbitrap_Fusion_Lumos') and (use_entries_with_eV==True):
            input_panda=input_panda.loc[
                (input_panda['Instrument']=='Orbitrap Fusion Lumos') & 
                (input_panda['Collision_energy'].str.contains('eV')),
                input_panda.columns
            ]
        elif (instrument_brand=='Orbitrap_Fusion_Lumos') and (use_entries_with_eV==False):
            input_panda=input_panda.loc[
                (input_panda['Instrument']=='Orbitrap Fusion Lumos') & 
                (~(input_panda['Collision_energy'].str.contains('eV'))),
                input_panda.columns
            ]
        elif (instrument_brand=='both') and (use_entries_with_eV==True):
            input_panda=input_panda.loc[
                (input_panda['Collision_energy'].str.contains('eV')),
                input_panda.columns
            ]
        elif (instrument_brand=='both') and (use_entries_with_eV==False):
            input_panda=input_panda.loc[
                (~(input_panda['Collision_energy'].str.contains('eV'))),
                input_panda.columns
            ]

        if put_eV_on_x_axis==True:
            input_panda['Collision_energy_hcd']=input_panda['Collision_energy'].str.findall(r'[0-9]+').str[1].astype(float)
        elif put_eV_on_x_axis==False:
            input_panda['Collision_energy_hcd']=input_panda['Collision_energy'].str.findall(r'[0-9]+').str[0].astype(float)
            input_panda['Collision_energy_hcd']=input_panda['Collision_energy_hcd'].multiply(input_panda['PrecursorMZ'])

        return input_panda, 'Collision_energy_hcd'


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

def make_energy_average_figure(label_list,list_of_averages,hist_labels,output_base,adduct,instrument,instrument_brand,use_entries_with_eV,put_eV_on_x_axis):
    matplotlib.pyplot.rcParams['font.size'] = 18
    matplotlib.pyplot.rcParams['axes.linewidth'] = 2

    #my_figure = matplotlib.pyplot.figure(figsize=(6, 6))
    my_figure = matplotlib.pyplot.figure(figsize=(6.69292, 8))
    #my_figure = matplotlib.pyplot.figure(figsize=(20, 8))

    if instrument=='qtof' and adduct=='[M+H]+':
        matplotlib.pyplot.xlabel('Experimental Collision Energies (eV)')
    elif instrument=='hcd' and adduct=='[M+H]+':
        #matplotlib.pyplot.xlabel('Experimental Collision Energies (eV)')
        matplotlib.pyplot.xlabel('Precursor Mass (Da) × %NCE')
    matplotlib.pyplot.ylabel('Average Dot Product')

    if instrument=='qtof' and adduct=='[M+H]+':
        n,bins,patches=matplotlib.pyplot.hist(
            x=[numpy.arange(0,bin_count) for temp in range(0,3)],
            weights=list_of_averages,
            bins=bin_count,
            histtype='step',
            linewidth=3,
            color=['darkorange','darkorchid','darkcyan']
        )
    elif instrument=='hcd' and adduct=='[M+H]+':
        n,bins,patches=matplotlib.pyplot.hist(
            x=[numpy.arange(0,bin_count/4) for temp in range(0,3)],
            weights=[list_of_averages[0][0:50],list_of_averages[1][0:50],list_of_averages[2][0:50]],
            # x=[numpy.arange(0,bin_count) for temp in range(0,3)],
            # weights=list_of_averages,
            bins=50,#bin_count
            histtype='step',
            linewidth=3,
            color=['darkorange','darkorchid','darkcyan']
        )
    my_axes=matplotlib.pyplot.gca()
    # print(n)
    # print(bins)
    # print(len(bins))

    # if instrument=='hcd' and adduct=='[M+H]+':
    #     n=n[0:50]
    #     bins=bins[0:50]
    #     patches=patches[0:50]
    #     hist_labels=hist_labels[0:49]


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
    
    #my_axes.set_xticklabels(hist_labels[::3],rotation=-90)   
    if instrument=='qtof' and adduct=='[M+H]+':
        x_labels=[' ' for i in range(len(hist_labels))]
        x_labels[0]='1'
        x_labels[8]='10'
        x_labels[18]='20'
        x_labels[38]='40'
        my_axes.set_xticks([ bins[i]-offset for i in range(0,len(bins)-1) ])
        my_axes.set_xticklabels(x_labels)#,rotation=-90)
    elif instrument=='hcd' and adduct=='[M+H]+':
        #x_labels=[' ' for i in range((50))]
        #x_labels[0]='1'
        #x_labels[7]='10'
        #x_labels[14]='20'
        #x_labels[28]='40'
        #x_labels[35]='50'
        #x_labels[49]='70'
        
        #by manually looking at the image with all 50, we can come up with the ranges
        #that we need, for example, x_labels[0] needs 64 to 916. we take the middle (average) of each
        x_labels=[' ' for i in range((50))]
        x_labels[0]='490'
        x_labels[7]='5,529'
        x_labels[14]='10,497'
        x_labels[28]='20,788'
        x_labels[35]='25,401'
        x_labels[49]='35,337'
        my_axes.set_xticks([ bins[i]-offset for i in range(0,len(bins)-1) ])
        my_axes.set_xticklabels(x_labels,rotation=-90)
        
        #my_axes.set_xticklabels(hist_labels[0:50],rotation=-90) 
    

    my_axes.set_yticks(numpy.arange(0,1.2,0.2))
    y_plot_labels=['0','200','400','600','800','999']
    my_axes.set_yticklabels(y_plot_labels,rotation=0)

    if instrument=='qtof' and adduct=='[M+H]+':
        legend_labels=[
            '[M+H]+ Q-TOF, CFM-ID 40',
            '[M+H]+ Q-TOF, CFM-ID 20',
            '[M+H]+ Q-TOF, CFM-ID 10',
        ]
    elif instrument=='hcd' and adduct=='[M+H]+':
        legend_labels=[
            '[M+H]+ HCD-Orbitrap, CFM-ID 40',
            '[M+H]+ HCD-Orbitrap, CFM-ID 20',
            '[M+H]+ HCD-Orbitrap, CFM-ID 10',
        ]

    matplotlib.pyplot.legend(legend_labels,loc='upper center')
    matplotlib.pyplot.tight_layout()
    #matplotlib.pyplot.show()
    total_output=output_base+adduct+'_'+instrument+'_'+instrument_brand+'_ev_entries:_'+str(use_entries_with_eV)+'_ev_on_x:_'+str(put_eV_on_x_axis)+'.png'
    matplotlib.pyplot.savefig(total_output)
    total_output=output_base+adduct+'_'+instrument+'_'+instrument_brand+'_ev_entries:_'+str(use_entries_with_eV)+'_ev_on_x:_'+str(put_eV_on_x_axis)+'.eps'
    matplotlib.pyplot.savefig(total_output)

def make_population_insert(bin_population_list,output_base,adduct,instrument,instrument_brand,use_entries_with_eV,put_eV_on_x_axis):
    my_figure=matplotlib.pyplot.figure(figsize=(3.5,3))
    max_population_value=max(bin_population_list)
    bin_population_list=[bin_population_list[i]/max_population_value for i in range(0,len(bin_population_list))]
    n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,1)],weights=bin_population_list[0:bin_count],bins=int(bin_count),histtype='bar',linewidth=3)

    matplotlib.pyplot.xlabel('Bin')
    matplotlib.pyplot.ylabel('Relative Population')
    matplotlib.pyplot.tight_layout()
    total_output=output_base+'population_'+adduct+'_'+instrument+'_'+instrument_brand+'_ev_entries:_'+str(use_entries_with_eV)+'_ev_on_x:_'+str(put_eV_on_x_axis)+'.png'
    matplotlib.pyplot.savefig(total_output)
    total_output=output_base+'population_'+adduct+'_'+instrument+'_'+instrument_brand+'_ev_entries:_'+str(use_entries_with_eV)+'_ev_on_x:_'+str(put_eV_on_x_axis)+'.eps'
    matplotlib.pyplot.savefig(total_output)
    #matplotlib.pyplot.show()


if __name__ == "__main__":

    # bin_count=44
    # adduct='[M+H]+'
    # instrument='qtof'
    # instrument_brand='junk'
    # use_entries_with_eV='junk'
    # put_eV_on_x_axis='junk'

    bin_count=200
    adduct='[M+H]+'
    instrument='hcd'
    #instrument_brand='Orbitrap_Fusion_Lumos'
    instrument_brand='Thermo_Finnigan_Elite_Orbitrap'
    use_entries_with_eV=True
    put_eV_on_x_axis=False

    # bin_count=int(sys.argv[1])
    # adduct=sys.argv[2]
    # instrument=sys.argv[3]
    # #instrument_brand='Orbitrap_Fusion_Lumos'
    # instrument_brand=sys.argv[4]
    # use_entries_with_eV=bool(int(sys.argv[5]))
    # put_eV_on_x_axis=bool(int(sys.argv[6]))


    cfmid_energy_list=['energy0','energy1','energy2']
    input_address_pos='../../../results/[M+H]+/'+instrument+'/precursor_no/binned_distances_[M+H]+_'+instrument+'_precursor_no.txt'
    input_address_neg='../../../results/[M-H]-/'+instrument+'/precursor_no/binned_distances_[M-H]-_'+instrument+'_precursor_no.txt'
    base_output_path='../../../results/energy_exploration/'+instrument+'/'

    

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
        if adduct=='[M+H]+':
            input_panda=pandas.read_csv(input_address_pos,sep='¬',engine='python')
        elif adduct=='[M-H]-':
            input_panda=pandas.read_csv(input_address_neg,sep='¬',engine='python')
        elif adduct=='both':
            input_panda_pos=pandas.read_csv(input_address_pos,sep='¬',engine='python')
            input_panda_neg=pandas.read_csv(input_address_neg,sep='¬',engine='python')
            input_panda=pandas.concat([input_panda_pos,input_panda_neg],axis='index')

        input_panda,new_collision_energy_name=transform_collision_energy_column(
            input_panda,
            instrument,
            instrument_brand,
            use_entries_with_eV,
            put_eV_on_x_axis
            )

        #to see number of spectra times 3
        print(input_panda)
        #hold=input('hold')

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

    make_energy_average_figure(
        label_list,
        list_of_averages,
        hist_labels,
        base_output_path,
        adduct,
        instrument,
        instrument_brand,
        use_entries_with_eV,
        put_eV_on_x_axis
    )
    # make_population_insert(
    #     bin_population_list,
    #     base_output_path,
    #     adduct,
    #     instrument,
    #     instrument_brand,
    #     use_entries_with_eV,
    #     put_eV_on_x_axis
    # )
