import numpy
import pandas
import seaborn
import matplotlib.pyplot

cfmid_energy='energy2'
adduct='[M+H]+'
instrument='qtof'
bin_count=int('20')
input_address='/home/rictuar/coding_projects/fiehn_work/text_files/orthogonal_snakemake/'+adduct+'/'+instrument+'/precursor_yes/binned_distances_'+adduct+'_'+instrument+'_precursor_yes.txt'

column_labels=["999 to 950","949 to 900","899 to 850","849 to 800",
"799 to 750","749 to 700","699 to 650","649 to 600",
"599 to 550","549 to 500","499 to 450","449 to 400",
"399 to 350","349 to 300","299 to 250","249 to 200",
"199 to 150","149 to 100","99 to 50","49 to 0"]



input_panda=pandas.read_csv(input_address,sep='¬')
#print(input_panda)

#def make_numerical_collision_energy_column(temp_panda,temp_instrument):
    #do stuff

def bin_column(temp_panda, temp_column_name, temp_bin_count):
    column_bin_integers=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count,labels=False)
    column_bin_edges=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count)
    
    #print(column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bins',value=column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bin_edges',value=column_bin_edges)
    return temp_panda[temp_column_name+'_bin_edges'].cat.categories
    #return column_bin_edges


edges=bin_column(input_panda,'Collision_energy',bin_count)







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


###############get row labels#################
row_labels=list()
for edge in edges:
    row_labels.append(str(edge))
#print(row_labels)
row_labels=list(row_labels)
#row_labels.sort()
#print(row_labels)
#hold=input('hold')
#print(input_panda)
#print(input_panda['Collision_energy'].value_counts())

#append population to row label
for i in range(0,len(row_labels)):
    row_labels[i]=row_labels[i]+' '+str(numpy.sum(two_d_histogram[i]))
#print(row_labels)
#hold=input('hold')
######################################################




#make histogram into neat panda
temp_hist_panda=pandas.DataFrame(two_d_histogram,columns=column_labels,index=row_labels)


#temp_hist_panda.drop(labels='49 to 0',axis=1,inplace=True)


#normalize rows
temp_hist_panda=temp_hist_panda.div(temp_hist_panda.sum(axis=1),axis=0)




print(temp_hist_panda)

seaborn.heatmap(temp_hist_panda)
matplotlib.pyplot.show()
#def normalize_rows

