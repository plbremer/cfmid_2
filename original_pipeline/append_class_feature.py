import pandas

#####################CHANGED FOR SNAKEMAKE########################
input_panda_address=snakemake.input.input_panda_address
classyfire_results_address=snakemake.input.classyfire_results_address
output_dataset_address=snakemake.output.output_dataset_address
#####################CHANGED FOR SNAKEMAKE########################

input_panda=pandas.read_csv(input_panda_address,sep='¬',header=0)
classyfire_panda=pandas.read_csv(classyfire_results_address,sep='\t',header=0,usecols=['InChIKey','Superclass','Class'])

#superclass already existed, so we will just drop the columns then re add it
input_panda.drop(labels='Superclass',axis=1,inplace=True)

#add a column to the input panda that will hold the class and superclass
input_panda.insert(loc=input_panda.columns.size-1,column='Superclass',value='asdf')
input_panda.insert(loc=input_panda.columns.size-1,column='Class',value='asdf')
print(input_panda)


#replace the Superclass and Class null values with actual class information
row_counter=0
for index,row in input_panda.iterrows():
    if ((row_counter%10000)==0):
        print(row_counter)

    #get the inchikey of the experimental panda
    temp_inchikey=row['InChIKey']    
    #get the row in the classyfire panda
    classy_fire_row_panda=classyfire_panda.loc[  classyfire_panda['InChIKey']==temp_inchikey  ]
    #extract the rows from the classyfire panda
    temp_superclass=classy_fire_row_panda['Superclass'].item()
    temp_class=classy_fire_row_panda['Class'].item()
    #plug those values into the experimental panda
    input_panda.loc[index,'Superclass']=temp_superclass
    input_panda.loc[index,'Class']=temp_class

    row_counter+=1

input_panda.to_csv(output_dataset_address,sep='¬',index=False)