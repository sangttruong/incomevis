Constructor
===========

.. py:class:: incomevis(input_path_ipums = '', input_path_rpp = '')

   :param input_path_ipums: path to IPUMS file. By default, data of ASEC samples from IPUMS-CPS of 1977-2019 sample year with only YEAR, ASECWTH, CPI99, STATEFIP, HHINCOME, PERNUM, and HFLAG variables will be used. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).
   :param input_path_rpp: path to regional price parity deflator file. By default, data from from BEA of 2008-2019 sample year will be use. Input data type needs to be readable to Pandas read_csv() function (e.g. csv or zip).