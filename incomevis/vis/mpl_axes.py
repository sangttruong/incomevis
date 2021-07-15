def axis_config(ax, axes_config):
    ax.view_init(5,-146)
    axes_dict = {'xaxis': [ax.set_xlim, ax.set_xticks, ax.set_xticklabels, ax.set_xlabel, ax.xaxis],
                 'yaxis': [ax.set_ylim, ax.set_yticks, ax.set_yticklabels, ax.set_ylabel, ax.yaxis],
                 'zaxis': [ax.set_zlim, ax.set_zticks, ax.set_zticklabels, ax.set_zlabel, ax.zaxis]}

    for axis in axes_config.key:
        axes_config[axis][0](config_dict[axis][0][0], config_dict[axis][0][1]) 
        ax.set_zticks(zticks)
        ax.set_zticklabels(ztickslabel,fontsize=15, fontweight='bold')
        ax.set_zlabel(zlabel, fontweight = 'bold', labelpad = zlabelpad, fontsize = 20, rotation = 90)
        ax.tick_params(axis = 'z', which = 'major', pad = zpad)
        axes_dict[axis][4].xaxis._axinfo["grid"].update({"linewidth":3, "color" : "grey", 'linestyle': '-.'})
        axes_dict[axis][4].xaxis.pane.fill = False # remove fill
        axes_dict[axis][4].xaxis.pane.set_edgecolor('w') # set color to white
