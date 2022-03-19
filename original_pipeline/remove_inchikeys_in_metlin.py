
orthogonal_similarity_input_address=snakemake.input.orthogonal_similarity_input_address

metlin_inchikey_address=snakemake.input.metlin_inchikey_address

orthogonal_similarity_output_address=snakemake.output.orthogonal_similarity_output_address


def get_set_of_firstblock_from_list(inchikey_list_address):

    inchikey_file=open(inchikey_list_address,'r')

    inchikey_firstblock_set=set()
    for line in inchikey_file:
        temp_firstblock=line.split('-')
        inchikey_firstblock_set.add(temp_firstblock[0])

    inchikey_file.close()

    return inchikey_firstblock_set



#remove inchikey from file
def remove_inchikeys_from_file_based_on_inchikey_list_orthogonal_similarity(file_address_to_remove,list_of_inchikey_address,output_address):
    inchikey_firstblock_set=get_set_of_firstblock_from_list(list_of_inchikey_address)

    file_to_cleanse=open(file_address_to_remove,'r')
    output_file=open(output_address,'w')
    line_counter=0
    for line in file_to_cleanse:
        if(line_counter==0):
            output_file.write(line)
            line_counter+=1
            continue
        if(line_counter%10000==0):
            print(line_counter)
        line_counter+=1

        #get the firstblock
        file_inchikey=values=line.split('¬')[8]
        file_inchikey_firstblock=file_inchikey.split('-')[0]
        #if the firstblock is not in set, write to file

        if (file_inchikey_firstblock not in inchikey_firstblock_set):
            output_file.write(line)

    file_to_cleanse.close()
    output_file.close()


remove_inchikeys_from_file_based_on_inchikey_list_orthogonal_similarity(orthogonal_similarity_input_address,metlin_inchikey_address,orthogonal_similarity_output_address)
