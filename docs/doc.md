The IncomeVis library includes incomevis class and several helper functions.

**IncomeVis class:**
1. Constructor: `IncomeVis(input_path_ipums, input_path_rpp)`
  * `input_path_ipums`: path to IPUMS file. `CSV` format required. 
  * `input_path_rpp`: path to RPP file. `CSV` format required.

2. Methods:
  * `getData()`: return the IPUMS-RPP data. 
  * `getPop()`: return a population Dataframe (all states, all year) in the input dataset.
  * `getSTATEFIPS()`: return a list of STATEFIP code.
  * `adjustIncome()`: adjust HHINCOME with 3 deflators: CPI, effective HHSIZE, RPP.
  * `getIncomeVis(incomeType = 'RHHINCOME', k = 'decile', year_start = 1977, year_end = 2019, output_path = '', suppress_sort50p = True, toState = False, provide_colorFrame = False, colorFrame = pd.DataFrame(), returnColor = False, AmChart = True)`
  * `bootstrap(seed = 0, incomeType = 'RHHINCOME', k = 'decile', year = 2018, statefip = 1, n = 1000000, output_path = '')`
  * `KDE(self, variable=0, lags=40, fig=None, figsize=(15,7), savefig = False, title = None, path = None)`

**Helper functions**
1. `getInteractive(k = 'decile', toState = False, outputHTML = False, input_path = 'output/decile/Year/AmChart/JS/YEAR1976_HHINCOME.js', output_path = 'gdrive/My Drive/Colab Notebooks/USIncomeVis/output/decile/Year/AmChart/HTML/YEAR1976_HHINCOME.html')`
2. `getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, input_path = 'output/decile/Year/Matplotlib/')`
