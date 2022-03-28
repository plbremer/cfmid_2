import pandas
import matplotlib.pyplot
import numpy
#import plotly.graph_objects
#import plotly.express
from matplotlib import cm


############################EDITED FOR SNAKEMAKE#######################################
#MAX_RANK_CREATED=24
feature='bins'
#the "cfmid actually fragmented" panda location
#cfmid_fragmented_output_address='/home/rictuar/coding_projects/fiehn_work/text_files/_cfmid_compared_to_experimental/qtof_top_25_dot_product_comparison_neg_mode_energy_added_cfmid_fragmented.txt'
#cfmid_fragmented_panda=pandas.read_csv(cfmid_fragmented_output_address,sep='¬',header=0)
#the address of 
#ranking_panda_address='/home/rictuar/coding_projects/fiehn_work/text_files/orthogonal_snakemake/[M-H]-/qtof/precursor_yes/energy_comparison_column_added_nist20_only_qtof_only_[M-H]-.txt'
#ranking_panda=pandas.read_csv(ranking_panda_address,sep='¬',header=0)
##print(ranking_panda)
#pareto_output_address='/home/rictuar/coding_projects/fiehn_work/text_files/orthogonal_snakemake/[M-H]-/qtof/precursor_yes/output_files/pareto_plot_[M-H]-_qtof_precursor_yes.html'
############################EDITED FOR SNAKEMAKE#######################################
#ranking_panda_address=snakemake.input.ranking_panda_address
#feature=snakemake.params.feature
#pareto_output_address=snakemake.output.pareto_output_address
############################EDITED FOR SNAKEMAKE#######################################
#ranking_panda=pandas.read_csv(ranking_panda_address,sep='¬',header=0)

feature='bins'
pareto_output_address='../../../results/final_figures/pareto_plot'
label_each_x=False


adduct_list=['[M+H]+','[M-H]-']
#instrument_list=['qtof','itft','hcd']
instrument_list=['hcd','itft','qtof']

list_of_bin_columns=list()
list_of_labels=list()

#color_list=

for instrument in instrument_list:
    for adduct in adduct_list:

        print(adduct+' '+instrument)
        ranking_panda_address='../../../results/'+adduct+'/'+instrument+'/precursor_no/cfmid-collision_'+adduct+'_'+instrument+'_precursor_no.txt'
        ranking_panda=pandas.read_csv(ranking_panda_address,sep='¬',header=0)
        #list_of_bin_columns.append(ranking_panda['bins'].to_list())
        list_of_bin_columns.insert(0,ranking_panda['bins'].to_list())
        #if
            
#list_of_labels.append(adduct+' '+instrument)
list_of_labels=[
    '[M+H]+ HCD-Orbitrap',
    '[M-H]-    HCD-Orbitrap',
    '[M+H]+ CID-Orbitrap',
    '[M-H]-    CID-Orbitrap',
    '[M+H]+ CID-Q-TOF',
    '[M-H]-    CID-Q-TOF']


#flip the order to avoid prepending
#list_of_labels=list_of_labels.reverse()
#list_of_labels.reverse()

#note avenir does not exist
matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.pyplot.rcParams['font.size'] = 18
matplotlib.pyplot.rcParams['axes.linewidth'] = 2
#specify figure size if desired


#my_figure = matplotlib.pyplot.figure(figsize=(3.34646, 4))
my_figure = matplotlib.pyplot.figure(figsize=(6.69292, 8))

#create custom axes. these are needed to do many things.
#my_axes=my_figure.add_axes([0,0,1,1])
#choose color scheme if desired
#
#
#specify axes labels
matplotlib.pyplot.xlabel('Dot Product')
matplotlib.pyplot.ylabel('Percentage of Spectra')
#specify title
#
#specify legen appears
#

#paired_colors=cm.get_cmap('Set1',6)
#named_colors=['red','indianred','green','palegreen','blue','cornflowerblue']
named_colors=['indianred','red','palegreen','green','cornflowerblue','blue']
n,bins,patches=matplotlib.pyplot.hist(
    x=list_of_bin_columns,
    bins=20,density=True,
    cumulative=True,
    #cumulative=False,
    histtype='step',
    label=list_of_labels,
    linewidth=3,
    color=named_colors
)
#remove the rightmost bar
patches[0][0].set_xy(patches[0][0].get_xy()[1:-1])
patches[1][0].set_xy(patches[1][0].get_xy()[1:-1])
patches[2][0].set_xy(patches[2][0].get_xy()[1:-1])
patches[3][0].set_xy(patches[3][0].get_xy()[1:-1])
patches[4][0].set_xy(patches[4][0].get_xy()[1:-1])
patches[5][0].set_xy(patches[5][0].get_xy()[1:-1])
#get current axes
my_axes=matplotlib.pyplot.gca()
print(my_axes)
#my_xticks=my_axes.xticks
#print(my_xticks)
#matplotlib.pyplot.xticks
#custom labels, ticks
#get current location and labels
#current_locations,current_labels=get_xticks()
#x_plot_labels=['≥950','≥750','≥500','≥250','≥0']
if (label_each_x==True):
    x_plot_labels_numbers=numpy.arange(950,-50,-50)
    print(x_plot_labels_numbers)
    #x_plot_labels_words=['≥' for x in range(0,20)]
    x_plot_labels=list()
    for i in range(0,20):
        x_plot_labels.append('≥'+str(x_plot_labels_numbers[i]))
    #matplotlib.pyplot.xticks(labels=plot_labels)
    my_axes.set_xticks(numpy.arange(0,19,0.95))
else:
    x_plot_labels_numbers=numpy.arange(900,-50,-100)
    print(x_plot_labels_numbers)
    #x_plot_labels_words=['≥' for x in range(0,20)]
    x_plot_labels=list()
    for i in range(0,10):
        x_plot_labels.append(str(x_plot_labels_numbers[i]))
    #matplotlib.pyplot.xticks(labels=plot_labels)
    my_axes.set_xticks(numpy.arange(1+(0.95/2),20,2*.95))



my_axes.set_xticklabels(x_plot_labels,rotation=-90)
#my_axes.set_xticklabels(x_plot_labels)

y_plot_labels=['0%','20%','40%','60%','80%','100%']
#matplotlib.pyplot.xticks(labels=plot_labels)
my_axes.set_yticklabels(y_plot_labels)
#my_axes.set_yxticklabels(y_plot_labels)

#legend
matplotlib.pyplot.legend(list_of_labels,loc='upper left')

#matplotlib.pyplot.figure(figsize=(3.34646,))
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig(pareto_output_address+'_cumulative.eps')
matplotlib.pyplot.savefig(pareto_output_address+'_cumulative.png')


matplotlib.pyplot.show()






#temporarily delete the energy1 and energy2
#ranking_panda.drop(labels=['energy1_match_rank','energy1_match_score','energy2_match_rank','energy2_match_score'],axis=1,inplace=True)
#print(ranking_panda)

#fragmented_boolean_mask=cfmid_fragmented_panda['cfmid_fragmented']
#print(fragmented_boolean_mask)

#remove the didnt-fragment rows from the ranking panda
#ranking_panda=ranking_panda[fragmented_boolean_mask]
#print(ranking_panda)

'''
#in this portion we fill a list with 0 to 25, inclusive, getting the values from the ranking panda.
#its just a weay to get the fucking thing done
ranks=ranking_panda['ranking'].value_counts()
print(ranks)
rank_count=list()
for i in range(0,25):
    if(i in ranks.keys()):
        rank_count.append(ranks[i])
    else:
        rank_count.append(0)
#append those who didnt get ranked
rank_count.append(ranks[50])
#plotly seems to fucking insist on pandas
temp_dict={'rankings':rank_count}
rank_count_panda=pandas.DataFrame.from_dict(temp_dict)
print(rank_count_panda)
'''

#convert the 50 to 25s (so stupid)
#def convert_50_to_25(temp_panda):
#    temp_panda.loc[temp_panda['ranking']==50,'ranking']=25
#    print(temp_panda)
    #temp_panda[]

#convert_50_to_25(ranking_panda)
#print(ranking_panda)
#giveen a particular rank, returns a list of indexes for which that rank is 
#the rank seen
#def return_rows_associated_with_rank(temp_panda,rank):
#    s
#my_pareto=seaborn.distplot(a=rank_count,x='rank',cumulative=True)
#my_pareto=plotly.graph_objects.Figure(data=[plotly.graph_objects.Histogram(x=ranking_panda[feature],cumulative_enabled=True,nbinsx=26)])
#matplotlib.pyplot.show()
#my_pareto=plotly.graph_objects.Histogram(x=rank_count)

#my_pareto.show()

#matplotlib.pyplot.scatter(x=range(0,26),)

#my_pareto.write_html(pareto_output_address)



'''
def pareto_plot(df, x=None, y=None, title=None, show_pct_y=False, pct_format='{0:.0%}'):
    xlabel = x
    ylabel = y
    tmp = df.sort_values(y, ascending=False)
    x = tmp[x].values
    y = tmp[y].values
    weights = y / y.sum()
    cumsum = weights.cumsum()
    
    fig, ax1 = plt.subplots()
    ax1.bar(x, y)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    ax2 = ax1.twinx()
    ax2.plot(x, cumsum, '-ro', alpha=0.5)
    ax2.set_ylabel('', color='r')
    ax2.tick_params('y', colors='r')
    
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    # hide y-labels on right side
    if not show_pct_y:
        ax2.set_yticks([])
    
    formatted_weights = [pct_format.format(x) for x in cumsum]
    for i, txt in enumerate(formatted_weights):
        ax2.annotate(txt, (x[i], cumsum[i]), fontweight='heavy')    
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    plt.show()
print(rank_count_panda)
pareto_plot(rank_count_panda,x=rank_count_panda.keys(),y=rank_count_panda)
'''