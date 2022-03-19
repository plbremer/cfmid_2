import numpy
import pandas
import seaborn
import matplotlib.pyplot
import re
import sys

#adduct='[M-H]-'
#instrument='qtof'
#cfmid_energy='energy0'

adduct=sys.argv[1]
instrument=sys.argv[2]
cfmid_energy=sys.argv[3]


instrument_brand='Orbitrap Fusion Lumos'
bin_count=int('50')
input_address='/home/rictuar/coding_projects/fiehn_work/text_files/orthogonal_snakemake/'+adduct+'/'+instrument+'/precursor_yes/binned_distances_'+adduct+'_'+instrument+'_precursor_yes.txt'
base_output_path='/home/rictuar/coding_projects/fiehn_work/text_files/_collision_energy_images/'
column_labels=["999 to 950","949 to 900","899 to 850","849 to 800",
"799 to 750","749 to 700","699 to 650","649 to 600",
"599 to 550","549 to 500","499 to 450","449 to 400",
"399 to 350","349 to 300","299 to 250","249 to 200",
"199 to 150","149 to 100","99 to 50","49 to 0"]




input_panda=pandas.read_csv(input_address,sep='¬')
#print(input_panda)

def transform_collision_energy_column(temp_panda,temp_instrument,temp_instrument_brand):
    if (temp_instrument=='qtof'):
        return temp_panda, 'Collision_energy'
    
    elif (temp_instrument=='itft'):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_itft',value=35)
        return temp_panda, 'Collision_energy_itft'

    #elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Thermo Finnigan Elite Orbitrap')):


    elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Orbitrap Fusion Lumos')):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_hcd_lumos_NCE_only',value=-1)
        #print(temp_panda)
        #hold=input('hold')


        for index,row in temp_panda.iterrows():
            #if the collision energy column contains eV, skip it
            if 'eV' in row['Collision_energy']:
                #print(row['Collision_energy'])
                #hold=input('hold')
                continue
            else:
                #print(row['Collision_energy'])
                #hold=input('hold')
                #print(row['Collision_energy_hcd_lumos_NCE_only'])
                #hold=input('hold')
                #print((re.findall(r'[0-9]+',row['Collision_energy']))[0])
                #hold=input('hold')
                temp_panda.loc[index,'Collision_energy_hcd_lumos_NCE_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])
                #hold=input('hold')
                #print(row['Collision_energy_hcd_lumos_NCE_only'])
                #hold=input('hold')
        
        
        
        
        #############################if lumos and hcd##################################
        #subset panda to make rest of script still work
        ##############################################################################
        temp_panda=temp_panda.loc[temp_panda['Collision_energy_hcd_lumos_NCE_only'] != -1]
        #print(temp_panda)
        #hold=input('hold')
        #############################if lumos and hcd##################################
        #divide column by precursor mz to figure out normalization
        ##############################################################################        
        temp_panda['Collision_energy_hcd_lumos_NCE_only']=temp_panda['Collision_energy_hcd_lumos_NCE_only'].multiply(temp_panda['PrecursorMZ'])
        #print(temp_panda)
        #hold=input('hold')        
        return temp_panda, 'Collision_energy_hcd_lumos_NCE_only'


#print(input_panda)

input_panda,new_collision_energy_name=transform_collision_energy_column(input_panda,instrument,instrument_brand)
#print(input_panda)
#hold=input('hold')


def bin_column(temp_panda, temp_column_name, temp_bin_count):
    column_bin_integers=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count,labels=False)
    column_bin_edges=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count)
    
    #print(column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bins',value=column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bin_edges',value=column_bin_edges)
    return temp_panda[temp_column_name+'_bin_edges'].cat.categories
    #return column_bin_edges


edges=bin_column(input_panda,new_collision_energy_name,bin_count)
#print(input_panda)
#hold=input('hold')

#print(edges)
#hold=input('edges')
# get the averages of each bin
def get_average_of_bin_column(temp_panda,temp_column_name, temp_bin_count,temp_cfmid_energy):
    temp_bin_value_list=list()
    temp_subset_population_list=list()
    
    for i in range(0,temp_bin_count):
        subset_experimental_collision=temp_panda.loc[temp_panda[temp_column_name+'_bins'] == i]
        subset_cfmid_energy=subset_experimental_collision.loc[subset_experimental_collision['energy#'] == temp_cfmid_energy]
        #print(subset_cfmid_energy)
        temp_average=subset_cfmid_energy['dot_product'].mean()
        temp_subset_population=len(subset_cfmid_energy.index)
#        print(temp_subset_population)
        if numpy.isnan(temp_average):
            temp_average=1.
        if numpy.isnan(temp_subset_population):
            temp_subset_population=0

        #print(temp_average)
        #hold=input('hold')
        temp_bin_value_list.append(1-temp_average)
        temp_subset_population_list.append(temp_subset_population)
    return temp_bin_value_list,temp_subset_population_list


bin_value_list,bin_population_list=get_average_of_bin_column(input_panda,new_collision_energy_name,bin_count,cfmid_energy)
#print(bin_value_list)
#hold=input('hold')

#


'''

#other oclumn assumed to be dot product
def populate_histogram_from_panda(temp_panda,temp_column_name_for_rows,temp_bin_count):

    #declare temp histogram
    temp_two_d_histogram=numpy.zeros(shape=(temp_bin_count,20))
    #print(temp_two_d_histogram)
    #rows to be the collision energy stuff
    #columns to be the similarity stuff

    #scroll through panda, increment position
    for index, row in temp_panda.iterrows():
        
        if row['energy#'] != cfmid_energy:
            continue

        #get the bin that the collision energy was put into
        temp_collision_bin=row[temp_column_name_for_rows+'_bins']
        #print(temp_collision_bin)
        temp_similarity_bin=row['bins']
        #print(temp_similarity_bin)

        #increment bin
        temp_two_d_histogram[temp_collision_bin,temp_similarity_bin]+=1
        #print(print(temp_two_d_histogram))

        #hold=input('hold')
    return temp_two_d_histogram

two_d_histogram=populate_histogram_from_panda(input_panda,'Collision_energy',bin_count)
'''

###############get histogram labels#################
histo_labels=list()
for edge in edges:
    histo_labels.append(str(edge))
#print(histo_labels)
histo_labels=list(histo_labels)

#histo_labels.sort()
#print(histo_labels)
#hold=input('hold')
#print(input_panda)
#print(input_panda['Collision_energy'].value_counts())






#append population to row label
for i in range(0,len(histo_labels)):
    #get number in group

    
    histo_labels[i]=histo_labels[i]+' '+str( bin_population_list[i]   )
#print(row_labels)
#hold=input('hold')
######################################################

#print(histo_labels)
#hold=input('hold')

####################prepare histogram image#######################################

#create array of ones
temp_array=numpy.arange(0,bin_count,1)
matplotlib.pyplot.figure(figsize=(15,5))
temp_hist_plot=matplotlib.pyplot.bar(x=temp_array,height=bin_value_list,tick_label=histo_labels)
matplotlib.pyplot.xticks(rotation=270,horizontalalignment='center')
matplotlib.pyplot.ylim([0,1])
matplotlib.pyplot.tight_layout()
#matplotlib.pyplot.show()
matplotlib.pyplot.savefig(base_output_path+adduct+'_'+instrument+'_'+cfmid_energy)
#make histogram into neat panda
#temp_hist_panda=pandas.DataFrame(two_d_histogram,columns=column_labels,index=row_labels)


#temp_hist_panda.drop(labels='49 to 0',axis=1,inplace=True)


#normalize rows
#temp_hist_panda=temp_hist_panda.div(temp_hist_panda.sum(axis=1),axis=0)




#print(temp_hist_panda)

#seaborn.heatmap(temp_hist_panda)

#def normalize_rows

