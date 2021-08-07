import sys, os
sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
sys.path.append(os.path.join(os.path.dirname("__file__"), '..', '..'))

def get_root_dir():
    dirname = os.getcwd()
    dirname_split = dirname.split("/")
    index = dirname_split.index("incomevis")
    dirname = "/".join(dirname_split[:index + 1])
    return dirname

if 'google.colab' in str(get_ipython()): root = '/content/incomevis'
else: root = get_root_dir()

SOURCE_DATA_PATH    = root + '/data/source_data/'
BENCHMARK_DATA_PATH = root + '/data/benchmark_data/'
DEFLATED_DATA_PATH  = root + '/data/deflated_data/'
OUTPUT_DATA_PATH    = root + '/data/output_data/'
