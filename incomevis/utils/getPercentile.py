#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Other Libs
import numpy as np

# Owned
__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def getPercentile(type):
    """
        Return percentile in either string or numeric form.
        Parameters
        ----------
        type: str
            Type of decile. Currently supported ``'string'`` (e.g. ``'5p'``) or
            ``'numeric'`` (e.g. ``0.5``)

        Returns
        -------
        class 'list'
    """
    if type == 'numeric': return np.arange(0.02, 1, 0.01)
    elif type == 'string': return [ '5p', '6p', '7p', '8p', '9p', '10p', '11p', '12p', '13p', '14p',
                                    '15p', '16p', '17p', '18p', '19p', '20p', '21p', '22p', '23p',
                                    '24p', '25p', '26p', '27p', '28p', '29p', '30p', '31p', '32p',
                                    '33p', '34p', '35p', '36p', '37p', '38p', '39p', '40p', '41p',
                                    '42p', '43p', '44p', '45p', '46p', '47p', '48p', '49p', '50p',
                                    '51p', '52p', '53p', '54p', '55p', '56p', '57p', '58p', '59p',
                                    '60p', '61p', '62p', '63p', '64p', '65p', '66p', '67p', '68p',
                                    '69p', '70p', '71p', '72p', '73p', '74p', '75p', '76p', '77p',
                                    '78p', '79p', '80p', '81p', '82p', '83p', '84p', '85p', '86p',
                                    '87p', '88p', '89p', '90p', '91p', '92p', '93p', '94p', '95p']
    else: raise ValueError