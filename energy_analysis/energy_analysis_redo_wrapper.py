import os


# bin_count=200
# adduct='[M-H]-'
# instrument='hcd'
# #instrument_brand='Orbitrap Fusion Lumos'
# instrument_brand='Thermo Finnigan Elite Orbitrap'
# use_entries_with_eV=True
# put_eV_on_x_axis=True


# bin_count=int(sys.argv[1])
# adduct=sys.argv[2]
# instrument=sys.argv[3]
# #instrument_brand='Orbitrap Fusion Lumos'
# instrument_brand=sys.argv[4]
# use_entries_with_eV=bool(sys.argv[5])
# put_eV_on_x_axis=bool(sys.argv[6])

# bin_count_list=['200']
# adduct_list=['[M+H]+','[M-H]-','both']
# instrument_list=['hcd']
# instrument_brand_list=['Thermo_Finnigan_Elite_Orbitrap','Orbitrap_Fusion_Lumos','both']
# use_entries_with_eV_list=[0,1]
# put_eV_on_x_axis_list=[0,1]

bin_count_list=['44']
adduct_list=['M+H+']
instrument_list=['qtof']
instrument_brand_list=['both']
use_entries_with_eV_list=[1]
put_eV_on_x_axis_list=[0]


for bin_count in bin_count_list:
    for adduct in adduct_list:
        for instrument in instrument_list:
            for instrument_brand in instrument_brand_list:
                for use_entries_with_eV in use_entries_with_eV_list:
                    for put_eV_on_x_axis in put_eV_on_x_axis_list:
                        print(f'python3 ./energy_analysis_redo.py {bin_count} {adduct} {instrument} {instrument_brand} {use_entries_with_eV} {put_eV_on_x_axis}')
                        os.system(
                            f'python3 ./energy_analysis_redo.py {bin_count} {adduct} {instrument} {instrument_brand} {use_entries_with_eV} {put_eV_on_x_axis}'
                        )