#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import os, json, pandas as pd, numpy as np
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

class incomevis:
  """
    Primary object for data processing. The object of this class takes input data from 
    IPUMS-CPS and IPUMS-USA and deflate them.
    
    Parameters
    ----------
    None
      Constructor of this class does not take parameter.

    Attributes
    ----------
      raw: ``pandas DataFrame``
        Raw data from IPUMS-CPS. By default, data of ASEC samples from IPUMS-CPS of 1977-2020 sample year with only
        YEAR, ASECWTH, CPI99, STATEFIP, HHINCOME, PERNUM, HFLAG variables and a few more demographic variables will be used.
        Details about specific demographic variables are coming soon. 
      
      rpp: ``pandas DataFrame``
        Regional price parity (RPP) data from IPUMS-USA.
      
      pop: ``pandas DataFrame``
        Population for all year and states
  """
  def __init__(self):
    self.__raw = pd.concat([pd.read_csv(SOURCE_DATA_PATH + 'ipums-cps-1-2020.zip'),
                            pd.read_csv(SOURCE_DATA_PATH + 'ipums-cps-2-2020.zip')])
    self.__rpp = pd.read_csv(SOURCE_DATA_PATH + 'rpp.csv')
    self.__raw = pd.merge(self.__raw, self.__rpp, how = 'outer', on = ['YEAR', 'STATEFIP'])
    self.__raw = self.__raw[self.__raw['HFLAG'] != 1]
    self.__raw = self.__raw.drop(columns = ['HFLAG'])
    self.__raw = self.__raw[self.__raw['YEAR'] > 1976]

    # Redundant information that need to be removed soon. 
    notLabelList = list(set(getStateName('string')) - set(['']))
    notLabelDict = dict.fromkeys(notLabelList , '')
    self.__state_name = pd.DataFrame(data = getStateName('string'), index = getStateName('numeric'), columns = ['State'])
    self.state_label = self.__state_name.replace(to_replace = notLabelDict)
    self.state_label = self.state_label.rename(columns = {'State': 'Label'})
    self.__colors = pd.DataFrame(getColor('classic'), columns = ['Color'], index = getStateName('numeric'))
    
    self.__pop = pd.DataFrame()
    for year in range(self.__raw['YEAR'].min(), self.__raw['YEAR'].max() + 1):
      year_df = self.__raw[self.__raw.YEAR == year]
      self.__pop['POP_' + str(year)] = year_df.groupby(['STATEFIP'])['ASECWTH'].agg('sum')
      self.__pop['UR_NORMPOP_' + str(year)] = self.__pop['POP_' + str(year)]/(np.percentile(self.__pop['POP_' + str(year)], 10))
      self.__pop['NORMPOP_' + str(year)] = round(self.__pop['UR_NORMPOP_' + str(year)])

  def getPop (self):
    """
      Return population for all state and all year in a Pandas dataframe.
      This method does not take parameter.

      Parameters
      ----------
      None
        This method does not take parameter.

      Returns
      ----------
      ``pandas DataFrame`` object
        Dataframe of population

    """
    return self.__pop

  def getData (self):
    """
      Return the inspected dataset in a Pandas dataframe. This method does not take parameter.
      
      Parameters
      ----------
      None
        This method does not take parameter.
      
      Returns
      ----------
      ``pandas DataFrame`` object
        Dataframe of full data
    """
    return self.__raw

  def adjustIncome(self):
    """
      Deflating househould income (HHINCOME) with consumer price index (CPI), househouse
      effective size (HHSIZE), and regional parity price (RPP). The result are real household 
      income (RHHINCOME, deflated with only CPI), equivalent real household income (ERHHINCOME, 
      deflated with CPI and HHSIZE), and regional-equivalent-real household income (RPPERHHINCOME, 
      deflated with all three deflators). This method does not take parameter.

      Parameters
      ----------
      None
        This method does not take parameter.

      Returns
      ----------
      ``pandas DataFrame`` object
        Dataframe of deflated data
    """
    # 1. RHHINCOME in 2018 dollars
    self.__raw['RHHINCOME'] = self.__raw['HHINCOME']*self.__raw['CPI99']*(1/0.652)

    # 2. ERHHINCOME:
    length = len(self.__raw[self.__raw['PERNUM'] == 1])
    self.__raw.loc[self.__raw['PERNUM'] == 1, 'HHID'] = np.arange(length)
    self.__raw = self.__raw.fillna(method = 'pad')
    hhsize = self.__raw.groupby(['HHID']).agg(HHSIZE = ('HHID', 'count'))
    self.__raw = pd.merge(self.__raw, hhsize, on = ['HHID'])
    self.__raw = self.__raw[self.__raw['PERNUM'] == 1]
    self.__raw['HHSIZE'] = (self.__raw['HHSIZE'])**(1/2)
    self.__raw['ERHHINCOME'] = self.__raw['RHHINCOME']/self.__raw['HHSIZE']

    # 3. RPPRHHINCOME and RPPERHHINCOME
    self.__raw['RPPRHHINCOME'] = self.__raw['RHHINCOME']/(self.__raw['RPP']/100)
    self.__raw['RPPERHHINCOME'] = self.__raw['ERHHINCOME']/(self.__raw['RPP']/100)

    return self.__raw

  def getIncomevis(self, incomeType = 'RPPERHHINCOME', k = 'decile',
                   year_start = 1977, year_end = 2020,
                   group = 'all',
                   benchmark = False,

                   provide_colorFrame = False, colorFrame = [], returnColor = False,
                   provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False,
                   age_resampling = False,
                   age_resampling_freq = 100,
                   toState = False): # if benchmark = True, then the benchmark year is the end year
    """
      Get deflated household income for each year.

      Parameters
      ----------
      incomeType: str
        Type of household income. Currently supported ``'HHINCOME'``, ``'RHHINCOME'``, 
        ``'ERHHINCOME'``, and ``'RPPERHHINCOME'``. Default: ``'RPPERHHINCOME'``, i.e.
        fully deflated.

      k: str
        Method of partitioning income, which is either ``'decile'`` or ``'percentile'``. 
        Default: ``'decile'``.

      year_start: int
        Starting year of data that will be printed out. Default: 1977, i.e. the earliest
        year household income was meaningfully documented by IPUMS. 
      
      year_end: int
        Ending year of data that will be printed out. Default: 2020.

      group: str
        Allowing to export (sub)population of data. Currently supported ``'all'``,
        ``'male'``, ``'female'``, ``'black'``, ``'non-black'``, ``'hispan'``, 
        ``'non-hispan'``, ``'high-educ'``, ``'low-educ'``. Default: ``'all'``. 
      
      benchmark: bool
        Whether the exporting data is the benchmark data. If ``benchmark = True``, the
        default benchmark data is the national income (with respect to the selected 
        income type) at ``'year_end'``. Default: False.
      
      Returns
      ----------
      None
        This function has no return.
    """
    if benchmark: output_path = BENCHMARK_DATA_PATH
    else: output_path = DEFLATED_DATA_PATH
    if group != 'all':
      if group == 'black': self.__raw = self.__raw.loc[(self.__raw['RACE'] == 200) | (self.__raw['RACE'] == 801) | (self.__raw['RACE'] == 805) | (self.__raw['RACE'] == 806) |
                                                       (self.__raw['RACE'] == 807) | (self.__raw['RACE'] == 810) | (self.__raw['RACE'] == 811) |
                                                       (self.__raw['RACE'] == 814) | (self.__raw['RACE'] == 816) | (self.__raw['RACE'] == 818), :]
      elif group == 'non-black': self.__raw = self.__raw.loc[(self.__raw['RACE'] != 200) & (self.__raw['RACE'] != 801) & (self.__raw['RACE'] != 805) & (self.__raw['RACE'] != 806) &
                                                           (self.__raw['RACE'] != 807) & (self.__raw['RACE'] != 810) & (self.__raw['RACE'] != 811) &
                                                           (self.__raw['RACE'] != 814) & (self.__raw['RACE'] != 816) & (self.__raw['RACE'] != 818), :]
      elif group == 'hispan': self.__raw = self.__raw.loc[(self.__raw['HISPAN'] > 0) & (self.__raw['HISPAN'] < 900), :]
      elif group == 'non-hispan': self.__raw = self.__raw.loc[self.__raw['HISPAN'] == 0, :]
      elif group == 'male': self.__raw = self.__raw.loc[self.__raw['SEX'] == 1, :]
      elif group == 'female': self.__raw = self.__raw.loc[self.__raw['SEX'] == 2, :]
      elif group == 'high-educ': self.__raw = self.__raw.loc[(self.__raw['EDUC'] > 73) & (self.__raw['EDUC'] < 999), :]
      elif group == 'low-educ': self.__raw = self.__raw.loc[(self.__raw['EDUC'] > 2) & (self.__raw['EDUC'] <= 73), :]
      else: raise ValueError

    for year in range(year_start, year_end+1):
      year_df = self.__raw[self.__raw['YEAR'] == year] # Generate year_df dataframe

      # Decile or percentile
      kiles = getDecile('numeric') if k == 'decile' else getPercentile('numeric')
      kNames = getDecile('string') if k == 'decile' else getPercentile('string')

      # Generate result grid, decile-column
      result = pd.DataFrame(index = kNames, columns = getStateName('numeric'))

      # Iterate through each state
      c = 0
      for statefip in getStateName('numeric'):
        if (not benchmark):
          state_df = year_df[year_df['STATEFIP'] == statefip] # Generate state dataframe
        else: state_df = year_df # if generating national benchmark, there is no need of partition

        # Resampling to uniform age distribution
        if age_resampling:
          dist_age = pd.DataFrame()
          state_df = state_df.loc[(state_df['AGE'] >= 18) & (state_df['AGE'] < 80), :]
          age_list = list(set(state_df['AGE']))
          for age in age_list:
              origin = state_df.loc[(temp['AGE'] == age), :]
              resampling = pd.DataFrame()
              while(len(resampling) < age_resampling_freq):
                  new_temp = origin.sample(n=age_resampling_freq, replace=True)
                  temp_dist_age = pd.concat([temp_dist_age, new_temp])
                  dist_age = pd.concat([dist_age, temp_dist_age])
              dist_age.reset_index(inplace=True, drop=True)

          # Break out of each-state-loop since there is no notion on state for national benchmark
          if benchmark: break

        state_df = state_df.reset_index(drop = True)
        state_df = state_df.sort_values(incomeType) # Sort state dataframe by RHHINCOME
        state_df['CUMWTH'] = state_df['ASECWTH'].cumsum() # Calculate cumulated weight and Percentage
        state_df['PERCENTH'] = state_df['CUMWTH']/(state_df['ASECWTH'].sum())

        # Calculate decile
        r = 0
        for kile in kiles:
          result.iloc[r,c] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
          r = r + 1
        c = c + 1

      # Transpose result table: column-decile
      result = result.T

      if (not provide_orderFrame):
        sorted_result = result.sort_values(by = ['50p'], ascending = True)
        orderFrame = sorted_result.index
      if (returnOrder): return orderFrame

      # Output csv file for toState
      if (toState): result.to_csv(output_path + k + '_' + group +  '_state_temp_' + incomeType + str(year-1) + '.csv', index = True)

      # Base color
      if(not provide_colorFrame): colorFrame = pd.DataFrame(data = list(self.__colors['Color']), index = orderFrame, columns=['Color'])
      if (returnColor): return colorFrame

      result = pd.concat([self.__state_name, result, self.state_label, colorFrame], axis = 1)
      result = pd.merge(result, self.__pop['UR_NORMPOP_' + str(year-1)], left_index = True, right_index = True)
      result = result.reindex(index = orderFrame)
      result.to_csv(output_path + k + '_' + group + '_year_matplotlib_' + incomeType + str(year-1) + '.csv', index = True)

    if (toState):
      for statefip in getStateName('numeric'):
        #Reformat the columns
        data_df = []
        index_df = [i for i in range(0, 43)]
        for year in range(year_start, year_end+1):
          df = pd.read_csv(output_path + k + '_' + group + '_state_temp_' + incomeType + str(year-1) + '.csv', index_col = 0)
          data_df.append(df.loc[statefip].tolist())
        if (k == 'decile'): state_df = pd.DataFrame(data_df,columns = self.__decileNames,index=index_df)
        elif (k == 'percentile'): state_df = pd.DataFrame(data_df,columns=self.__percentileNames,index=index_df)
        else: raise ValueError('Illegal value of k. k can only be either decile or percentile.')
        state_df['Year'] = [i-1 for i in range(year_start, year_end + 1)]
        state_df['Label'] = ''
        if (k == 'decile'): state_df = state_df.reindex(columns = ['Year'] + self.__decileNames + ['Label'])
        elif (k == 'percentile'): state_df = state_df.reindex(columns = ['Year'] + self.__percentileNames + ['Label'])
        else: raise ValueError('Illegal value of k. k can only be either decile or percentile.')

        # Convert dataframe to JSON
        state_df = state_df.to_json(orient = 'records')
        state_df = json.loads(state_df, object_pairs_hook = OrderedDict)
        state_df = json.dumps(state_df, indent = 4, sort_keys = False) # Make JSON format readable

        # Save JSON file -- y-1 adjusts sample year to HHINCOME year
        with open(output_path + k + '_' + group + '_state_' + incomeType + str(year-1) + '.js', 'w') as outfile:
          outfile.write(state_df)

      for year in range(year_start, year_end+1):
        os.remove(output_path + k + '_' + group + '_state_temp_' + incomeType + str(year-1) + '.csv')
