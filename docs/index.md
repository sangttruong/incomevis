incomevis is a visualization toolbox to graphically representing income distribution. It includes incomevis class and several helper functions.

<div id='id-section1'/>
# **incomevis class**

## Constructor
`incomeVis(input_path_ipums, input_path_rpp)`
* Parameters:
    * `input_path_ipums`: path to IPUMS file. By default, data of ASEC samples from IPUMS-CPS of 1977-2019 sample year with only YEAR, ASECWTH, CPI99, STATEFIP, HHINCOME, PERNUM, and HFLAG variables will be used. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
    * `input_path_rpp`: path to regional price parity deflator file. By default, data from from BEA of 2008-2019 sample year will be use. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
    
## Methods

### `getData()`
* Parameters: None
* Return type: Pandas dataframe 
* Return value: primary dataframe that is currently in the analysis flow.
     
### `getPop()`
* Parameters: None
* Return type: Pandas dataframe
* Return value: relative population of all states and all years from the input dataset.

### `getSTATEFIPS()`
* Parameters: None
* Return type: list
* Return value: a list of STATEFIP as defined by IPUMS-CPS
     
### `adjustIncome()`
* Parameters: None
* Return type: Pandas dataframe
* Return value: primary dataframe that has adjusted HHINCOME based on 3 deflators combinations: CPI, CPI-HHSIZE, and CPI-HHSIZE-RPP
     
### `getIncomevis(self, incomeType = 'RHHINCOME', k = 'decile', year_start = 1977, year_end = 2019, output_path = 'package/directory', toState = False, provide_colorFrame = False, colorFrame = [], returnColor = False, provide_orderFrame = False, orderFrame = pd.DataFrame(), returnOrder = False, AmChart = True)`
* Parameters:
    * incomeType: income type. By default, there is 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
    * k: segmentation level, which can either be 'decile' or 'percentile'
    * year_start: Analysis starting year
    * year_end: Analysis ending year, which also be included
    * output_path: output path. We highly recommend the users to specify their own output path to avoid missing file or confusion
    * toState: if true will also return a set of state graph with the respective year ranges
    * provide_colorFrame: if colorframe will be provided or not
    * colorFrame: color list, which will be ignored if provide_colorFrame is set to False
    * returnColor: if the colorframe is returned or not
    * provide_orderFrame: if the orderframe will be provided or not
    * orderFrame: orderframe, which will be ignored if provide_orderFrame is set to False
    * returnOrder: if the orderframe is returned or not
    * AmChart: library that will be used for rendering the visualization. If False, Matplotlib will be used.
* Return type: None
* Return value: None

### `bootstrap(seed = 0, incomeType = 'RHHINCOME', k = 'decile', year = 1977, statefip = 1, n = 1000000, output_path = 'package/directory')`
* Parameters:
    * seed: seed of the uniform random sampling
    * incomeType: income type. By default, there is 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
    * k: segmentation level, which can either be 'decile' or 'percentile'
    * year: bootstrapping year
    * statefip: bootstrapping state
    * n: number of iteration
    * output_path: output path. We highly recommend the users to specify their own output path to avoid missing file or confusion
* Return type: Pandas dataframe
* Return value: bootstrapting result

<div id='id-section2'/>
# **Helper functions**

### `getInteractive(k = 'decile', toState = False, outputHTML = False, input_path = 'package/directory/' + 'RHHINCOME1976.js', output_path = 'package/directory/' + 'RHHINCOME1976.html')`
* Parameters:
    * k: segmentation level, which can either be 'decile' or 'percentile'
    * toState = if true will display state graph instead of year graph
    * outputHTML = if true will output an HTML file in the specified output path
    * input_path = input path of the file that needs to be displayed
    * output_path = input path of the HTML file that will be printed out
* Return type: IPython.display.HTML object
* Return value: Interactive graph

### `getAnimated(incomeType = 'RHHINCOME', year_start = 1977, year_end = 2019, highlight = '', input_path = 'package/directory/')`
* Parameters:
    * incomeType: income type. By default, there is 5 options: 'HHINCOME', 'RHHINCOME', 'ERHHINCOME', 'RPPRHHINCOME', 'RPPERHHINCOME'
    * year_start: Analysis starting year
    * year_end: Analysis ending year, which also be included
    * highlight: Full name (not STATEFIP) of state that will be highlighted.
    * input_path = input directory of all files that will be animated
* Return type: matplotlib.animation.FuncAnimation object
* Return value: animated graph

### `KDE(data = pd.read_csv('package/directory/' + 'xRHHINCOME1977_11_10000.csv'))`
* Parameters:
   * data: data () that will be compared to the normal distribution
* Return type: matplotlib.pyplot.figure object
* Return value: Kernel density estimation of the input data
