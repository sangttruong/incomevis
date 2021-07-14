from incomevis import *
import os.path

dir_name = os.path.dirname(__file__)
print(dir_name)
myIncomevis = incomevis(dir_name + '/data/')
myIncomevis.adjustIncome()