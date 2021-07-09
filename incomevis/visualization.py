
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation, rc
from mpl_toolkits.mplot3d.axes3d import Axes3D

import os.path
import matplotlib

from pylab import *
import matplotlib

from mpl_toolkits.mplot3d.axis3d import Axis


# Remove gridlines unneccessary
if not hasattr(Axis, "_get_coord_info_old"):
    def _get_coord_info_new(self, renderer):
        mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
        mins += deltas / 4
        maxs -= deltas / 4
        return mins, maxs, centers, deltas, tc, highs
    Axis._get_coord_info_old = Axis._get_coord_info  
    Axis._get_coord_info = _get_coord_info_new

# Axis configuration
def axis_config(ax, incomeType, segments):
    ax.view_init(5,-146)

    # z axis tick labels
    # RPPERHHINCOME
    if incomeType == 'RPPERHHINCOME':
        # Configure z axis
        ax.set_zlim(0, 300000) 
        ax.set_zticks([0,100000,200000,300000])
        ax.set_zticklabels([0,100000,200000,300000],fontsize=23, fontweight='bold')

        # Configure y axis
        ax.set_yticks([0,3,7,10])
        ax.set_yticklabels(['5p','35p','65p', '95p'],fontsize=23, fontweight = 'bold') 

    # HHINCOME
    elif incomeType == 'HHINCOME':
        # Configure z axis
        ax.set_zlim(0, 400000) 
        ax.set_zticks([0,100000,200000,300000,400000])
        ax.set_zticklabels([0,100000,200000,300000,400000],fontsize=23, fontweight='bold')

        # Configure y axis
        ax.set_yticks([0, 30, 60, 90])
        ax.set_yticklabels(['5p','35p','65p','95p'],fontsize=23, fontweight = 'bold')
    
    # z axis tick labels
    ax.tick_params(axis='z', which='major', pad=45)
    ax.zaxis.set_rotate_label(False)
    
    # x axis tick labels
    ax.set_xlim(-70000, 40000)
    ax.set_xticks([-60000,  -40000, -20000, 0, 20000, 40000])
    ax.set_xticklabels([-60000,  -40000, -20000, 0, 20000, 40000], fontsize=23, fontweight='bold')
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
    ax.set_xlabel('Distance from benchmark ($)', fontweight = 'bold', labelpad = 65, fontsize = 30)
    ax.set_ylabel('Percentile',  labelpad = 35, fontsize = 30, fontweight = 'bold')
    ax.set_zlabel('Adjusted annual household income ($)', rotation = 90, labelpad = 95, fontsize = 30, fontweight = 'bold')



# Currently availlable for RPPERHHINCOME and HHINCOME
def getAnimated_abs_rank(incomeType = 'RPPERHHINCOME', year_start = 1977, year_end = 2019, highlight = '',
                        input_path = '', 
                        benchmark_path = 'D:\\Github\\incomevis\\data\\absolute_ranking\\data_nation\\', 
                        new_sort=True, k='decile', sex=None, save=False):
    
    # Figure size
    fig = plt.figure(figsize=(20,17))
    ax = plt.axes(projection='3d')

    # Scalling
    x_scale, y_scale, z_scale = 3, 1, 1 
    scale = np.diag([x_scale, y_scale, z_scale, 1])
    scale = scale * (1.0/scale.max())
    scale[3, 3] = 0.7

    # Bounding box adjustment
    def short_proj(): return np.dot(Axes3D.get_proj(ax), scale)
    ax.get_proj = short_proj

    plt.subplots_adjust(left = -0.18, right = 1.03, bottom = -0.4, top = 2.2) 
    # plt.close()

    # distance direction, income direction, width, heigh
    cbax = fig.add_axes([.75,.55,.02,.2], alpha=0) 

    # Create colorbar
    all_num = [i for i in range(-60000, 40001)]
    all_num.reverse()
    cmap = plt.cm.bwr.reversed()
    norm = matplotlib.colors.TwoSlopeNorm(vmin=-60000, vmax=40001, vcenter=0)
    cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),cax=cbax, shrink = 0.15, ticks=[-60000,0,40000])
    cb.ax.set_yticklabels(['-60000' , '0 (50p benchmark)', '40000'], fontsize=22,weight='bold')
    # plt.close()

    def animate(year):
        ax.clear() # Clear the vis between each frame
        cb.ax.set_title(str(year), fontsize=40, fontweight='bold', pad=30)
        # Read the data
        pop_label = 'UR_NORMPOP_' + str(year+1)

        year_df = pd.read_csv(input_path + k + '_year_matplotlib_' + incomeType + str(year) + '.csv', index_col='State')

        if new_sort:
            nat = pd.read_csv(benchmark_path + 'nation' + '_' + k + '_' + incomeType + '_2019.csv')
            year_df['Location'] = year_df['50p'].values - nat['50p'].values
            year_df['Location'] = year_df['Location'].apply(np.int64)
            year_df['new_color'] = year_df.index.map(abs_color(incomeType=incomeType, k=k, gender=sex))

        if k == 'decile':
            # Decile
            segments = ['5p','15p','25p','35p','45p','50p','55p','65p','75p','85p','95p']

        if k == 'percentile':
            # Percentile
            segments = ['5p', '6p', '7p', '8p', '9p', '10p', '11p',
                        '12p', '13p', '14p', '15p', '16p', '17p', '18p', '19p', '20p',
                        '21p', '22p', '23p', '24p', '25p', '26p', '27p', '28p', '29p',
                        '30p', '31p', '32p', '33p', '34p', '35p', '36p', '37p', '38p',
                        '39p', '40p', '41p', '42p', '43p', '44p', '45p', '46p', '47p',
                        '48p', '49p', '50p', '51p', '52p', '53p', '54p', '55p', '56p',
                        '57p', '58p', '59p', '60p', '61p', '62p', '63p', '64p', '65p',
                        '66p', '67p', '68p', '69p', '70p', '71p', '72p', '73p', '74p',
                        '75p', '76p', '77p', '78p', '79p', '80p', '81p', '82p', '83p',
                        '84p', '85p', '86p', '87p', '88p', '89p', '90p', '91p', '92p',
                        '93p', '94p', '95p']

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
            
            # if save == True:
            # if sex == 'female':
            #     if highlight == '':
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile_gender/female_' + incomeType + '_' + str(year) + '.jpg', dpi=500)
            #     else:
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile_gender/female_' + incomeType + '_' + str(highlight) + '_' + str(year) + '.jpg', dpi=500)  
            # elif sex == 'male':
            #     if highlight == '':
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile_gender/male_' + incomeType + '_' + str(year) + '.jpg', dpi=500)
            #     else:
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile_gender/male_' + incomeType + '_' + str(highlight) + '_' + str(year) + '.jpg', dpi=500)  
            # else:    
            #     if highlight == '':
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile/' + incomeType + '_' + str(year) + '.jpg', dpi=500)
            #     else:
            #         ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_decile/' + incomeType + '_' + str(highlight) + '_' + str(year) + '.jpg', dpi=500)
    
                
        # if highlight == '':
        #     ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_percentile/' + incomeType + '_' + str(year) + '.jpg', dpi=500)
        # else:
        #     ax.figure.savefig('gdrive/My Drive/Colab Notebooks/incomevis/analysis/absolute_ranking/gallery_percentile/' + incomeType + '_' + str(highlight) + '_' + str(year) + '.jpg', dpi=500)
    # rc('axes',linewidth = 3)
    #Animation features: frames - max range for year in animate function; interval - time changing between each frame
    dynamic = animation.FuncAnimation(fig, animate, frames = [year for year in range(year_start - 1, year_end)], interval = 500)
    # rc('animation', html = 'jshtml')
    return dynamic

if __name__=="__main__":
    plot = getAnimated_abs_rank(incomeType='RPPERHHINCOME', year_start=1977, year_end=1978,
                                input_path='D:\\Github\\incomevis\\data\\bootstrap\\withreplacement\\bootstrap_age\\data\\')
    plot.save('D:\\Github\\incomevis\\gallery\\animation.gif', writer='imagemagick', fps=60)
    # print(abs_color(incomeType='RPPERHHINCOME', k='decile', gender=None))
    # plt.show()
    # print(plot)
    # plt.show()






# for testing purpose
# if __name__=="__main__":
#     color_abs = abs_visualization()
#     print(color_abs.color_RPPERHHINCOME())


