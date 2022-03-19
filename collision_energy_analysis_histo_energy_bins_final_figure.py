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
#cfmid_energy=sys.argv[3]
cfmid_energy_list=['energy0','energy1','energy2']

instrument_brand='Orbitrap Fusion Lumos'

input_address='../../results/'+adduct+'/'+instrument+'/precursor_no/binned_distances_'+adduct+'_'+instrument+'_precursor_no.txt'
base_output_path='../../results/'

bin_count=int('200')

column_labels=["999 to 950","949 to 900","899 to 850","849 to 800",
"799 to 750","749 to 700","699 to 650","649 to 600",
"599 to 550","549 to 500","499 to 450","449 to 400",
"399 to 350","349 to 300","299 to 250","249 to 200",
"199 to 150","149 to 100","99 to 50","49 to 0"]


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
                temp_panda.at[index,'Collision_energy_hcd_lumos_NCE_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])
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


def bin_column(temp_panda, temp_column_name, temp_bin_count):
    column_bin_integers=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count,labels=False)
    column_bin_edges=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count)
    
    #print(column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bins',value=column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bin_edges',value=column_bin_edges)
    return temp_panda[temp_column_name+'_bin_edges'].cat.categories
    #return column_bin_edges


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
        print(temp_subset_population)
        if numpy.isnan(temp_average):
            temp_average=1.
        if numpy.isnan(temp_subset_population):
            temp_subset_population=0

        #print(temp_average)
        #hold=input('hold')
        temp_bin_value_list.append(1-temp_average)
        temp_subset_population_list.append(temp_subset_population)
    return temp_bin_value_list,temp_subset_population_list

LABEL_LIST=list()
LIST_OF_AVERAGES=list()
HIST_LABELS='to_be_replaced'

for cfmid_energy in cfmid_energy_list:
    input_panda=pandas.read_csv(input_address,sep='¬')
    input_panda,new_collision_energy_name=transform_collision_energy_column(input_panda,instrument,instrument_brand)
    edges=bin_column(input_panda,new_collision_energy_name,bin_count)
    bin_value_list,bin_population_list=get_average_of_bin_column(input_panda,new_collision_energy_name,bin_count,cfmid_energy)
    ###############get histogram labels#################
    histo_labels=list()
    
    x_label_counter=0
    for edge in edges:
        
        #####################MODIFIED FOR HCD########################
        temp_edge=str(edge)
        first_edge=temp_edge.split(', ')[0]
        second_edge=temp_edge.split(', ')[1]
        first_edge=first_edge[1:]
        second_edge=second_edge[:-1]
        first_edge_rounded=round(float(first_edge))
        second_edge_rounded=round(float(second_edge))
#modified to get values for paper for oliver edits
#        if x_label_counter%5==0:
        histo_labels.append('('+str(first_edge_rounded)+' '+str(second_edge_rounded)+']')
#        else:
#        histo_labels.append('')
        x_label_counter+=1

        
        ###################################################################
        
        #if x_label_counter%5==0:
        #    histo_labels.append(str(edge))
        #else:
        #    histo_labels.append('')
        #x_label_counter+=1

    #print(histo_labels)
    histo_labels=list(histo_labels)
    ####################################################
    ##########append population to row label############
    #for i in range(0,len(histo_labels)):
    #    histo_labels[i]=histo_labels[i]+' '+str( bin_population_list[i]   )
    ######################################################
    #######add shit to global variable carriers#########
    LIST_OF_AVERAGES.append(bin_value_list)
    HIST_LABELS=histo_labels
    LABEL_LIST.append(adduct+' '+instrument+' '+cfmid_energy)
    ####################################################

#if (instrument=='qtof'):
LABEL_LIST=['CFM-ID Energy 10','CFM-ID Energy 20','CFM-ID Energy 40']


####################prepare histogram image#######################################
matplotlib.rcParams['font.family'] = 'Avenir'
matplotlib.pyplot.rcParams['font.size'] = 18
matplotlib.pyplot.rcParams['axes.linewidth'] = 2

#my_figure = matplotlib.pyplot.figure(figsize=(6, 6))
my_figure = matplotlib.pyplot.figure(figsize=(6.69292, 8))

matplotlib.pyplot.xlabel('Experimental Collision Energies')
matplotlib.pyplot.ylabel('Average Dot Product')
#######################modified for HCD###############################3

n,bins,patches=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,3)],weights=LIST_OF_AVERAGES,bins=bin_count,histtype='step',linewidth=3)

#cut to one half
print(bin_count/2)
#n,bins,patches=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count/4) for temp in range(0,3)],weights=[LIST_OF_AVERAGES[0][0:50],LIST_OF_AVERAGES[1][0:50],LIST_OF_AVERAGES[2][0:50]],bins=int(bin_count/4),histtype='step',linewidth=3)

##########################################################################




#transpose for plot
print(LIST_OF_AVERAGES)
LIST_OF_AVERAGES=numpy.array(LIST_OF_AVERAGES)
LIST_OF_AVERAGES=LIST_OF_AVERAGES.T

#matplotlib.pyplot.plot(LIST_OF_AVERAGES,marker='_',linestyle='None',markeredgewidth=5,markersize=19)
#print(patches[0])
#patches[0][0].set_xy(patches[0][0].get_xy()[1:-1])
'''
for i in range(0,len(patches)):
    for j in range(0,len(patches[i])):
        #patches[i][j].set_xy(patches[i][j].get_xy()[1:-1])
        print(patches[i][j].get_xy())
        hold=input('hold')
'''


my_axes=matplotlib.pyplot.gca()



#######################MODIFIED FOR HCD###############################
my_axes.set_xticks(numpy.arange(0,bin_count))
#my_axes.set_xticks(numpy.arange(0,int(bin_count/4)))
my_axes.set_xticklabels(HIST_LABELS,rotation=-90)
#my_axes.set_xticklabels(HIST_LABELS[0:50],rotation=-90)
######################################################################

my_axes.set_yticks(numpy.arange(0,1,0.2))
y_plot_labels=['0','200','400','600','800','999']

matplotlib.pyplot.legend(LABEL_LIST,loc='upper center')

matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'.eps',bbox_inches="tight")
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'.png',bbox_inches="tight")
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()
'''
#create array of ones
temp_array=numpy.arange(0,bin_count,1)
matplotlib.pyplot.figure(figsize=(15,5))
temp_hist_plot=matplotlib.pyplot.bar(x=temp_array,height=bin_value_list,tick_label=histo_labels)
matplotlib.pyplot.xticks(rotation=270,horizontalalignment='center')
matplotlib.pyplot.ylim([0,1])
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()
#matplotlib.pyplot.savefig(base_output_path+adduct+'_'+instrument+'_'+cfmid_energy)
#make histogram into neat panda
#temp_hist_panda=pandas.DataFrame(two_d_histogram,columns=column_labels,index=row_labels)
'''


#make the population inset
#bin_population_list
#matplotlib.pyplot.
my_figure=matplotlib.pyplot.figure(figsize=(3.5,3))

max_population_value=max(bin_population_list)
bin_population_list=[bin_population_list[i]/max_population_value for i in range(0,len(bin_population_list))]

#my_figure=matplotlib.pyplot.figure(figsize=(3.34646,4))

#n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,1)],weights=bin_population_list,bins=bin_count,histtype='bar',linewidth=3)

#######################MODIFIED FOR HCD###############################
n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,1)],weights=bin_population_list,bins=bin_count,histtype='bar',linewidth=3)
#n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count/4) for temp in range(0,1)],weights=bin_population_list[0:50],bins=int(bin_count/4),histtype='bar',linewidth=3)

######################################################################



matplotlib.pyplot.xlabel('Bin')
matplotlib.pyplot.ylabel('Relative Population')
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'_inset.eps')
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'_inset.png')

matplotlib.pyplot.show()
