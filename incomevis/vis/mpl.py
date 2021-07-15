import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.axis3d import Axis

# Instantiate utils
from incomevis.utils import *
from incomevis.animation.animation_config import *

dir_name = ""
# Remove gridlines unneccessary
if not hasattr(Axis, "_get_coord_info_old"):
    def _get_coord_info_new(self, renderer):
        mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
        mins += deltas / 4
        maxs -= deltas / 4
        return mins, maxs, centers, deltas, tc, highs
    Axis._get_coord_info_old = Axis._get_coord_info  
    Axis._get_coord_info = _get_coord_info_new

# Currently availlable for RPPERHHINCOME and HHINCOME
def getAnimated_abs_rank(incomeType = 'RPPERHHINCOME', year_start = 1977, year_end = 2019, highlight = '', cm_str='bwr', 
                        input_path = '',  benchmark_path = 'D:\\Github\\incomevis\\data\\absolute_ranking\\data_nation\\', 
                        new_sort=True, k='decile', sex=None, save_frame=None, using_JN = False):
    
    # Figure size
    fig = plt.figure(figsize=(15,10))
    ax = plt.axes(projection='3d')

    # Scalling
    x_scale, y_scale, z_scale = 3, 1, 1.5
    scale = np.diag([x_scale, y_scale, z_scale, 1])
    scale = scale * (1.0/scale.max())
    scale[3, 3] = 0.7

    # Bounding box adjustment
    def short_proj(): return np.dot(Axes3D.get_proj(ax), scale)
    ax.get_proj = short_proj

    # plt.close()
    plt.subplots_adjust(left = 0, right = 0.95, bottom = -0.5, top = 1.8) 
    
    cb = colorbar_config(fig)

    def animate(year):
      ax.clear() # Clear the vis between each frame
      cb.ax.set_title(str(year), fontsize=30, fontweight='bold', pad=30)
      # Read the data
      pop_label = 'UR_NORMPOP_' + str(year+1)

      year_df = pd.read_csv(input_path + k + '_year_matplotlib_' + incomeType + str(year) + '.csv', index_col='State')

      if new_sort:
          nat = pd.read_csv(benchmark_path + 'nation' + '_' + k + '_' + incomeType + '_2019.csv')
          year_df['Location'] = year_df['50p'].values - nat['50p'].values
          year_df['Location'] = year_df['Location'].apply(np.int64)
          year_df['new_color'] = year_df.index.map(color_config(incomeType=incomeType, k=k, gender=sex))

      if k == 'decile': segments = getDecile('numeric')
      if k == 'percentile': segments = getPercentile('numeric')

      axis_config(ax, incomeType, segments)

      for state in range(year_df.index.size):
          for segment in range(len(segments)):
              if highlight != '':
                  for i in highlight:
                      if (year_df.iloc[state].name != i):
                          ax.bar3d(year_df['Location'][state], segment, 0,
                                  year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                                  year_df.loc[year_df.iloc[state].name, segments[segment]],
                                  color = '#00C2FB08')
                      else:
                          ax.bar3d(year_df['Location'][state], segment, 0,
                                  year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                                  year_df.loc[year_df.iloc[state].name, segments[segment]],
                                  color = year_df.loc[year_df.iloc[state].name, 'new_color'])
              else:
                  # RPPERHHINCOME
                  if incomeType == 'RPPERHHINCOME':
                      ax.bar3d(year_df['Location'][state], segment, 0,
                              year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                              year_df.loc[year_df.iloc[state].name, segments[segment]],
                              color = year_df.loc[year_df.iloc[state].name, 'new_color'])
                  # HHINCOME
                  elif incomeType == 'HHINCOME':
                      ax.bar3d(year_df['Location'][state], segment, 0,
                          year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                          year_df.loc[year_df.iloc[state].name, segments[segment]],
                          color = year_df.loc[year_df.iloc[state].name, 'new_color'], edgecolor='grey', linewidth=0.25)
          if save_frame != None:
            ax.figure.savefig(save_frame, dpi=500)
    
    #Animation features: frames - max range for year in animate function; interval - time changing between each frame
    dynamic = animation.FuncAnimation(fig, animate, frames = [year for year in range(year_start - 1, year_end)], interval = 500)
    if using_JN:
      rc('axes',linewidth = 3)
      rc('animation', html = 'jshtml')
    return dynamic

def getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, highlight = '', input_path = dir_name):

  # PyTest
  assert incomeType in ['RHHINCOME', 'RPPERHHINCOME', 'HHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME', 'ERHHINCOME']
  # Display setting
  fig = plt.figure(figsize=(20,17), tight_layout=True)
  ax = plt.axes(projection='3d')
  x_scale = 3 # Scalling
  y_scale = 1
  z_scale = 1
  scale = np.diag([x_scale, y_scale, z_scale, 1])
  scale = scale*(1.0/scale.max())
  scale[3, 3] = 0.7
  def short_proj(): return np.dot(Axes3D.get_proj(ax), scale)
  ax.get_proj = short_proj
  plt.subplots_adjust(left = -0.35, right = 1, bottom = -0.5, top = 2.45) # Bounding box adjustment
  plt.close()

  def animate(year):
    #Read the data
    pop_label = 'UR_NORMPOP_' + str(year+1)
    year_df = pd.read_csv(input_path + 'decile_year_matplotlib_' + incomeType + str(year) + '.csv', index_col='State')
    ax.view_init(5,-140)
    #Convert the data to suitable format for the 3D bar chart
    deciles = ['5p','15p','25p','35p','45p','50p','55p','65p','75p','85p','95p']
    label = year_df['Label'].tolist()
    for j in range(len(label)):
      if isinstance(label[j], float): label[j] = ''
      # if year_df.index[j] == 'California': label[j] = 'CA'
      # if year_df.index[j] == 'District of Columbia': label[j] = 'DC'

    ax.clear() #Clear the vis between each frame
    ax.set_zlim(0, 400000) #Set the limit of the z axis
    ax.set_zticklabels([0,50000,100000,150000,200000,250000,300000,350000,400000],fontsize=15)
    #Resize and label the x axis
    ax.set_xticks([j for j in range(len(year_df[pop_label].tolist()))])
    ax.set_xticklabels(label, rotation=-45, fontsize='x-large')
    ax.grid(False)
    #Adjust label in z axis
    ax.tick_params(axis='z', which='major', pad=30)
    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    #Resize and label the y axis
    ax.set_yticks(np.arange(len(deciles)))
    ax.set_yticklabels(['' for year in range(len(deciles))])
    ax.zaxis.set_rotate_label(False)  
    ax.set_zlabel('Annual Household Income (2018$)', rotation = 90, labelpad = 60, fontsize = 20, fontweight = 'bold')
    ax.set_xlabel('Poorer States                             ' + str(year) + '                             Richer States',
                  fontweight = 'bold', labelpad = 30, fontsize = 20)

    #Draw the 3D bar chart 11
    for state in range(year_df.index.size):
      for decile in range(len(deciles)):
        if (highlight != ''):
          if (year_df.iloc[state].name != highlight):
            ax.bar3d(state, decile, 0,
                    year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                    year_df.loc[year_df.iloc[state].name, deciles[decile]],
                    color = '#00C2FB08')
          else:
            ax.bar3d(state, decile, 0,
                    year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                    year_df.loc[year_df.iloc[state].name, deciles[decile]],
                    color = year_df.loc[year_df.iloc[state].name, 'Color'])
        else:
          ax.bar3d(state, decile, 0,
                  year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                  year_df.loc[year_df.iloc[state].name, deciles[decile]],
                  color = year_df.loc[year_df.iloc[state].name, 'Color'])

  #Animation features: frames - max range for year in animate function; interval - time changing between each frame
  dynamic = animation.FuncAnimation(fig, animate, frames = [year for year in range(year_start - 1, year_end)], interval = 500)
  rc('animation', html = 'jshtml')
  return dynamic