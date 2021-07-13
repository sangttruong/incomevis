import multiprocessing, concurrent.futures, os, sys, IPython, json
import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib as mpl, matplotlib.ticker as ticker
from collections import OrderedDict
from matplotlib import animation, rc
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from statsmodels.graphics.utils import _import_mpl, create_mpl_fig
from scipy.stats import gaussian_kde, norm
import os.path
import utils

from bootstrap import bootstrap_age, bootstrap_var

dir_name = os.path.dirname(__file__) + '/data/'

class incomevis:
  def __init__(self, input_path_ipums = '', input_path_rpp = ''):
    utils.features()
    if not input_path_ipums: self.__raw = pd.concat([pd.read_csv(dir_name + 'ipums-cps-lite1.gz'),
                                                     pd.read_csv(dir_name + 'ipums-cps-lite2.gz')])
    else: self.__raw = pd.read_csv(input_path_ipums)
    if not input_path_rpp: self.__rpp = pd.read_csv(dir_name + 'rpp.csv')
    else: self.__rpp = pd.read_csv(input_path_rpp)
    self.__raw = pd.merge(self.__raw, self.__rpp, how = 'outer', on = ['YEAR', 'STATEFIP'])
    self.__raw = self.__raw[self.__raw['HFLAG'] != 1]
    self.__raw = self.__raw.drop(columns = ['HFLAG'])
    self.__raw = self.__raw[self.__raw['YEAR'] > 1976]
    self.__statefips = list(set(self.__raw['STATEFIP']))
    self.__state_name = utils.state_name
    self.label_list = ['']
    notLabelList = list(set(self.__state_name) - set(self.label_list))
    notLabelDict = dict.fromkeys(notLabelList , '')
    self.__state_name = pd.DataFrame(data = self.__state_name, index = self.__statefips, columns = ['State'])
    self.state_label = self.__state_name.replace(to_replace = notLabelDict)
    self.state_label = self.state_label.rename(columns = {'State': 'Label'})
    self.__colors = ['#FF0000', '#FF0A00', '#FF1400', '#FF1E00', '#FF2800', '#FF3300', '#FF3D00',
                     '#FF4700', '#FF5100', '#FF5B00', '#FF6600', '#FF7000', '#FF7A00', '#FF8400',
                     '#FF8E00', '#FF9900', '#FFA300', '#FFAD00', '#FFB700', '#FFC100', '#FFCC00',
                     '#FFD600', '#FFE000', '#FFEA00', '#FFF400', '#FFFF00', '#F4FF00', '#EAFF00',
                     '#E0FF00', '#D6FF00', '#CCFF00', '#C1FF00', '#B7FF00', '#ADFF00', '#A3FF00',
                     '#99FF00', '#8EFF00', '#84FF00', '#7AFF00', '#70FF00', '#66FF00', '#5BFF00',
                     '#51FF00', '#47FF00', '#3DFF00', '#32FF00', '#28FF00', '#1EFF00', '#14FF00',
                     '#0AFF00', '#00FF00']
    self.__colors = pd.DataFrame(self.__colors, columns = ['Color'], index = self.__statefips)
    self.__deciles = np.arange(0.05, 1.05, 0.1) # 10
    self.__deciles = np.insert(arr = self.__deciles, obj = 5, values = 0.5) # 11  
    self.__percentiles = np.arange(0.02, 1, 0.01) # 98
    self.__decileNames = utils.decile
    self.__percentileNames = utils.percentile
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
                   year_start = 1977, year_end = 2019, n = 100000, 
                   output_path = dir_name, toState = False,
                   provide_colorFrame = False, colorFrame = [], returnColor = False,
                   provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False,
                   AmChart = True, bs_var = False, bs_age = False):
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
        state_df = year_df[year_df['STATEFIP'] == statefip] # Generate state dataframe

        # Untested bootstrap
        if bs_age == True:
          state_df = bootstrap_age(year_df, n=n, year=year, statefip=statefip)
        if bs_var == True:
          state_df = bootstrap_var(year_df, seed=0, incomeType=incomeType, 
                                   statefip=statefip, year=year, n=n)
                                   
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

  def getIncomevis_subpop(self, subpop = False, black = None, hispan = None, sex=None, educ=None):
    if subpop:
      if black is not None:
        if black == True:
          self.__raw = self.__raw.loc[(self.__raw['RACE'] == 200) | (self.__raw['RACE'] == 801) | (self.__raw['RACE'] == 805) | (self.__raw['RACE'] == 806) |
                                      (self.__raw['RACE'] == 807) | (self.__raw['RACE'] == 810) | (self.__raw['RACE'] == 811) |
                                      (self.__raw['RACE'] == 814) | (self.__raw['RACE'] == 816) | (self.__raw['RACE'] == 818), :]
        if black == False:
          self.__raw = self.__raw.loc[(self.__raw['RACE'] != 200) & (self.__raw['RACE'] != 801) & (self.__raw['RACE'] != 805) & (self.__raw['RACE'] != 806) &
                                      (self.__raw['RACE'] != 807) & (self.__raw['RACE'] != 810) & (self.__raw['RACE'] != 811) &
                                      (self.__raw['RACE'] != 814) & (self.__raw['RACE'] != 816) & (self.__raw['RACE'] != 818), :]         
      if hispan is not None:
        if hispan == True:
          self.__raw = self.__raw.loc[(self.__raw['HISPAN'] > 0) & (self.__raw['HISPAN'] < 900), :]
        if hispan == False:
          self.__raw = self.__raw.loc[self.__raw['HISPAN'] == 0, :]
      if sex is not None:
        if sex == True:
          self.__raw = self.__raw.loc[self.__raw['SEX'] == 1, :]
        if sex == False:
          self.__raw = self.__raw.loc[self.__raw['SEX'] == 2, :]
      if educ is not None:
        if educ == True:
          self.__raw = self.__raw.loc[(self.__raw['EDUC'] > 73) & (self.__raw['EDUC'] < 999), :]
        if educ == False:
          self.__raw = self.__raw.loc[(self.__raw['EDUC'] > 2) & (self.__raw['EDUC'] <= 73), :]


  def getIncomevis_nation(self, incomeType='RPPERHHINCOME', k='decile', year=2019, output_path=''):
      # Adjustable variable
      year_df = self.__raw[self.__raw['YEAR'] == year] 

      # Generate result grid, decile-column
      if k == 'decile':
          result = pd.DataFrame(index = utils.decile, columns = ['nation'])
      if k == 'percentile':
          result = pd.DataFrame(index = utils.percentile, columns = ['nation'])

      # Iterate through each state
      c = 0
      # for statefip in __statefips:
      state_df = year_df # Generate state dataframe
      state_df = state_df.reset_index(drop = True)
      state_df = state_df.sort_values(incomeType) # Sort state dataframe by RHHINCOME
      state_df['CUMWTH'] = state_df['ASECWTH'].cumsum() # Calculate cumulated weight and Percentage
      state_df['PERCENTH'] = state_df['CUMWTH']/(state_df['ASECWTH'].sum())

      # Calculate decile
      if k == 'decile':
          r = 0
          for kile in [0.05, 0.15, 0.25, 0.35, 0.45, 0.50, 0.55, 0.65, 0.75, 0.85, 0.95]:
              result.iloc[r,c] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
              r = r + 1
          c = c + 1
      if k == 'percentile':
          r = 0
          for kile in np.arange(0.02, 1, 0.01):
              result.iloc[r,c] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
              r = r + 1
          c = c + 1

      # Transpose result table: column-decile
      result = result.T

      # Save to csv
      result.to_csv(output_path + 'nation_' + k + '_' + str(incomeType) + '_' + str(year) + '.csv')        
  
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