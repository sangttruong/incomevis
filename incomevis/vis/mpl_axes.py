from incomevis.utils.getDecile import getDecile
import numpy as np
from incomevis.utils import *

def axes_config(ax, type, k):
    """
        Configurate axes for 3D visualization in matplotlib

        Arguments
        =============================
        ax: matplotlib 3D axes
        type: benchmark or simple
        k: decile or percentile
    """
    ax.clear()
    ax.view_init(5,-146)
    kiles = getDecile('string') if k == 'decile' else getPercentile('string')

    # Remove fill and set background to white
    ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    # z axis tick labels
    ax.set_zlim(0, 400000)
    ax.set_zticks([0,100000,200000,300000,400000])
    ax.set_zticklabels([0,100000,200000,300000,400000],fontsize=23, fontweight='bold')
    ax.tick_params(axis='z', which='major', pad=45)
    ax.zaxis.set_rotate_label(False)

    # Gridlines
    ax.xaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
    ax.yaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
    ax.zaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})

    if type == 'benchmark':
        # y axis tick labels
        if k == 'decile': ax.set_yticks([0,3,7,10])
        else: ax.set_yticks([0, 30, 60, 90])
        ax.set_ylim3d(0, len(kiles)+1)
        ax.set_yticklabels(['5p','35p','65p', '95p'],fontsize=23, fontweight = 'bold')

        # x axis tick labels
        ax.set_xlim(-70000, 40000)
        ax.set_xticks([-60000,  -40000, -20000, 0, 20000, 40000])
        ax.set_xticklabels([-60000,  -40000, -20000, 0, 20000, 40000], fontsize=23, fontweight='bold')
        ax.tick_params(axis='x', which='major', pad=15)

        # x y z main labels
        ax.set_xlabel('Distance from benchmark ($)', fontweight = 'bold', labelpad = 65, fontsize = 30)
        ax.set_ylabel('Percentile',  labelpad = 35, fontsize = 30, fontweight = 'bold')
        ax.set_zlabel('Adjusted annual household income ($)', rotation = 90, labelpad = 95, fontsize = 30, fontweight = 'bold')

    elif type == 'simple':
        ax.set_yticklabels(['' for year in range(len(getDecile('string')))])
        ax.set_xticks([j for j in range(len(getStateName('numeric')))])

        # #Resize and label the x axis
        # ax.grid(False)

        #Adjust label in z axis
        ax.tick_params(axis='z', which='major', pad=30)

        # Resize and label the y axis
        deciles = getDecile('string')
        ax.set_yticks(np.arange(len(deciles)))
        ax.zaxis.set_rotate_label(False)
        
        # x y z main labels
        ax.set_zlabel('Annual Household Income (2018$)', rotation = 90, labelpad = 60, fontsize = 20, fontweight = 'bold')
        ax.set_xlabel('Poorer States                                                          Richer States',
                fontweight = 'bold', labelpad = 30, fontsize = 20)
    else: raise RuntimeError


# def optimized_axis_config(ax, axes_config):
#     ax.view_init(5,-146)
#     # parsing arguments:
#     for axis in axes_config.key:
#         axes_config[axis][0](config_dict[axis][0][0], config_dict[axis][0][1])
#         ax.set_zticks(zticks)
#         ax.set_zticklabels(ztickslabel,fontsize=15, fontweight='bold')
#         ax.set_zlabel(zlabel, fontweight = 'bold', labelpad = zlabelpad, fontsize = 20, rotation = 90)
#         ax.tick_params(axis = 'z', which = 'major', pad = zpad)
#         axes_dict[axis][4].xaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
#         axes_dict[axis][4].xaxis.pane.fill = False # remove fill
#         axes_dict[axis][4].xaxis.pane.set_edgecolor('w') # set color to white
