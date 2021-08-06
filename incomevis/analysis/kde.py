from scipy.stats import gaussian_kde, norm
# KDE is now unavailable
# def KDE(data = pd.read_csv(dir_name + 'xRHHINCOME1977_11_10000.csv')['50p']):
#   fig = plt.figure(figsize=(15,7))
#   data = (data - np.nanmean(data)) / np.nanstd(data)
#   data_nonmissing = data[~(np.isnan(data))]
#   try: plt.hist(data_nonmissing, 60, density = True, label = 'Normalized bootstrap histogram', facecolor = '#568ae6', alpha = 0.3)
#   except AttributeError: plt.hist(data_nonmissing, 60, normed = True, label = 'Normalized bootstrap histogram', facecolor = '#568ae6', alpha = 0.3)
#   kde = gaussian_kde(data_nonmissing, bw_method = 0.3)
#   xlim = (-1.96*2, 1.96*2)
#   x = np.linspace(xlim[0], xlim[1])
#   plt.plot(x, kde(x), 'r--', linewidth = 2, color = '#a924b7', label = 'KDE')
#   plt.plot(x, norm.pdf(x), 'r--', linewidth = 2, color = '#449ff0', label = r'$\mathcal{N}(0,1)$')
#   plt.xlim(xlim)
#   plt.legend()
#   plt.grid(True)
#   plt.xlabel('', fontweight = 'bold', fontsize = 'x-large')
#   plt.ylabel('', fontweight = 'bold', fontsize = 'x-large')
#   plt.close()
#   return fig
