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
        
def bootstrap_age(raw, n=100, year = 2019, statefip = 1):
    dist_age = pd.DataFrame()
    temp = raw.loc[(raw['YEAR'] == year) & (raw['STATEFIP'] == statefip), :]
    temp = temp.loc[(temp['AGE'] >= 18) & (temp['AGE'] < 80), :]
    temp_uni_age = list(set(temp['AGE']))
    for age in temp_uni_age:
        new_temp_start = temp.loc[(temp['AGE'] == age), :] 
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

def bootstrap_var(raw, seed = 0, incomeType = 'RHHINCOME', statefip=1, n = 100000, year=2019):
    
    np.random.seed(seed)
    year_df = raw[raw['YEAR'] == year]
    update_raw = pd.DataFrame(columns=raw.columns)

    # Resampling n times
    for _ in range(n):
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

        update_raw = pd.concate(update_raw, state_df)
    return update_raw

   