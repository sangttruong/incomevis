#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import pandas as pd, numpy as np
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

def complex_animate(year, ax, k, cb, benchmark, input_path, benchmark_dir,
                    incomeType, group, highlight, year_end):
  """
    Helper function for animating complex income distribution (i.e. with benchmark). 
    Documentation coming soon.
  """

  # Axes and colorbar configuration
  axes_config(ax, type = 'benchmark', k = k)
  cb.ax.set_title(str(year), fontsize=40, fontweight='bold', pad=30)

  # Data import and calibrate with benchmark if needed
  pop_label = 'UR_NORMPOP_' + str(year+1)
  year_df = pd.read_csv(input_path + k + '_' + group + '_year_matplotlib_'
                    + incomeType + str(year) + '.csv', index_col='State')
  if benchmark:
      nat = pd.read_csv(benchmark_dir + k + '_' + group + '_year_matplotlib_'
                      + incomeType + str(year_end-1) + '.csv')
      year_df['Location'] = year_df['50p'].values - nat['50p'].values
      year_df['Location'] = year_df['Location'].apply(np.int64)
      year_df['new_color'] = year_df.index.map(getColor(str(incomeType)))
      # TODO: getColor() needs to have 'group' as an argument

  # Axes and colorbar configuration
  axes_config(ax, type = 'benchmark', k = k)
  cb.ax.set_title(str(year), fontsize=40, fontweight='bold', pad=30)
  if not benchmark:
    label = year_df['Label'].tolist()
    ax.set_xticklabels(label, rotation=-45, fontsize='x-large')

  kiles = getDecile('string') if k == 'decile' else getPercentile('string')
  label = year_df['Label'].tolist()

  for j in range(len(label)):
    if isinstance(label[j], float): label[j] = ''

  for state in range(year_df.index.size):
    for kile in range(len(kiles)):
      if highlight != '':
        for i in highlight:
          if (year_df.iloc[state].name != i):
            ax.bar3d(year_df['Location'][state], kile, 0,
                    year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                    year_df.loc[year_df.iloc[state].name, kiles[kile]],
                    color = '#00C2FB08')
      ax.bar3d(year_df['Location'][state], kile, 0,
              year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
              year_df.loc[year_df.iloc[state].name, kiles[kile]],
              color = year_df.loc[year_df.iloc[state].name, 'new_color'])