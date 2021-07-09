import pandas as pd
import numpy as np
from incomevis import incomevis

import utils 

utils.features()

# class gather_absolute_ranking:
#     def __init__(self, input_path_ipums, input_path_rpp):
#         iv = incomevis(input_path_ipums = input_path_ipums, input_path_rpp = input_path_rpp)
#         raw = iv.adjustIncome()
#         statefip = list(set(raw['STATEFIP']))
#         pop = iv.getPop()
        
def bootstrap_age(raw, n=100, year_start=1977, year_end=2019):
    dist_age = pd.DataFrame()
    for year in range(year_start, year_end+1):
        temp = raw.loc[(raw['YEAR'] == year), :]
        temp = temp.loc[(temp['AGE'] >= 18) & (temp['AGE'] < 80), :]
        temp_uni_age = list(set(temp['AGE']))
        temp_statefip = list(set(temp['STATEFIP']))
        for state in temp_statefip:
            for age in temp_uni_age:
                new_temp_start = temp.loc[(temp['AGE'] == age) & (temp['STATEFIP'] == state), :] 
                temp_dist_age = pd.DataFrame()
                while(len(temp_dist_age) < n):
                    try:
                        new_temp = new_temp_start.sample(n=n, replace=True)
                        temp_dist_age = pd.concat([temp_dist_age, new_temp])
                    except:
                        break
                # print(str(age) + ' Finished')
                dist_age = pd.concat([dist_age, temp_dist_age])
            dist_age.reset_index(inplace=True, drop=True)
    return dist_age

def bootstrap_var(raw, seed = 0, incomeType = 'RHHINCOME', k = 'decile',
            year = 1977, statefip = 1, n = 1000000,
            output_path = ''):
    np.random.seed(seed)
    year_df = raw[raw['YEAR'] == year]

    # Decile or percentile
    if (k == 'decile'):
        kiles = np.arange(0.05, 1.05, 0.1)
        kNames = utils.decile
    elif (k == 'percentile'):
        kiles = np.arange(0.02, 1, 0.01)
        kNames = utils.percentile
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

def getIncomevis_nation(raw, incomeType='RPPERHHINCOME', k='decile', year=2019, output_path=''):
    # Adjustable variable
    year_df = raw[raw['YEAR'] == year] 

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