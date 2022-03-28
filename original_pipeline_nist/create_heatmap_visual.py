import pandas
import seaborn

#################edited for snakemake##############################
input_panda_address=snakemake.input.input_panda_address
output_heatmap_address=snakemake.output.output_heatmap_address
#################edited for snakemake##############################



clustermap_panda=pandas.read_csv(input_panda_address,sep='¬',index_col=0,header=0)
#drop na rows

if (len(clustermap_panda.index) > 1):
    clustermap_panda.dropna(axis=0,how='any',inplace=True)
    my_clustermap=seaborn.clustermap(data=clustermap_panda,method='centroid',metric='euclidean',figsize=(20,20),col_cluster=False,)
    my_clustermap.savefig(output_heatmap_address)



else: 
    heatmap_panda=pandas.read_csv(input_panda_address,sep='¬',index_col=0,header=0)
    my_heatmap=seaborn.heatmap(data=heatmap_panda)
    my_heatmap.figure.savefig(output_heatmap_address,bbox_inches="tight")
