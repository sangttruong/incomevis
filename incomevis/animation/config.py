import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

# Color configuration
def color_config(incomeType = 'RPPERHHINCOME', k = 'decile', cm_str='bwr', reversed_cm = True,
                input_path = 'D:\\Github\\incomevis\\data\\bootstrap\\withreplacement\\bootstrap_age\\data\\', 
                benchmark_path = 'D:\\Github\\incomevis\\data\\absolute_ranking\\data_nation\\', gender=None):
    """
    Gather color gradient based on the given benchmark (nation)
    Arguments
    =================================================================
        incomeType (str): Type of income. (RPPERHHINCOME and HHINCOME)
                            Default RPPERHHINCOME
        
        k (str): Chossing between decile or percentile
                    Deault decile
        input_path (str): Input directory
        benchmark_path (str): Benchmark directory 
        gender (str): Choosing between male or female
                        Deault None
    """
    
    # Color map for entire benchmark
    color_map = {}
    all_num = [i for i in range(-60000, 40001)]
    all_num.reverse()
    
    if reversed_cm == True: cmap = plt.cm.get_cmap(cm_str).reversed()
    else: cmap = plt.cm.get_cmap(cm_str)
    norm = matplotlib.colors.TwoSlopeNorm(vmin=-60000, vmax=40001, vcenter=0)

    color = cmap(norm(all_num))
    hex_color = [matplotlib.colors.rgb2hex(i) for i in color]
    for i in range(len(all_num)): color_map[all_num[i]] = hex_color[i]

    # Get color for decile RPPERHHINCOME
    year_df = ''
    if gender == None: year_df = pd.read_csv(input_path + k + '_year_matplotlib_' + incomeType + '1976.csv', index_col='State')
    else: year_df = pd.read_csv(input_path + gender + '_' + k + ' _year_matplotlib_' + incomeType + '1976.csv', index_col='State')

    nat = pd.read_csv(benchmark_path + 'nation_decile_' + incomeType + '_2019.csv')
    year_df['Location'] = year_df['50p'].values - nat['50p'].values
    year_df['Location'] = year_df['Location'].apply(np.int64)
    state_map = []
    for i in range(len(year_df)): state_map.append(color_map[year_df['Location'][i]])
    year_df['new_color'] = state_map
    new_color_map = year_df['new_color'].to_dict()
    return new_color_map