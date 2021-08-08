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
            k = 'decile', group = 'all',
            year_start = 1977, year_end = 2020, highlight = '',
            benchmark = True, benchmark_path = BENCHMARK_DATA_PATH,
            input_path = DEFLATED_DATA_PATH,):
  """
  Animate economic distribution over year.

  Parameters
  ----------
  incomeType: str
    Type of household income. Currently supported ``'HHINCOME'``, ``'RHHINCOME'``, 
    ``'ERHHINCOME'``, and ``'RPPERHHINCOME'``. Default: ``'RPPERHHINCOME'``, i.e.
    fully deflated.

  k: str
    Method of partitioning income, which is either ``'decile'`` or ``'percentile'``. 
    Default: ``'decile'``.

  year_start: int
    Starting year of data that will be printed out. Default: 1977, i.e. the earliest
    year household income was meaningfully documented by IPUMS. 
      
  year_end: int
    Ending year of data that will be printed out. Unlike pandas index convention, 
    the ending data year will be included in render. Default: 2020.
  
  highlight : str
    State to highlight. Default: empty string.
  
  group: str
    Allowing to export (sub)population of data. Currently supported ``'all'``,
    ``'male'``, ``'female'``, ``'black'``, ``'non-black'``, ``'hispan'``, 
    ``'non-hispan'``, ``'high-educ'``, ``'low-educ'``. Default: ``'all'``. 

  benchmark: bool
    Whether the exporting data is the benchmark data. If ``benchmark = True``, the
    default benchmark data is the national income (with respect to the selected 
    income type) at ``'year_end'``. Default: False.
  
  benchmark_path: str
    Benchmark directory. Default: ``BENCHMARK_DATA_PATH``.

  input_path: str
    Path to data to animate. Default: ``DEFLATED_DATA_PATH``
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
                                              input_path = input_path, benchmark_path = benchmark_path,
                                              incomeType = incomeType, group = group, highlight = highlight,
                                              year_end = year_end)
  else:
    def animate(year): return simple_animate(year, ax = ax, k = k, cb = colorbar_config(fig),
                                              benchmark = benchmark,
                                              input_path = input_path, benchmark_path = benchmark_path,
                                              incomeType = incomeType, group = group, highlight = highlight,
                                              year_end = year_end)

  dynamic = animation.FuncAnimation(fig, animate,
                                    frames = [year for year in range(year_start - 1, year_end)],
                                    interval = 500)
  rc('animation', html = 'jshtml')
  return dynamic
