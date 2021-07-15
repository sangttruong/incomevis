import pandas as pd
import numpy as np
from incomevis.processing import *
from incomevis.utils import *

def age_sample_incomevis(self, dist_age, year_start=1977, year_end=2019, incomeType='RPPERHHINCOME', k = 'decile',
                        subpop = False, black = None, hispan = None, sex = None, educ = None,
                        output_path=''):
    sub_raw = dist_age
    if subpop:
        if black is not None:
            if black == True:
                sub_raw = sub_raw.loc[(sub_raw['RACE'] == 200) | (sub_raw['RACE'] == 801) | (sub_raw['RACE'] == 805) | (sub_raw['RACE'] == 806) |
                                    (sub_raw['RACE'] == 807) | (sub_raw['RACE'] == 810) | (sub_raw['RACE'] == 811) |
                                    (sub_raw['RACE'] == 814) | (sub_raw['RACE'] == 816) | (sub_raw['RACE'] == 818), :]
            if black == False:
                sub_raw = sub_raw.loc[(sub_raw['RACE'] != 200) & (sub_raw['RACE'] != 801) & (sub_raw['RACE'] != 805) & (sub_raw['RACE'] != 806) &
                                    (sub_raw['RACE'] != 807) & (sub_raw['RACE'] != 810) & (sub_raw['RACE'] != 811) &
                                    (sub_raw['RACE'] != 814) & (sub_raw['RACE'] != 816) & (sub_raw['RACE'] != 818), :]         
        if hispan is not None:
            if hispan == True:
                sub_raw = sub_raw.loc[(sub_raw['HISPAN'] > 0) & (sub_raw['HISPAN'] < 900), :]
            if hispan == False:
                sub_raw = sub_raw.loc[sub_raw['HISPAN'] == 0, :]
        if sex is not None:
            if sex == True:
                sub_raw = sub_raw.loc[sub_raw['SEX'] == 1, :]
            if sex == False:
                sub_raw = sub_raw.loc[sub_raw['SEX'] == 2, :]
        if educ is not None:
            if educ == True:
                sub_raw = sub_raw.loc[(sub_raw['EDUC'] > 73) & (sub_raw['EDUC'] < 999), :]
            if educ == False:
                sub_raw = sub_raw.loc[(sub_raw['EDUC'] > 2) & (sub_raw['EDUC'] <= 73), :]

    state_name = incomevis.Utils.getStateName()
    state_name = pd.DataFrame(data = state_name, index = self.statefip, columns = ['State'])

    for year in range(year_start, year_end+1):
        year_df = sub_raw[sub_raw['YEAR'] == year] # Generate year_df dataframe

        if k == 'decile':
            # Generate result grid, decile-column
            decile_column = incomevis.Utils.getDecile()
            result = pd.DataFrame(index = decile_column, columns=self.statefip)

            # Iterate through each state
            c = 0
            for state in self.statefip:
                state_df = year_df[year_df['STATEFIP'] == state] # Generate state dataframe
                state_df = state_df.reset_index(drop = True)
                state_df = state_df.sort_values(incomeType) # Sort state dataframe by RHHINCOME
                state_df['CUMWTH'] = state_df['ASECWTH'].cumsum() # Calculate cumulated weight and Percentage
                state_df['PERCENTH'] = state_df['CUMWTH']/(state_df['ASECWTH'].sum())

                # Calculate decile
                r = 0
                for kile in [0.05, 0.15, 0.25, 0.35, 0.45, 0.5, 0.55, 0.65, 0.75, 0.85, 0.95]:
                    result.iloc[r,c] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
                    r = r + 1
                c = c + 1

            # Transpose result table: column-decile
            result = result.T
            result = pd.concat([state_name, result], axis = 1)
            sorted_result = result.sort_values(by = ['50p'], ascending = True)
            orderFrame = sorted_result.index
            result = pd.merge(result, self.pop['UR_NORMPOP_' + str(year)], left_index = True, right_index = True)
            result = result.reindex(index = orderFrame)
            result.to_csv(output_path+ k +'_year_matplotlib_' + incomeType + '' + str(year-1) + '.csv', index=False)
            
        if k == 'percentile':
            # Generate result grid, percentile-column
            percentile_column = incomevis.Utils.getPercentile()
            result = pd.DataFrame(index = percentile_column, columns=self.statefip)

            # Iterate through each state
            c = 0
            for state in self.statefip:
                state_df = year_df[year_df['STATEFIP'] == state] # Generate state dataframe
                state_df = state_df.reset_index(drop = True)
                state_df = state_df.sort_values(incomeType) # Sort state dataframe by RHHINCOME
                state_df['CUMWTH'] = state_df['ASECWTH'].cumsum() # Calculate cumulated weight and Percentage
                state_df['PERCENTH'] = state_df['CUMWTH']/(state_df['ASECWTH'].sum())

                # Calculate decile
                r = 0
                for kile in np.arange(0.02, 1, 0.01):
                    result.iloc[r,c] = state_df.loc[state_df['PERCENTH'] <= kile, incomeType].max()
                    r = r + 1
                c = c + 1

            # Transpose result table: column-decile
            result = result.T
            result = pd.concat([state_name, result], axis = 1)
            sorted_result = result.sort_values(by = ['50p'], ascending = True)
            orderFrame = sorted_result.index
            result = pd.merge(result, self.pop['UR_NORMPOP_' + str(year)], left_index = True, right_index = True)
            result = result.reindex(index = orderFrame)
            # To_csv
            result.to_csv(output_path+ k +'_year_matplotlib_' + incomeType + '' + str(year-1) + '.csv', index=False)