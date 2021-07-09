import matplotlib
import matplotlib.pyplot as plt

import pandas as pd

# Color configuration
def abs_color(incomeType = 'RPPERHHINCOME', k = 'decile',
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

    cmap = plt.cm.bwr.reversed()
    norm = matplotlib.colors.TwoSlopeNorm(vmin=-55000, vmax=30000, vcenter=0)

    color = cmap(norm(all_num))
    hex_color = [matplotlib.colors.rgb2hex(i) for i in color]
    for i in range(len(all_num)):
        color_map[all_num[i]] = hex_color[i]

    # Get color for decile RPPERHHINCOME
    year_df = ''
    if gender == None:
        year_df = pd.read_csv(input_path + k + '_year_matplotlib_' + incomeType + '1976.csv', index_col='State')
    else:
        year_df = pd.read_csv(input_path + gender + '_' + k + ' _year_matplotlib_' + incomeType + '1976.csv', index_col='State')

    nat = pd.read_csv(benchmark_path + 'nation_decile_' + incomeType + '_2019.csv')
    year_df['Location'] = year_df['50p'].values - nat['50p'].values
    year_df['Location'] = year_df['Location'].apply(np.int64)
    new_color = []
    for i in range(len(year_df)):
        new_color.append(color_map[year_df['Location'][i]])
    year_df['new_color'] = new_color
    return year_df['new_color'].to_dict()