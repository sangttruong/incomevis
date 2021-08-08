import IPython, json, pandas as pd, numpy as np
from collections import OrderedDict
from incomevis.utils import *

def visualize(k = 'decile', year = 1977, toState = False,
              input_path = ''):
  """
    Get interactive visualization in AmChart. Receive deflated data of a year with
    normalized (potentially unrounded) population with details. The data is assumed to
    have (1) an index column using STATEFIP, (2) State, (3) kiles name,
    (4) Label, (5) Color, and (6) UR_NORMPOP_$year$, with $year$ replaced with the
    economic of the visualization.

    Parameters
    ----------
    input_path : str
      Default: Empty string
      Absolute path to data file.

    year : int
      Default: 1977
      Year when the data was collected by IPUMS-CPS (not the economic year).
      Nonetheles, note that file name or details inside of file are often
      following economic year instead of data collection year. For example, 
      year = 1976 is invalid because there is no data collected on 1976. Yet, 
      in this package, we see analysis of the economy in 1976 using data collected
      in 1977.
    
    k: st
      Default: "decile"
      Either "decile" or "percentile" 

    toState: bool
      Default: False
      Whether or not converting the data to one state, many year format. 
      Currently unsupported.

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
  return IPython.display.HTML(data = result)