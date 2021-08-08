#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import matplotlib.pyplot as plt, matplotlib

# Owned
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def colorbar_config(fig, left=0.721, elevation=0.62, width=0.02, height=0.2, alpha = 0,
                    cm_str='bwr', upper = 40000, lower=-60000):
  """
    Custom color bar for incomevis

    Arguments
    =============================
      fig: ``matplotlib figure`` object

      left: int
            adjust left (decrease) and right (increase). Default: 0.73

      elevation: int
            adjust down (decrease) and up (increase). Default: 0.65

      width: int
            width of the colorbar. Default: 0.02

      height: int
            height of the colorbar. Default: 0.2

      alpha: int
            blur the colorbar. Default: 0

      cm_str: str
            string represents colorbar. Default ``'bwr'``.

      upper: int
            upper bound difference. Default: 40000

      lower: int
            lower bound difference. Default: -60000
  """
  cbax = fig.add_axes([left,elevation,width, height], alpha=alpha)
  all_num = [i for i in range(lower, upper)]
  all_num.reverse()
  cmap = plt.cm.get_cmap(cm_str).reversed()
  norm = matplotlib.colors.TwoSlopeNorm(vmin=-60000, vmax=40001, vcenter=0)
  cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbax, shrink = 0.15, ticks=[-60000,0,40000])
  cb.ax.set_yticklabels([str(lower) , '0 (50p benchmark)', str(upper)], fontsize=15, weight='bold')
  return cb
