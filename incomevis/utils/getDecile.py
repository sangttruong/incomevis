#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sang T. Truong"
__copyright__ = "Copyright 2021, The incomevis project"
__credits__ = ["Sang T. Truong"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Sang T. Truong"
__email__ = "sttruong@cs.stanford.edu"
__status__ = "Dev"

def getDecile(type):
    """
    Return decile in either string or numeric form
    """
    if type == 'numeric': return [0.05, 0.15, 0.25, 0.35, 0.45, 0.50, 0.55, 0.65, 0.75, 0.85, 0.95]
    elif type == 'string': return ['5p','15p','25p','35p','45p','50p','55p','65p','75p','85p','95p']
    else: raise ValueError