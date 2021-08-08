#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import pandas as pd
from pylab import *

# Owned
from incomevis.utils import *
from incomevis.vis.mpl_colorbar import *
from incomevis.vis.mpl_axes import axes_config
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def simple_animate(year, ax, k, cb, benchmark, input_path, benchmark_path,
                    incomeType, group, highlight, year_end):
  """
    Helper function for animating simple income distribution (i.e. without benchmark). 
    Documentation coming soon.
  """
  
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
