import pandas
import regex

###################replaced for snakemake############################
input_address=snakemake.input.input_address
output_dataset_address=snakemake.output.output_dataset_address
###################replaced for snakemake############################
input_panda=pandas.read_csv(input_address,sep='¬',header=0)


def parse_collision_energy(temp_string):
  
    try:
        percent=float(regex.findall('NCE=(.*)\%',temp_string)[0])
    except IndexError:
        percent='null'
    try:
        eV=float(regex.findall('\%\ (.*)eV',temp_string)[0])
    except:
        eV='null'
    
    return percent,eV
    

def split_collision_energy_column(temp_panda):

    for index,row in temp_panda.iterrows():

        if row['Instrument_type']=='HCD':
            percent, eV=parse_collision_energy(row['Collision_energy'])
            temp_panda.loc[index, 'orbi_collision_energy']=percent
            
        elif row['Instrument_type']=='IT-FT/ion trap with FTMS':
            percent, eV=parse_collision_energy(row['Collision_energy'])

            temp_panda.loc[index, 'Collision_energy']=percent   
    
    
        
split_collision_energy_column(input_panda)


input_panda.to_csv(output_dataset_address,sep='¬',index=False)