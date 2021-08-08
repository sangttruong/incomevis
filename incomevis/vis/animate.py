#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import numpy as np, matplotlib.pyplot as plt
from matplotlib import animation, rc
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.axis3d import Axis

# Owned
from incomevis.utils import *
from incomevis.vis.mpl_colorbar import *
from incomevis.vis.mpl_axes import axes_config
from incomevis.vis.mlp_simple import *
from incomevis.vis.mlp_complex import *
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

# Remove gridlines unneccessary
if not hasattr(Axis, "_get_coord_info_old"):
  def _get_coord_info_new(self, renderer):
      mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
      mins += deltas / 4
      maxs -= deltas / 4
      return mins, maxs, centers, deltas, tc, highs
  Axis._get_coord_info_old = Axis._get_coord_info
  Axis._get_coord_info = _get_coord_info_new

def animate(incomeType = 'RPPERHHINCOME',
            year_start = 1977, year_end = 2020,
            highlight = '',
            benchmark = True,
            input_path = SOURCE_DATA_PATH,
            k = 'decile', group = 'all',
            benchmark_dir = BENCHMARK_DATA_PATH):
  """
  Animate economic distribution over year.

  Parameters
  ----------
  incomeType : str
    Income type.
    Default value is RPPERHHINCOME.
    Typically HHINCOME, RHHINCOME, ERHHINCOME, RPPERHHINCOME.
  
  year_start : int
    Starting data year.
    Default value is 1977.
  
  year_end : int
    Ending data year.
    Default value is 2020.
    Unlike pandas index convention, the ending data year will be
    included in render.
  
  highlight : str
    State to highlight
  
  k : str
    decile or percentile.
  
  group : str
    Demographic groups.
    Typically male, female, black
  
  benchmark_dir: str
    Benchmark directory
  """

  # Figure size
  fig = plt.figure(figsize=(20,17))

  # Scalling
  x_scale, y_scale, z_scale = 3, 1, 1.5
  scale = np.diag([x_scale, y_scale, z_scale, 1])
  scale = scale * (1.0/scale.max())
  scale[3, 3] = 0.7

  # Bounding box adjustment
  ax = plt.axes(projection='3d')
  def short_proj(): return np.dot(Axes3D.get_proj(ax), scale)
  ax.get_proj = short_proj
  rc('axes',linewidth = 3)

  if benchmark:
    # animate function need to have precisely a single input
    def animate(year): return complex_animate(year, ax = ax, k = k, cb = colorbar_config(fig),
                                              benchmark = benchmark,
                                              input_path = input_path, benchmark_dir = benchmark_dir,
                                              incomeType = incomeType, group = group, highlight = highlight,
                                              year_end = year_end)
  else:
    def animate(year): return simple_animate(year, ax = ax, k = k, cb = colorbar_config(fig),
                                              benchmark = benchmark,
                                              input_path = input_path, benchmark_dir = benchmark_dir,
                                              incomeType = incomeType, group = group, highlight = highlight,
                                              year_end = year_end)

  dynamic = animation.FuncAnimation(fig, animate,
                                    frames = [year for year in range(year_start - 1, year_end)],
                                    interval = 500)
  rc('animation', html = 'jshtml')
  return dynamic
