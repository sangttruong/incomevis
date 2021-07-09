import pandas as pd
import numpy as np
from incomevis import incomevis

class gather_absolute_ranking:
    def __init__(self, input_path_ipums, input_path_rpp):
        iv = incomevis(input_path_ipums = input_path_ipums, input_path_rpp = input_path_rpp)
        self.raw = iv.adjustIncome()
        self.statefip = list(set(self.raw['STATEFIP']))
        self.pop = iv.getPop()
        
    def uni_sample(self, n=100, year_start=1977, year_end=2019):
        dist_age = pd.DataFrame()
        for year in range(year_start, year_end+1):
            temp = self.raw.loc[(self.raw['YEAR'] == year), :]
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

        state_name = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                    'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
                    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
                    'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                    'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

        state_name = pd.DataFrame(data = state_name, index = self.statefip, columns = ['State'])

        for year in range(year_start, year_end+1):
            year_df = sub_raw[sub_raw['YEAR'] == year] # Generate year_df dataframe

            if k == 'decile':
                # Generate result grid, decile-column
                decile_column = ['5p', '15p', '25p', '35p', '45p', '50p', '55p', '65p', '75p', '85p', '95p']
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
                percentile_column = ['2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p',
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

    def nation(self, incomeType='RPPERHHINCOME', k='decile', year=2019, output_path=''):
        # Adjustable variable
        year_df = self.raw[self.raw['YEAR'] == year] 

        # Generate result grid, decile-column
        if k == 'decile':
            result = pd.DataFrame(index = ['5p', '15p', '25p', '35p', '45p', '50p', '55p', '65p', '75p', '85p', '95p'], columns = ['nation'])
        if k == 'percentile':
            result = pd.DataFrame(index =  ['2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p',
                                    '12p', '13p', '14p', '15p', '16p', '17p', '18p', '19p', '20p',
                                    '21p', '22p', '23p', '24p', '25p', '26p', '27p', '28p', '29p',
                                    '30p', '31p', '32p', '33p', '34p', '35p', '36p', '37p', '38p',
                                    '39p', '40p', '41p', '42p', '43p', '44p', '45p', '46p', '47p',
                                    '48p', '49p', '50p', '51p', '52p', '53p', '54p', '55p', '56p',
                                    '57p', '58p', '59p', '60p', '61p', '62p', '63p', '64p', '65p',
                                    '66p', '67p', '68p', '69p', '70p', '71p', '72p', '73p', '74p',
                                    '75p', '76p', '77p', '78p', '79p', '80p', '81p', '82p', '83p',
                                    '84p', '85p', '86p', '87p', '88p', '89p', '90p', '91p', '92p',
                                    '93p', '94p', '95p', '96p', '97p', '98p', '99p'], columns = ['nation'])

        # Iterate through each state
        c = 0
        # for statefip in self.__statefips:
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