import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
from incomevis import *
import os.path

# dir_name = os.path.dirname(__file__)
# myIncomevis = incomevis(dir_name + '/data/')
# myIncomevis.adjustIncome()
# order = myIncomevis.getIncomevis(output_path = dir_name + '/data_local/', year_start = 1977, year_end = 1977, returnOrder = True, AmChart=False)
# myIncomevis.getIncomevis(output_path = dir_name + '/data_local/', year_start = 1977, year_end = 2019, AmChart=False)
# plot = getAnimated_abs_rank(incomeType='RPPERHHINCOME', year_start=1977, year_end=2020,
#        input_path= dir_name + '/data_local/',
#        benchmark_path = dir_name + '/data_local/')
# plt.show()

yticks = [0,3,7,10]
ytickslabel = [getDecile('string')[i] for i in yticks]
print(ytickslabel)