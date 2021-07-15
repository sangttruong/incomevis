def nation(self, incomeType='RPPERHHINCOME', k='decile', year=2019, output_path=''):
    # Adjustable variable
    year_df = self.raw[self.raw['YEAR'] == year]

    # Generate result grid, decile-column
    if k == 'decile':
        result = pd.DataFrame(index = incomevis.utils.getDecile(), columns = ['nation'])
    if k == 'percentile':
        result = pd.DataFrame(index =  incomevis.utils.getPercentile(), columns = ['nation'])

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
