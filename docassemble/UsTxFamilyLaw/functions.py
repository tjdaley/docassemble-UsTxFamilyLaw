"""
functions.py - functions for use in docassemble
"""
from docassemble.UsTxFamilyLaw.courts import TexasJPCourts, TexasDistrictCourts, TexasDistrictClerks, TexasCountyCourtsAtLaw
from docassemble.base.util import DAObject

JPCOURTS = TexasJPCourts()
DISTRICTCOURTS = TexasDistrictCourts()
DISTRICTCLERKS = TexasDistrictClerks()
COUNTY_COURTS_AT_LAW = TexasCountyCourtsAtLaw()

ALIGNMENTS = {
    'Petitioner': 'Petitioner',
    'Respondent': 'Respondent',
    'Intervenor': 'Intervenor',
    'Third Party': 'Third Party'
}

def jp_court_choices_for_county(county_name:str, refresh:bool = False) ->list:
    """
    Return a list of justice of the peace courts for the given county.
    This will be a list suitable for use in a dropdown.

    :param county_name: The name of the county.
    :type county_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: list
    """
    return sorted(JPCOURTS.get_courts_dropdown_for_county(county_name, refresh))

def jp_court_for_county(county_name:str, court_name:str, refresh:bool = False) -> DAObject:
    """
    Return a given justice of the peace court for the given county.

    :param county_name: The name of the county.
    :type county_name: str
    :param court_name: The name of the court.
    :type court_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: dict
    """
    return JPCOURTS.get_court(county_name, court_name, refresh)

def district_court_choices_for_county(county_name:str, refresh:bool = False) ->list:
    """
    Return a list of district courts for the given county.
    This will be a list suitable for use in a dropdown.

    :param county_name: The name of the county.
    :type county_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: list
    """
    return sorted(DISTRICTCOURTS.get_courts_dropdown_for_county(county_name, refresh))

def district_court_for_county(county_name:str, court_name:str, refresh:bool = False) -> DAObject:
    """
    Return a given district court for the given county.

    :param county_name: The name of the county.
    :type county_name: str
    :param court_name: The name of the court.
    :type court_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: dict
    """
    return DISTRICTCOURTS.get_court(county_name, court_name, refresh)

def county_court_at_law_choices_for_county(county_name:str, refresh:bool = False) ->list:
    """
    Return a list of county courts at law for the given county.
    This will be a list suitable for use in a dropdown.

    :param county_name: The name of the county.
    :type county_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: list
    """
    return sorted(COUNTY_COURTS_AT_LAW.get_courts_dropdown_for_county(county_name, refresh))

def county_court_at_law_for_county(county_name:str, court_name:str, refresh:bool = False) -> DAObject:
    """
    Return a given county court at law for the given county.

    :param county_name: The name of the county.
    :type county_name: str
    :param court_name: The name of the court.
    :type court_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: dict
    """
    return COUNTY_COURTS_AT_LAW.get_court(county_name, court_name, refresh)

def district_clerk_for_county(county_name:str, refresh:bool = False) -> DAObject:
    """
    Return a given district clerk for the given county.

    :param county_name: The name of the county.
    :type county_name: str
    :param court_name: The name of the court.
    :type court_name: str
    :param refresh: Whether to refresh the cache. (default: False)
    :type refresh: bool
    :rtype: dict
    """
    return DISTRICTCLERKS.get_clerk(county_name, refresh)

def nested_attr(obj, attr:str, default=None):
    """
    Return the value of a nested attribute.

    :param obj: The object to search.
    :type obj: object
    :param attr: The attribute to search for.
    :type attr: str
    :param default: The default value to return if the attribute is not found.
    :rtype: object
    """
    try:
        for a in attr.split('.'):
            obj = getattr(obj, a)
        return obj
    except AttributeError:
        return default

def us_counties(filter_state) ->list:
    """
    Return a dict of counties for the given state.

    :param state: The two-letter state code.
    :type state: str
    :rtype: dict
    """

    import os

    data_file = os.path.join(os.path.dirname(__file__), 'data', 'unique_county_state_list.csv')
    with open(data_file) as f:
        # read the file into a list of lines
        lines = f.readlines()
    counties = {}
    for i, line in enumerate(lines):
        # remove the newline character from each line
        clean_line = line.strip()
        county, us_state = clean_line.split('|')
        if filter_state == us_state:
            counties[county] = county
    return counties

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

def unsecured_debt_types() ->dict:
    """
    Return a dict of unsecured debt types.

    :rtype: dict
    """
    return __sorted_dict({
        'credit_card': 'Credit Card',
        'medical': 'Medical',
        'personal_loan': 'Personal Loan',
        'student_loan': 'Student Loan',
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
