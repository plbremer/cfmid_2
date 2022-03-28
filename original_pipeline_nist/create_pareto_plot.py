import pandas
import matplotlib.pyplot as plt
import plotly.graph_objects
import plotly.express


############################EDITED FOR SNAKEMAKE#######################################
feature='bins'
############################EDITED FOR SNAKEMAKE#######################################
ranking_panda_address=snakemake.input.ranking_panda_address
feature=snakemake.params.feature
pareto_output_address=snakemake.output.pareto_output_address
############################EDITED FOR SNAKEMAKE#######################################
ranking_panda=pandas.read_csv(ranking_panda_address,sep='¬',header=0)



my_pareto=plotly.graph_objects.Figure(data=[plotly.graph_objects.Histogram(x=ranking_panda[feature],cumulative_enabled=True,nbinsx=26)])


my_pareto.write_html(pareto_output_address)

