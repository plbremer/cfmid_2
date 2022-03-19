import subprocess
import os

#adduct_list=['[M-H]-','[M+H]+']
#instrument_list=['qtof','itft','hcd']
#cfmid_energy_list=['energy0','energy1','energy2']
#adduct_list=['[M-H]-','[M+H]+']
#instrument_list=['hcd']
adduct_list=['[M+H]+']
instrument_list=['qtof']

cfmid_energy_list=['energy0']

for adduct in adduct_list:
    for instrument in instrument_list:
        for cfmid_energy in cfmid_energy_list:
            #subprocess.call('/home/rictuar/coding_projects/fiehn_work/small_scripts/collision_energy_analysis_histo_energy_bins.py '+adduct+' '+instrument+' '+cfmid_energy, shell=True)
            os.system('python3 ./collision_energy_analysis_histo_energy_bins.py '+adduct+' '+instrument+' '+cfmid_energy)
