#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import matplotlib, matplotlib.pyplot as plt
import pandas as pd, numpy as np

# Owned
from incomevis.utils import *
from incomevis.utils.path import *
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def getColor(type):
    """
        Gather color gradient based on the given benchmark (nation). More detailed 
        documentation is coming soon. 
        Parameters
        ----------

        type: str
            Type of collor pallette. Currently support ``'classic'`` or one of the 
            incomeType (``'HHINCOME'``, ``'RHHINCOME'``, ``'ERHHINCOME'``, and 
            ``'RPPERHHINCOME'``)

        k: str
            Method of partitioning income, which is either ``'decile'`` or ``'percentile'``. 
            Default: ``'decile'``.

        group: str
            Allowing to export (sub)population of data. Currently supported ``'all'``,
            ``'male'``, ``'female'``, ``'black'``, ``'non-black'``, ``'hispan'``, 
            ``'non-hispan'``, ``'high-educ'``, ``'low-educ'``. Default: ``'all'``. 

        Returns
        ----------
        class 'list'
            if the input type is 'classic'
        pandas.DataFrame object
            if the input type is one of the household income type.
    """
    if type == 'classic': return ['#FF0000', '#FF0A00', '#FF1400', '#FF1E00', '#FF2800', '#FF3300', '#FF3D00',
                                    '#FF4700', '#FF5100', '#FF5B00', '#FF6600', '#FF7000', '#FF7A00', '#FF8400',
                                    '#FF8E00', '#FF9900', '#FFA300', '#FFAD00', '#FFB700', '#FFC100', '#FFCC00',
                                    '#FFD600', '#FFE000', '#FFEA00', '#FFF400', '#FFFF00', '#F4FF00', '#EAFF00',
                                    '#E0FF00', '#D6FF00', '#CCFF00', '#C1FF00', '#B7FF00', '#ADFF00', '#A3FF00',
                                    '#99FF00', '#8EFF00', '#84FF00', '#7AFF00', '#70FF00', '#66FF00', '#5BFF00',
                                    '#51FF00', '#47FF00', '#3DFF00', '#32FF00', '#28FF00', '#1EFF00', '#14FF00',
                                    '#0AFF00', '#00FF00']
    else:
        incomeType = type
        k = 'decile'
        cm_str='bwr'
        reversed_cm = True
        input_path = DEFLATED_DATA_PATH
        benchmark_path = BENCHMARK_DATA_PATH
        group = 'all'
        year_end = 2019

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
        year_df = pd.read_csv(input_path + k + '_' + group + '_year_matplotlib_' + incomeType + '1976.csv', index_col='State')
        nat = pd.read_csv(benchmark_path + k + '_' + group + '_year_matplotlib_' + incomeType + str(year_end-1) +'.csv')
        year_df['Location'] = year_df['50p'].values - nat['50p'].values
        year_df['Location'] = year_df['Location'].apply(np.int64)
        state_map = []
        for i in range(len(year_df)): state_map.append(color_map[year_df['Location'][i]])
        year_df['new_color'] = state_map
        new_color_map = year_df['new_color'].to_dict()
        return new_color_map
