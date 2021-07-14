import os, IPython, json
import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib as mpl, matplotlib.ticker as ticker
from collections import OrderedDict
from matplotlib import animation, rc
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from scipy.stats import gaussian_kde, norm
import os.path

dir_name = os.path.dirname(__file__) + '/data/'

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
    self.__state_name = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                        'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
                        'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
                        'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                        'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                        'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                        'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
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
    # self.__deciles = np.arange(0.05, 1.05, 0.1) # 10
    self.__deciles = [0.05, 0.15, 0.25, 0.35, 0.45, 0.5, 0.55, 0.65, 0.75, 0.85, 0.95]
    # self.__deciles = np.insert(arr = self.__deciles, obj = 5, values = 0.5) # 11  
    self.__percentiles = np.arange(0.02, 1, 0.01) # 98
    self.__decileNames = ['5p', '15p', '25p', '35p', '45p', '50p', '55p', '65p', '75p', '85p', '95p']
    self.__percentileNames = ['2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p',
                              '12p', '13p', '14p', '15p', '16p', '17p', '18p', '19p', '20p',
                              '21p', '22p', '23p', '24p', '25p', '26p', '27p', '28p', '29p',
                              '30p', '31p', '32p', '33p', '34p', '35p', '36p', '37p', '38p',
                              '39p', '40p', '41p', '42p', '43p', '44p', '45p', '46p', '47p',
                              '48p', '49p', '50p', '51p', '52p', '53p', '54p', '55p', '56p',
                              '57p', '58p', '59p', '60p', '61p', '62p', '63p', '64p', '65p',
                              '66p', '67p', '68p', '69p', '70p', '71p', '72p', '73p', '74p',
                              '75p', '76p', '77p', '78p', '79p', '80p', '81p', '82p', '83p',
                              '84p', '85p', '86p', '87p', '88p', '89p', '90p', '91p', '92p',
                              '93p', '94p', '95p', '96p', '97p', '98p', '99p']
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
                   output_path = dir_name,
                   toState = False,
                   provide_colorFrame = False, colorFrame = [], returnColor = False,
                   provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False,
                   AmChart = True):
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

  def getIncomevis_subpop(self, incomeType = 'RHHINCOME', k = 'decile',
                   year_start = 1977, year_end = 2019,
                   output_path = dir_name,
                   toState = False,
                   provide_colorFrame = False, colorFrame = [], returnColor = False,
                   provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False,
                   AmChart = True, 
                   subpop = False, black = None, hispan = None, sex=None, educ=None):
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
      year_df = sub_raw[sub_raw['YEAR'] == year] # Generate year_df dataframe

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


  def bootstrap(self, seed = 0, incomeType = 'RHHINCOME', k = 'decile',
                year = 1977, statefip = 1, n = 1000000,
                output_path = dir_name):
    np.random.seed(seed)
    year_df = self.__raw[self.__raw['YEAR'] == year]

    # Decile or percentile
    if (k == 'decile'):
      kiles = self.__deciles
      kNames = self.__decileNames
    elif (k == 'percentile'):
      kiles = self.__percentiles
      kNames = self.__percentileNames
    else: raise ValueError('Illegal value of k. k can only be either decile or percentile.')

    # Generate result grid, decile-column
    result = pd.DataFrame(index = kNames, columns = np.arange(n))

    # Resampling n times
    for i in range(n):
      # Generate state dataframe
      state_df = year_df[year_df['STATEFIP'] == statefip]
      state_df = state_df.reset_index(drop = True) # Optional
      # sample_size = len(state_df)
      
      # Resampling
      # index = np.random.choice(state_df.index, sample_size)
      # state_df = state_df.iloc[index, :]
      state_df = state_df.sample(frac= 1, replace=True)
      state_df = state_df.reset_index(drop = True)

      # Sort state dataframe by RHHINCOME
      state_df = state_df.sort_values(incomeType)

      # Calculate cumulated weight and Percentage
      state_df['CUMWTH'] = state_df['ASECWTH'].cumsum()
      state_df['PERCENTH'] = state_df['CUMWTH']/(state_df['ASECWTH'].sum())

      # Calculate decile
      r = 0
      for kile in kiles:
        result.iloc[r, i] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
        r = r + 1
    
      if (i%5000 == 0): print('Start iteration ' + str(i))        
    result = result.T
    result.to_csv(output_path + k + '_' + str(seed) + incomeType + str(year) + '_' + str(statefip) + '_' + str(n) + '.csv', index = False)
    return result
  
def getInteractive(k = 'decile', toState = False, outputHTML = False,
                   input_path = dir_name,
                   output_path = dir_name):
  #Missing files - Need to fix
  if k == 'decile':
    if(not toState): html1 = open(dir_name + 'html1_d_year.txt', 'r')
    else: html1 = open(dir_name + 'html1_p_state.txt', 'r')
  elif k == 'percentile':
    if (not toState): html1 = open(dir_name + 'html1_p_year.txt', 'r')
    else: html1 = html1 = open(dir_name + 'html1_p_state.txt', 'r')
  html2 = open(dir_name + 'html2.txt', 'r')

  #Need to fix 
  json = open(input_path + 'decile_year_amchart_js_RHHINCOME1976.js','r')
  AmChart = html1.read() + json.read() + html2.read()
  if outputHTML:
    with open(output_path + 'decile_year_amchart_html_RHHINCOME1976.html', 'w') as outfile:
      outfile.write(AmChart)
  return IPython.display.HTML(data = AmChart)

def getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, highlight = '',
                input_path = dir_name):
  # Display setting
  # fig = plt.figure(figsize=(15,15))
  fig = plt.figure(figsize=(20,17))
  ax = plt.axes(projection='3d')
  x_scale = 3 # Scalling
  y_scale = 1
  z_scale = 1
  scale = np.diag([x_scale, y_scale, z_scale, 1])
  scale = scale*(1.0/scale.max())
  scale[3, 3] = 0.7
  def short_proj(): return np.dot(Axes3D.get_proj(ax), scale)
  ax.get_proj = short_proj
  plt.subplots_adjust(left = -0.35, right = 1, bottom = -0.5, top = 2.45) # Bounding box adjustment
  plt.close()

  def animate(year):
    #Read the data
    pop_label = 'UR_NORMPOP_' + str(year+1)
    year_df = pd.read_csv(input_path + 'decile_year_matplotlib_' + incomeType + str(year) + '.csv', index_col='State')
    ax.view_init(5,-140)
    #Convert the data to suitable format for the 3D bar chart
    deciles = ['5p','15p','25p','35p','45p','50p','55p','65p','75p','85p','95p']
    label = year_df['Label'].tolist()
    for j in range(len(label)):
      if isinstance(label[j], float): label[j] = ''
      # if year_df.index[j] == 'California': label[j] = 'CA'
      # if year_df.index[j] == 'District of Columbia': label[j] = 'DC'

    ax.clear() #Clear the vis between each frame
    ax.set_zlim(0, 400000) #Set the limit of the z axis
    ax.set_zticklabels([0,50000,100000,150000,200000,250000,300000,350000,400000],fontsize=15)
    #Resize and label the x axis
    ax.set_xticks([j for j in range(len(year_df[pop_label].tolist()))])
    ax.set_xticklabels(label, rotation=-45, fontsize='x-large')
    ax.grid(False)
    #Adjust label in z axis
    ax.tick_params(axis='z', which='major', pad=30)
    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    #Resize and label the y axis
    ax.set_yticks(np.arange(len(deciles)))
    ax.set_yticklabels(['' for year in range(len(deciles))])
    ax.zaxis.set_rotate_label(False)  
    ax.set_zlabel('Annual Household Income (2018$)', rotation = 90, labelpad = 60, fontsize = 20, fontweight = 'bold')
    ax.set_xlabel('Poorer States                             ' + str(year) + '                             Richer States',
                  fontweight = 'bold', labelpad = 30, fontsize = 20)

    #Draw the 3D bar chart 11
    for state in range(year_df.index.size):
      for decile in range(len(deciles)):
        if (highlight != ''):
          if (year_df.iloc[state].name != highlight):
            ax.bar3d(state, decile, 0,
                    year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                    year_df.loc[year_df.iloc[state].name, deciles[decile]],
                    color = '#00C2FB08')
          else:
            ax.bar3d(state, decile, 0,
                    year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                    year_df.loc[year_df.iloc[state].name, deciles[decile]],
                    color = year_df.loc[year_df.iloc[state].name, 'Color'])
        else:
          ax.bar3d(state, decile, 0,
                  year_df.loc[year_df.iloc[state].name, pop_label]*0.025, 1,
                  year_df.loc[year_df.iloc[state].name, deciles[decile]],
                  color = year_df.loc[year_df.iloc[state].name, 'Color'])

  #Animation features: frames - max range for year in animate function; interval - time changing between each frame
  dynamic = animation.FuncAnimation(fig, animate, frames = [year for year in range(year_start - 1, year_end)], interval = 500)
  rc('animation', html = 'jshtml')
  return dynamic

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
