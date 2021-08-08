#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import IPython, json, pandas as pd, numpy as np
from collections import OrderedDict

# Owned
from incomevis.utils import *
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def visualize(k = 'decile', year = 1977, input_path = '', toState = False):
  """
    Get interactive visualization in AmChart. Receive deflated data of a year with
    normalized (potentially unrounded) population with details. The data is assumed to
    have (1) an index column using ``STATEFIP``, (2) ``State``, (3) kiles name,
    (4) ``Label``, (5) ``Color``, and (6) ``UR_NORMPOP_$year$``, with ``$year$`` 
    replaced with the year of the visualization.

    Parameters
    ----------
    input_path : str
      Absolute path to data file. Default: Empty string

    year : int
      Year of visualization. Default: 1977
    
    k: str
      Method of partitioning income, which is either ``'decile'`` or ``'percentile'``. 
      Default: ``'decile'``.
    
    Returns
    ----------
    There is no return for this function.

  """

  # Convert csv to json format
  result = pd.read_csv(input_path, index_col = 0)

  # Replicate each state's dataline with its respective replication number
  for statefip in getStateName('numeric'):
    rep = result.loc[statefip, 'UR_NORMPOP_' + str(year-1)] - 1
    rep = int(rep)
    line = pd.DataFrame(result.loc[statefip]).T
    line.loc[statefip, 'Label'] = ''
    for _ in range(0, rep): result = pd.concat([result, line])

  # Add the middle property
  result.reset_index(drop = True, inplace = True)
  result.sort_values(by=['State'], inplace = True)
  result['Middle'] = np.nan
  counter = 0
  for state in getStateName('string'):
    temp = result[result['State'] == state]
    temp_size = len(temp.index)
    middle = (temp_size // 2)
    counter = counter + middle
    result.iloc[counter, -1] = 1
    counter = counter - middle + temp_size
  result.sort_values(by=['50p', 'Middle'], inplace = True)

  # Convert dataframe to JSON
  result = result.to_json(orient = 'records')
  result = json.loads(result, object_pairs_hook = OrderedDict)
  result = json.dumps(result, indent = 4, sort_keys = False) # Make JSON format readable

  # Open html environment and display
  if k == 'decile':
    if(not toState): html1 = open(SOURCE_DATA_PATH + 'html1_d_year.txt', 'r')
    else: html1 = open(SOURCE_DATA_PATH + 'html1_p_state.txt', 'r')
  elif k == 'percentile':
    if (not toState): html1 = open(SOURCE_DATA_PATH + 'html1_p_year.txt', 'r')
    else: html1 = html1 = open(SOURCE_DATA_PATH + 'html1_p_state.txt', 'r')
  html2 = open(SOURCE_DATA_PATH + 'html2.txt', 'r')
  result = html1.read() + result + html2.read()
  IPython.display.HTML(data = result)
  