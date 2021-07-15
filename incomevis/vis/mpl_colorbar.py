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