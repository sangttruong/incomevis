Helper functions
================

.. py:function:: getInteractive(k = 'decile', toState = False, outputHTML = False, input_path = 'package/directory/' + 'RHHINCOME1976.js', output_path = 'package/directory/' + 'RHHINCOME1976.html')

   :param k: segmentation level, which can either be 'decile' or 'percentile'
   :param toState: if true will display state graph instead of year graph
   :param outputHTML: if true will output an HTML file in the specified output path
   :param input_path: input path of the file that needs to be displayed
   :param output_path: input path of the HTML file that will be printed out
   :rtype: IPython.display.HTML object
   :return: Interactive graph

.. py:function:: getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, highlight = '', input_path = 'package/directory/')

   :param incomeType: income type. By default, there are 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
   :param year_start: Analysis starting year
   :param year_end: Analysis ending year, which also be included
   :param highlight: Full name (not STATEFIP) of state that will be highlighted.
   :param input_path: input directory of all files that will be animated
   :rtype: matplotlib.animation.FuncAnimation object
   :return: animated graph

.. py:function:: KDE(data = pd.read_csv('package/directory/' + 'xRHHINCOME1977_11_10000.csv'))

   :param data: data () that will be compared to the normal distribution
   :rtype: matplotlib.pyplot.figure object
   :return: Kernel density estimation of the input data


