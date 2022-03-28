import pandas


#######################adjusted for snakemade###############################
input_panda_address=snakemake.input.input_panda_address
number_of_ranks=snakemake.params.number_of_ranks
feature=snakemake.params.feature
feature_list_user_specified=snakemake.params.feature_list_user_specified
output_dataset_address=snakemake.output.output_dataset_address
#######################adjusted for snakemade###############################

input_panda=pandas.read_csv(input_panda_address,sep='¬',header=0)

#get list of feature values
#this can be from a hand-given list (in order to make 1 cohorts heatmap comparable to another)
#or from the range of possibel values produced by a given list

if (not feature_list_user_specified):
    #create a list of unique values for the given feature
    feature_list=input_panda[feature].unique()


my_heatmap_panda=pandas.DataFrame(index=feature_list,columns=list(range(0,number_of_ranks)),dtype=int)

#set all the nan values to zero
my_heatmap_panda.fillna(value=0,inplace=True)

#get a list of the number of ranks available
#lets keep this simple and make it user defined to be 25...?
#why would i do it this way
for i in range(0,number_of_ranks):

    temp_subset=input_panda.loc[input_panda['bins']==i]
    
    #on each rank, iterature through the series that is the featurevalues that appear
    #for feature_value in temp_subset[feature].value_counts():

    for feature_value in temp_subset[feature].value_counts().iteritems():

        my_heatmap_panda.loc[feature_value[0],i]=feature_value[1]


def add_row_sum_to_feature_name(temp_panda):
    column_of_norms=temp_panda.sum(axis=1)

    temp_panda.index=column_of_norms.astype(str) + '    ' +temp_panda.index.astype(str)

    return temp_panda

def normalize_by_row(temp_panda):
    
    column_of_norms=temp_panda.sum(axis=1)

    temp_panda=temp_panda.div(other=column_of_norms,axis=0)

    return temp_panda

    
my_heatmap_panda=add_row_sum_to_feature_name(my_heatmap_panda)

my_heatmap_panda=normalize_by_row(my_heatmap_panda)

my_heatmap_panda.to_csv(output_dataset_address,sep='¬')