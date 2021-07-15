import os, IPython, json
import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib as mpl, matplotlib.ticker as ticker
from collections import OrderedDict
from matplotlib import animation, rc
from mpl_toolkits.mplot3d.axes3d import Axes3D
from scipy.stats import gaussian_kde, norm
import os.path
from incomevis.utils import *

class incomevis:
  def __init__(self, data_path = ''):
    self.__raw = pd.concat([pd.read_csv(data_path + 'ipums-cps-lite1.gz'),
                            pd.read_csv(data_path + 'ipums-cps-lite2.gz')])
    self.__rpp = pd.read_csv(data_path + 'rpp.csv')

    self.__raw = pd.merge(self.__raw, self.__rpp, how = 'outer', on = ['YEAR', 'STATEFIP'])
    self.__raw = self.__raw[self.__raw['HFLAG'] != 1]
    self.__raw = self.__raw.drop(columns = ['HFLAG'])
    self.__raw = self.__raw[self.__raw['YEAR'] > 1976]
    self.__statefips = list(set(self.__raw['STATEFIP']))
    self.label_list = ['']
    notLabelList = list(set(incomevis.utils.getStateName) - set(self.label_list))
    notLabelDict = dict.fromkeys(notLabelList , '')
    self.__state_name = pd.DataFrame(data = incomevis.utils.getStateName, index = self.__statefips, columns = ['State'])
    self.state_label = self.__state_name.replace(to_replace = notLabelDict)
    self.state_label = self.state_label.rename(columns = {'State': 'Label'})

    self.__colors = incomevis.utils.getColor()
    self.__colors = pd.DataFrame(self.__colors, columns = ['Color'], index = self.__statefips)
    self.__deciles = incomevis.utils.getDecile('numeric')
    self.__percentiles = incomevis.utils.getPercentile('numeric')
    self.__decileNames = incomevis.utils.getDecile('string')
    self.__percentileNames = incomevis.utils.getPercentile('string')
    self.__pop = pd.DataFrame()
    for year in range(self.__raw['YEAR'].min(), self.__raw['YEAR'].max() + 1):
      year_df = self.__raw[self.__raw.YEAR == year]
      self.__pop['POP_' + str(year)] = year_df.groupby(['STATEFIP'])['ASECWTH'].agg('sum')
      self.__pop['UR_NORMPOP_' + str(year)] = self.__pop['POP_' + str(year)]/(np.percentile(self.__pop['POP_' + str(year)], 10))
      self.__pop['NORMPOP_' + str(year)] = round(self.__pop['UR_NORMPOP_' + str(year)])
  
  def getPop (self): return self.__pop
  
  def getData (self): return self.__raw
   
  def getSTATEFIPS (self): return self.__statefips
 
  def adjustIncome(self):
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

  def getIncomevis(self, incomeType = 'RHHINCOME', k = 'decile',
                   year_start = 1977, year_end = 2019,
                   output_path = '',
                   toState = False,
                   provide_colorFrame = False, colorFrame = [], returnColor = False,
                   provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False,
                   AmChart = True,
                   subpop = False, black = None, hispan = None, sex=None, educ=None,
                   age_resampling = False, age_resampling_freq = 100,
                   benchmark = False, benchmark_year = 2019):
    if subpop:
      if black is not None:
        if black == True:
          sub_raw = self.__raw.loc[(self.__raw['RACE'] == 200) | (self.__raw['RACE'] == 801) | (self.__raw['RACE'] == 805) | (self.__raw['RACE'] == 806) |
                                      (self.__raw['RACE'] == 807) | (self.__raw['RACE'] == 810) | (self.__raw['RACE'] == 811) |
                                      (self.__raw['RACE'] == 814) | (self.__raw['RACE'] == 816) | (self.__raw['RACE'] == 818), :]
        if black == False:
          sub_raw = self.__raw.loc[(self.__raw['RACE'] != 200) & (self.__raw['RACE'] != 801) & (self.__raw['RACE'] != 805) & (self.__raw['RACE'] != 806) &
                                      (self.__raw['RACE'] != 807) & (self.__raw['RACE'] != 810) & (self.__raw['RACE'] != 811) &
                                      (self.__raw['RACE'] != 814) & (self.__raw['RACE'] != 816) & (self.__raw['RACE'] != 818), :]         
      if hispan is not None:
        if hispan == True:
          sub_raw = self.__raw.loc[(self.__raw['HISPAN'] > 0) & (self.__raw['HISPAN'] < 900), :]
        if hispan == False:
          sub_raw = self.__raw.loc[self.__raw['HISPAN'] == 0, :]
      if sex is not None:
        if sex == True:
          sub_raw = self.__raw.loc[self.__raw['SEX'] == 1, :]
        if sex == False:
          sub_raw = self.__raw.loc[self.__raw['SEX'] == 2, :]
      if educ is not None:
        if educ == True:
          sub_raw = self.__raw.loc[(self.__raw['EDUC'] > 73) & (self.__raw['EDUC'] < 999), :]
        if educ == False:
          sub_raw = self.__raw.loc[(self.__raw['EDUC'] > 2) & (self.__raw['EDUC'] <= 73), :]

    for year in range(year_start, year_end+1):
      year_df = self.__raw[self.__raw['YEAR'] == year] # Generate year_df dataframe

      # Decile or percentile
      if (k == 'decile'):
        kiles = self.__deciles
        kNames = self.__decileNames
      elif (k == 'percentile'):
        kiles = self.__percentiles
        kNames = self.__percentileNames
      else: raise ValueError('Illegal value of k. k can only be either decile or percentile.')

      # Generate result grid, decile-column
      result = pd.DataFrame(index = kNames, columns = self.__statefips)

      # Iterate through each state
      c = 0
      for statefip in self.__statefips:
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
      if (toState): result.to_csv(output_path + k + '_state_temp_' + incomeType + str(year-1) + '.csv', index = True)

      # Base color
      if(not provide_colorFrame): colorFrame = pd.DataFrame(data = list(self.__colors['Color']), index = orderFrame, columns=['Color'])
      if (returnColor): return colorFrame
      result = pd.concat([self.__state_name, result, self.state_label, colorFrame], axis = 1)

      # Amchart vs. Matplotlib
      if (AmChart):
        # Replicate each state's dataline with its respective replication number
        for statefip in self.__statefips:
          rep = self.__pop.loc[statefip, 'NORMPOP_' + str(year)] - 1
          rep = int(rep)
          line = pd.DataFrame(result.loc[statefip]).T
          line.loc[statefip, 'Label'] = ''
          for _ in range(0, rep): result = pd.concat([result, line])
        result.reset_index(drop = False, inplace = True)
        result.rename_axis('ID', inplace = True)
        result.rename(columns={'index': 'STATEFIP'}, inplace = True)
        result.set_index('STATEFIP', append=True, inplace=True)
        result = result.groupby(['STATEFIP', 'ID']).sum() # Sum has no effect since all key combinations are unique
        result = result.reindex(orderFrame, level = 'STATEFIP')

        # Add the middle property
        result.reset_index(drop = True, inplace = True)
        result['Middle'] = np.nan
        counter = 0
        for state in result.State.drop_duplicates():
          temp = result[result.State == state]
          temp_size = len(temp.index)
          middle = (temp_size // 2)
          counter = counter + middle
          result.loc[counter, 'Middle'] = 1
          counter = counter - middle + temp_size
        
        # Convert dataframe to JSON
        result = result.to_json(orient = 'records')
        result = json.loads(result, object_pairs_hook = OrderedDict)
        result = json.dumps(result, indent = 4, sort_keys = False) # Make JSON format readable

        # Save JSON file -- y-1 adjusts sample year_df to HHINCOME year_df
        with open(output_path + k + '_year_amchart_js_' + incomeType + str(year-1) + '.js', 'w') as outfile:
          outfile.write(result)
      else:
        result = pd.merge(result, self.__pop['UR_NORMPOP_' + str(year)], left_index = True, right_index = True)
        result = result.reindex(index = orderFrame)
        result.to_csv(output_path + k + '_year_matplotlib_' + incomeType + str(year-1) + '.csv', index = True)
    
    if (toState):    
      for statefip in self.__statefips:
        #Reformat the columns
        data_df = []
        index_df = [i for i in range(0, 43)]
        for year in range(year_start, year_end+1):
          df = pd.read_csv(output_path + k + '_state_temp_' + incomeType + str(year-1) + '.csv', index_col = 0)
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
        with open(output_path + k + '_state_' + incomeType + str(year-1) + '.js', 'w') as outfile:
          outfile.write(state_df)
          
      for year in range(year_start, year_end+1):
        os.remove(output_path + k + '_state_temp_' + incomeType + str(year-1) + '.csv')
        