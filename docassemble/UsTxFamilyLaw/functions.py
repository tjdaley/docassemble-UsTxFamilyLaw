"""
functions.py - functions for use in docassemble
"""

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
