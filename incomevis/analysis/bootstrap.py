import numpy as np, pandas as pd

def bootstrap(self, seed = 0, incomeType = 'RHHINCOME', k = 'decile',
            year = 1977, statefip = 1, n = 1000000,
            output_path = ''):
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
