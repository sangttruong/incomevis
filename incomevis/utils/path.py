import sys, os
sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
sys.path.append(os.path.join(os.path.dirname("__file__"), '..', '..'))

if 'google.colab' in str(get_ipython()):
    SOURCE_DATA_PATH = '/content/incomevis/data/'
    BENCHMARK_PATH = ''
    DATA_PATH =
else:
    SOURCE_DATA_PATH =
    BENCHMARK_PATH =
    DATA_PATH =
    
