import matplotlib, matplotlib.pyplot as plt, pandas as pd, numpy as np

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

# Axis configuration
def axis_config(ax, incomeType, segments):
    ax.view_init(5,-146)

    # z axis tick labels
    # RPPERHHINCOME
    if incomeType == 'RPPERHHINCOME':
        # Configure z axis
        ax.set_zlim(0, 300000) 
        ax.set_zticks([0,100000,200000,300000])
        ax.set_zticklabels([0,100000,200000,300000],fontsize=15, fontweight='bold')

        # Configure y axis
        ax.set_yticks([0,3,7,10])
        ax.set_yticklabels(['5p','35p','65p', '95p'],fontsize=15, fontweight = 'bold') 

    # HHINCOME
    elif incomeType == 'HHINCOME':
        # Configure z axis
        ax.set_zlim(0, 400000) 
        ax.set_zticks([0,100000,200000,300000,400000])
        ax.set_zticklabels([0,100000,200000,300000,400000],fontsize=15, fontweight='bold')

        # Configure y axis
        ax.set_yticks([0, 30, 60, 90])
        ax.set_yticklabels(['5p','35p','65p','95p'],fontsize=15, fontweight = 'bold')
    
    # z axis tick labels
    ax.tick_params(axis='z', which='major', pad=30)
    ax.zaxis.set_rotate_label(False)
    
    # x axis tick labels
    ax.set_xlim(-70000, 40000)
    ax.set_xticks([-60000,  -40000, -20000, 0, 20000, 40000])
    ax.set_xticklabels([-60000,  -40000, -20000, 0, 20000, 40000], fontsize=15, fontweight='bold')
    ax.tick_params(axis='x', which='major', pad=15)

    # Gridlines option
    ax.xaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
    ax.yaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
    ax.zaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
    
    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    # y axis tick labels
    ax.set_ylim3d(0, len(segments)+1)

    # x y z main labels
    ax.set_xlabel('Distance from benchmark ($)', fontweight = 'bold', labelpad = 60, fontsize = 20)
    ax.set_ylabel('Percentile',  labelpad = 35, fontsize = 20, fontweight = 'bold')
    ax.set_zlabel('Adjusted annual household income ($)', rotation = 90, labelpad = 50, fontsize = 20, fontweight = 'bold')

def colorbar_config(fig, left=0.721, elevation=0.62, width=0.02, height=0.2, alpha = 0,
                    cm_str='bwr', upper = 40000, lower=-60000):
  """
    Custom color bar for incomevis

    Arguments
    =============================
      fig: matplotlib figure object

      left: adjust left (decrease) and right (increase);
            Default: 0.73
      
      elevation: adjust down (decrease) and up (increase);
            Default: 0.65
      
      width: width of the colorbar;
            Default: 0.02
      
      height: height of the colorbar;
            Default: 0.2

      alpha: blur the colorbar;
            Default: 0

      cm_str: string represents colorbar;
            Default bwr

      upper: upper bound difference;
            Default: 40000
      
      lower: lower bound difference;
            Default: -60000
  """
  cbax = fig.add_axes([left,elevation,width, height], alpha=alpha)
  all_num = [i for i in range(lower, upper)]
  all_num.reverse()
  cmap = plt.cm.get_cmap(cm_str).reversed()
  norm = matplotlib.colors.TwoSlopeNorm(vmin=-60000, vmax=40001, vcenter=0)
  cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbax, shrink = 0.15, ticks=[-60000,0,40000])
  cb.ax.set_yticklabels([str(lower) , '0 (50p benchmark)', str(upper)], fontsize=15, weight='bold') 
  return cb
