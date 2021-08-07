import pandas as pd
from pylab import *

from incomevis.utils import *
from incomevis.vis.mpl_colorbar import *
from incomevis.vis.mpl_axes import axes_config

def simple_animate(year, ax, k, cb, benchmark, input_path, benchmark_dir,
                    incomeType, group, highlight, year_end):
  
  # Data import and calibrate with benchmark if needed
  year_df = pd.read_csv(input_path + k + '_' + group + '_year_matplotlib_' 
                        + incomeType + str(year) + '.csv', index_col='State')
  
  # Axes and colorbar configuration
  label = year_df['Label'].tolist()
  axes_config(ax, type = 'simple', k = 'simple')
  ax.set_xticklabels(label, rotation=-45, fontsize='x-large')
  deciles = getDecile('string')

  for j in range(len(label)):
    if isinstance(label[j], float): label[j] = ''
    # if year_df.index[j] == 'California': label[j] = 'CA'
    # if year_df.index[j] == 'District of Columbia': label[j] = 'DC'
  pop_label = 'UR_NORMPOP_' + str(year+1)

  #Draw the 3D bar chart 11
  for state in range(year_df.index.size):
    for decile in range(len(deciles)):
      if (highlight != '' and year_df.iloc[state].name != highlight):
        ax.bar3d(state, decile, 0,
                year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                year_df.loc[year_df.iloc[state].name, deciles[decile]],
                color = '#00C2FB08')
      ax.bar3d(state, decile, 0,
              year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
              year_df.loc[year_df.iloc[state].name, deciles[decile]],
              color = year_df.loc[year_df.iloc[state].name, 'Color'])
