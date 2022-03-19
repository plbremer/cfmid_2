import pandas
import numpy
#thsi script takes the distances and puts them into a specified number of bins

####################
binned_csv_address=snakemake.input.binned_csv_address
best_cfmid_selected_address=snakemake.output.best_cfmid_selected_address
number_of_bins=snakemake.params.number_of_bins
distance_method=snakemake.params.distance_method
####################

one_cohort_panda=pandas.read_csv(binned_csv_address,sep='¬')

def make_boolean_mask_of_greatest(temp_panda):

    boolean_mask=list()

    for i in range(0,len(temp_panda.index),3):

        #get value of lowest
        min_distance=min(temp_panda.loc[i,distance_method],temp_panda.loc[i+1,distance_method],temp_panda.loc[i+2,distance_method])

        for j in range(0,3):
            if (temp_panda.loc[i+j,distance_method]==min_distance):
                boolean_mask.append(True)
            else:
                boolean_mask.append(False)

    return boolean_mask

#get the boolean mask
mask=make_boolean_mask_of_greatest(one_cohort_panda)
#make the subset based on the mask
best_match_selected_panda=one_cohort_panda.loc[ mask ]
#write the subset to file
best_match_selected_panda.to_csv(best_cfmid_selected_address,sep='¬',index=False)