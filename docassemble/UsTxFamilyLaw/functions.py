"""
functions.py - functions for use in docassemble
"""
from docassemble.UsTxFamilyLaw.courts import TexasJPCourts, TexasDistrictCourts, TexasDistrictClerks, TexasCountyCourtsAtLaw
from docassemble.base.util import DAObject, DAList
from docassemble.base.functions import user_info, write_record, read_records, delete_record

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

DB_DATAKEYS = ['cases', 'subpoenas', 'witnesses']

def user_db_object_key(user_privs:list, user_id:str, datakey:str) -> str:
    """
    Return the applicable key for looking up objects in the database. The
    key is either the user's first firm privilege (for firm-wide searches) or
    the user's id if the user does not have a firm privilege.

    :param user_privs: List of privileges for this user
    :type user_privs: list[str]
    :param user_id:str: User's id property
    :type user_id: str
    :param datakey: Key indicating what type of objects will be retrieved
    :type datakey: str
    :rtype: str

    Throws ValueError exception if datakey is not in the allowed list of values.
    """
    lower_datakey = datakey.lower()
    if lower_datakey not in DB_DATAKEYS:
        raise ValueError(f"datakey '{datakey}' not found in allowed list: {', '.join(DB_DATAKEYS)}")

    if not user_id:
        raise ValueError("Invalid 'user_id' parameter value. Use 'user_info().id' to get the correct value")

    if not user_privs:
        raise ValueError("Invalid 'privs' parameter value. Use 'user_privileges()' to get the correct value")

    user_key = next((priv for priv in user_privs), None) or str(user_id)
    db_key = f'{user_key}::{lower_datakey}'
    return db_key

def db_object_key(datakey:str) -> str:
    """
    Return the applicable key for looking up objects in the database.

    :param datakey: Index into DB_DATAKEYS indicating which type of object to retrieve
    :type datakey: str

    Throws ValueError exception if datakey not in the allowed list of values.
    """
    the_user_info = user_info()
    user_privs = the_user_info.privileges
    user_id = the_user_info.id
    db_key = user_db_object_key(user_privs, user_id, datakey)

def validate_case(case: DAObject) -> bool:
    """
    Verify that a case has the minimal information that we need.
    
    Returns:
        True if case passed validations. Otherwise an exception is thrown.

    Throws:
      ValueError: If the case is missing a required property

    :param case: The case to validate
    :type case: DAObject
    :rtype: bool
    """
    
    if case.id is None:
        raise ValueError('Case must have an "id" property, which is the cause number.')

    if case.county is None:
        raise ValueError('Case must have a "county" property, which is the county in which the case is pending.')

    if case.us_state is None:
        case.us_state = 'TX'

    return True

def find_case_id(db_key: str, case: DAObject) -> str:
    """
    Returns the ID of a case. This is the docassemble internal database id assigned when the case was saved.

    Returns:
      ID of the case, if found, otherwise None

    Throws:
      Any excpetion thrown by validate_case()
    """
    if not validate_case(case):
        return None

    saved_cases = read_records(db_key)
    for id in saved_cases:
        saved_case = saved_cases[id]
        if cases_match(case, saved_case):
            return id
    return None

def cases_match(case1, case2) -> bool:
    """
    Compare two case objects to see if they match.
    """
    if case1.id != case2.id:
        return False

    if case1.county != case2.county:
        return False

    if (case1.us_state or 'TX') != (case2.us_state or 'TX'):
        return False

    return True

def get_cases() -> DAList:
    """
    Returns a list of cases for this user or firm.
    
    TODO: Filter by "is_hidden".
    TODO: Sort by Client Name + Cause Number

    :rtype: DAList
    """
    db_key = db_object_key('cases')
    return read_records(db_key)

def get_case(id) -> DAObject:
    """
    Return one case identified by the given id.
    """
    cases = get_cases()
    for case_id in cases:
        the_case = cases[case_id]
        if id == case_id:
            return the_case

def case_choices() -> list:
    """
    Returns a list suitable for use as choices in a dropdown.
    """
    cases = get_cases()
    choices = []
    for case_id in cases:
        the_case = cases[case_id]
        choice = {
            the_case: case.client,
            'help': f"{case.county} Cause #{case.id} - {case.petitioner} v. {case.respondent}"
        }
        choices.append(choice)
    return choices
    
def save_case(case: DAObject):
    """
    Saves a case. Wrapper for update_case().

    Returns:
      DB ID of the newly saved case record.

    Throws:
      Any excpetion thrown by validate_case()
    """
    return update_case(case)

def delete_case(case: DAObject):
    """
    Deletes a case from the DB.

    :param case: The case to delete
    :type case: DAObject
    :rtype: bool as to whether case was actually deleted
    """
    
    if not validate_case(case):
        return False

    db_key = db_object_key('cases')
    case_id = find_case_id(db_key, case)
    if case_id:
        delete_record(db_key, case_id)
        return True
    return False

def update_case(case: DAObject):
    """
    Update a case in the database. First, delete any existing case record that matches this case.
    Then save the case to the database.

    Returns:
      newly created database Id or None if not successful
    """
    if not validate_case(case):
        return None

    # Delete the existing case recrod, if any
    delete_case(case)
    
    # Save case information
    db_key = db_object_key('cases')
    new_case_id = write_record(db_key, case)
    return new_case_id

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
