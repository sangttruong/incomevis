Example and Tutorials
=====================

You can get familiar with the incomevis library by doing the tutorial.

An interative and descriptive noteboook is on `Google Colab <https://colab.research.google.com/drive/1oebYZsoDHM8e0urOedVfjimrjvrxR-nY?usp=sharing>`_.

A interactive website demonstrates library is on `this website <https://research.depauw.edu/econ/incomevis/>`_.

To look up a specific function, see the API documentation.

.. code-block:: python
  :linenos:

  !git clone https://github.com/sangttruong/incomevis.git
  %cd incomevis

  import pandas as pd
  import warnings
  warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
  from incomevis.vis import *
  
  visualize(k = 'decile', year = 2021,
          input_path = '/content/decile_all_year_matplotlib_HHINCOME2020.csv')
