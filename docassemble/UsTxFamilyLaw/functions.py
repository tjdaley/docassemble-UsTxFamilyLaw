"""
functions.py - functions for use in docassemble
"""
ALIGNMENTS = ({
    'p': 'Petitioner',
    'r': 'Respondent',
    'i': 'Intervenor',
    't': 'Third Party'
})

def us_counties(state) ->dict:
    """
    Return a dict of counties for the given state.

    :param state: The two-letter state code.
    :type state: str
    :rtype: dict
    """

    import json
    import os

    data_file = os.path.join(os.path.dirname(__file__), 'data', 'us_counties.json')
    with open(data_file) as f:
        counties_by_state = json.load(f)

    counties = counties_by_state.get(state.upper(), [])
    county_dict = {x: x for x in counties}
    return county_dict

def alignment_list() ->dict:
    """
    Return a dict of alignment options.

    :rtype: dict
    """
    return __sorted_dict(ALIGNMENTS)

def translate_alignment(align:str) ->str:
    """
    Return the full name of an alignment.

    :param align: The alignment code from the ALIGNMENTS dict.
    :type align: str
    :rtype: str
    """
    return ALIGNMENTS.get(align, 'Unknown')

def bank_account_types() ->dict:
    """
    Return a dict of bank account types.

    :rtype: dict
    """
    return __sorted_dict({
        'checking': 'Checking',
        'savings': 'Savings',
        'money_market': 'Money Market',
        'cd': 'Certificate of Deposit',
        'other': 'Other',
    })

def retirement_account_types() ->dict:
    """
    Return a dict of retirement account types.

    :rtype: dict
    """
    return __sorted_dict({
        '401k': '401(k)',
        '403b': '403(b)',
        'ira': 'IRA',
        'keogh': 'Keogh',
        'pension': 'Pension',
        'profit_sharing': 'Profit Sharing',
        'roth': 'Roth IRA',
        'sep': 'SEP IRA',
        'teacher': 'Teacher Retirement System',
        'ers': 'ERS',
        'jrs': 'JRS II',
        'lecos': 'LECOS',
        'tcdrs': 'TCDRS',
        'tesrs': 'TESRS',
        'tmrs': 'TMRS',
        'tsa': 'TSA',
        'other': 'Other',
    })

def aircraft_types() ->dict:
    """
    Return a dict of aircraft types.

    :rtype: dict
    """
    return __sorted_dict({
        'airplane': 'Airplane',
        'helicopter': 'Helicopter',
        'glider': 'Glider',
        'ultralight': 'Ultralight',
        'balloon': 'Balloon',
        'other': 'Other',
    })

def watercraft_types() ->dict:
    """
    Return a dict of watercraft types.

    :rtype: dict
    """
    return __sorted_dict({
        'sailboat': 'Sailboat',
        'powerboat': 'Powerboat',
        'jet_ski': 'Jet Ski',
        'canoe': 'Canoe',
        'kayak': 'Kayak',
        'paddleboard': 'Paddleboard',
        'yacht': 'Yacht',
        'other': 'Other',
    })

def __sorted_dict(d:dict) -> dict:
    """
    Return a dict sorted by key.

    :param d: The dict to sort.
    :type d: dict
    :rtype: dict
    """
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}
