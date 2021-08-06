def axes_config(ax):
    ax.view_init(5,-146)

    # x axis tick labels
    ax.set_xlim(-70000, 40000)
    ax.set_xticks([-60000,  -40000, -20000, 0, 20000, 40000])
    ax.set_xticklabels([-60000,  -40000, -20000, 0, 20000, 40000], fontsize=23, fontweight='bold')
    ax.tick_params(axis='x', which='major', pad=15)

    # Gridlines
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

    # Resize and label the y axis
    # y axis tick labels
    ax.set_yticks([0,3,7,10])
    ax.set_yticklabels(['5p','35p','65p', '95p'],fontsize=23, fontweight = 'bold')
    ax.set_ylim3d(0, 11)

    # x y z main labels
    ax.set_xlabel('Distance from benchmark ($)', fontweight = 'bold', labelpad = 65, fontsize = 30)
    ax.set_ylabel('Percentile',  labelpad = 35, fontsize = 30, fontweight = 'bold')
    ax.set_zlabel('Adjusted annual household income ($)', rotation = 90, labelpad = 95, fontsize = 30, fontweight = 'bold')

    ax.set_yticklabels(['5p','35p','65p','95p'],fontsize=23, fontweight = 'bold')


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
