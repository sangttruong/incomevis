
incomevis is a visualization toolbox to graphically representing income distribution. It includes incomevis class and several helper functions.

<div id='id-section1'/>
## **incomevis class:**

## Constructor:
    `incomeVis(input_path_ipums, input_path_rpp)`
    * Parameters:
      * `input_path_ipums`: path to IPUMS file. By default, data of ASEC samples from IPUMS-CPS of 1977-2019 sample year with only YEAR, ASECWTH, CPI99, STATEFIP, HHINCOME, PERNUM, and HFLAG variables will be used. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
      * `input_path_rpp`: path to regional price parity deflator file. By default, data from from BEA of 2008-2019 sample year will be use. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
    
2. Methods:
  * `getData()`:
    * Parameters: None
     * Return type: Pandas dataframe 
     * Return value: primary dataframe that is currently in the analysis flow.
  * `getPop()`:
     * Parameters: None
     * Return type: Pandas dataframe
     * Return value: relative population of all states and all years from the input dataset.
  * `getSTATEFIPS()`:
     * Parameters: None
     * Return type: list
     * Return value: a list of STATEFIP as defined by IPUMS-CPS.
  * `adjustIncome()`: adjust HHINCOME with 3 deflators combinations: CPI, CPI-HHSIZE, and CPI-HHSIZE-RPP
     * Parameters: None
     * Return type: Pandas dataframe
     * Return value: primary dataframe that has adjusted HHINCOME
  * `getIncomeVis(self, incomeType = 'RHHINCOME', k = 'decile', year_start = 1977, year_end = 2019, output_path = 'src/output/', toState = False, provide_colorFrame = False, colorFrame = [], returnColor = False, provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False, AmChart = True)`
     * Parameters:
       * incomeType: 
       * k: 
       
     * Return type:
     * Return value:
  * `bootstrap(seed = 0, incomeType = 'RHHINCOME', k = 'decile', year = 1977, statefip = 1, n = 1000000, output_path = 'src/output/bootstrap/')`
  * `bootstrap(seed = 0, incomeType = 'RHHINCOME', k = 'decile', year = 1977, statefip = 1, n = 1000000, output_path = 'src/output/bootstrap/')`
  
<div id='id-section2'/>
## **Helper functions**

1. `getInteractive(k = 'decile', toState = False, outputHTML = False, input_path = 'src/output/decile/year/amchart/js/RHHINCOME1976.js', output_path = 'src/output/decile/year/amchart/html/RHHINCOME1976.html')`
2.  `getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, input_path = 'src/output/decile/year/matplotlib/')`
3.  `KDE(data = pd.read_csv('src/output/bootstrap/decile/xRHHINCOME1977_11_10000.csv'))`
