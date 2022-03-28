#this takes the nist20 only file and outputs the six cohorts that we deemed important
import pandas

#######################modified for snakemake##############################
overall_input_file_address=snakemake.input.overall_input_file_address
one_cohort_output_csv_address=snakemake.output.one_cohort_output_csv_address
adduct=snakemake.params.adduct
instrument=snakemake.params.instrument
precursor_status=snakemake.params.precursor_status
separator='¬'
#######################modified for snakemake##############################

instrument_type_in_file='null'
if instrument=='qtof':
    instrument_type_in_file='Q-TOF'
elif instrument=='hcd':
    instrument_type_in_file='HCD'
elif instrument=='itft':
    instrument_type_in_file='IT-FT/ion trap with FTMS'


overall_input_file=open(overall_input_file_address,'r')
one_cohort_output_csv_file=open(one_cohort_output_csv_address,'w')

line_counter=0

for line in overall_input_file:
    one_line_list=line.split(separator)

    if (line_counter==0):
        one_cohort_output_csv_file.write(line)
    line_counter+=1

    #10 is the index of Instrument_type
    if (one_line_list[10]==instrument_type_in_file) and (one_line_list[20]==adduct):
        one_cohort_output_csv_file.write(line)


overall_input_file.close()
one_cohort_output_csv_file.close()
