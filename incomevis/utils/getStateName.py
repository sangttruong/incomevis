def getStateName(type):
    """
    Return state in either string or numeric form
    """
    if type == 'string': return ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                                'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
                                'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
                                'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                                'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                                'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                                'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                                'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                                'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    elif type == 'numeric': return [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20,
                                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                                     37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
    else: raise ValueError
