def uni_sample(n=100, year_start=1977, year_end=2019):
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
                dist_age = pd.concat([dist_age, temp_dist_age])
            dist_age.reset_index(inplace=True, drop=True)
    return dist_age
