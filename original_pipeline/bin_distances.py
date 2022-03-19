import pandas
import numpy
#this script takes the distances and puts them into a specified number of bins

###################
one_cohort_file_address=snakemake.input.one_cohort_file_address
binned_output_csv_address=snakemake.output.binned_output_csv_address
number_of_bins=snakemake.params.number_of_bins
distance_method=snakemake.params.distance_method
##################

#read in panda
one_cohort_panda=pandas.read_csv(one_cohort_file_address,sep='¬')

#generate cusstom interval range (defines the bins)
bins=pandas.interval_range(start=-0.0001,end=1,periods=number_of_bins)

#bin the data
#broke on purpose so i come back to it
binned_distances=pandas.cut(one_cohort_panda[distance_method].to_list(),bins=bins,labels=range(0,number_of_bins))

#give the categories attribute of binsa name
binned_distances.categories=range(0,number_of_bins)

#create a new column with the bin labels and bin values
one_cohort_panda['bins']=numpy.nan
one_cohort_panda['bins']=binned_distances

#output the bin
one_cohort_panda.to_csv(binned_output_csv_address,sep='¬',index=False)