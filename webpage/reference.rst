.. incomevis documentation master file, created by
   sphinx-quickstart on Mon Jul  5 11:01:17 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root toctree directive.



Reference manual
=====================================

Constructor
------------

.. py:class:: incomevis(input_path_ipums = '', input_path_rpp = '')

   :param input_path_ipums: path to IPUMS file. By default, data of ASEC samples from IPUMS-CPS of 1977-2019 sample year with only YEAR, ASECWTH, CPI99, STATEFIP, HHINCOME, PERNUM, and HFLAG variables will be used. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
   :param input_path_rpp: path to regional price parity deflator file. By default, data from from BEA of 2008-2019 sample year will be use. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).

Methods
--------

.. py:function:: getData()

   :param: None
   :rtype: Pandas dataframe 
   :return: primary dataframe that is currently in the analysis flow.
     
.. py:function:: getPop()

   :param: None
   :rtype: Pandas dataframe
   :return: relative population of all states and all years from the input dataset.

.. py:function:: getSTATEFIPS()

   :param: None
   :rtype: list
   :return: a list of STATEFIP as defined by IPUMS-CPS
     
.. py:function:: adjustIncome()

   :param: None
   :rtype: Pandas dataframe
   :return: primary dataframe that has adjusted HHINCOME based on 3 deflators combinations: CPI, CPI-HHSIZE, and CPI-HHSIZE-RPP
     
.. py:function:: getIncomevis(incomeType = 'RHHINCOME', k = 'decile', year_start = 1977, year_end = 2019, output_path = 'package/directory', toState = False, provide_colorFrame = False, colorFrame = [], returnColor = False, provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False, AmChart = True)

   :param incomeType: income type. By default, there are 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
   :param k: segmentation level, which can either be 'decile' or 'percentile'
   :param year_start: Analysis starting year
   :param year_end: Analysis ending year, which also be included
   :param output_path: output path. We highly recommend the users to specify their own output path to avoid missing file or confusion
   :param toState: if true will also return a set of state graph with the respective year ranges
   :param provide_colorFrame: if colorframe will be provided or not
   :param colorFrame: color list, which will be ignored if provide_colorFrame is set to False
   :param returnColor: if the colorframe is returned or not
   :param provide_orderFrame: if the orderframe will be provided or not
   :param orderFrame: orderframe, which will be ignored if provide_orderFrame is set to False
   :param returnOrder: if the orderframe is returned or not
   :param AmChart: library that will be used for rendering the visualization. If False, Matplotlib will be used.
   :rtype: None
   :return: None

.. py:function:: bootstrap(seed = 0, incomeType = 'RHHINCOME', k = 'decile', year = 1977, statefip = 1, n = 1000000, output_path = 'package/directory')

   :param seed: seed of the uniform random sampling
   :param incomeType: income type. By default, there are 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
   :param k: segmentation level, which can either be 'decile' or 'percentile'
   :param year: bootstrapping year
   :param statefip: bootstrapping state
   :param n: number of iteration
   :param output_path: output path. We highly recommend the users to specify their own output path to avoid missing file or confusion
   :rtype: Pandas dataframe
   :return: bootstrapting result

Helper functions
-----------------

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


