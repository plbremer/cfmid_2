import pandas

#################
input_panda_address=snakemake.input.input_panda_address
output_panda_address=snakemake.output.output_panda_address
#################
input_panda=pandas.read_csv(input_panda_address,sep='¬',header=0)

def fill_cfmid_collision_energy_column(temp_panda):

    #iterrate through entire panda
    for index,row in temp_panda.iterrows():

        #if the rank observed is lower than the lowest rank, record that
        if row['energy#']=='energy0':
            temp_panda.loc[index,'cfmid-collision']='10-'+str(row['Collision_energy'])

        elif row['energy#']=='energy1':
            temp_panda.loc[index,'cfmid-collision']='20-'+str(row['Collision_energy'])

        elif row['energy#']=='energy2':
            temp_panda.loc[index,'cfmid-collision']='40-'+str(row['Collision_energy'])
        

input_panda.insert(loc=input_panda.columns.size-2,column='cfmid-collision',value='null')
fill_cfmid_collision_energy_column(input_panda)

input_panda.to_csv(output_panda_address,sep='¬',index=False)
