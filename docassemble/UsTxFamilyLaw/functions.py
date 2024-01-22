"""
functions.py - functions for use in docassemble
"""

def us_counties(state):
    """
    Get a list of counties for the given state.

    :param state: The two-letter state code.
    :type state: str
    :rtype: list
    """

    import json
    import os

    data_file = os.path.join(os.path.dirname(__file__), 'data', 'us_counties.json')
    with open(data_file) as f:
        counties_by_state = json.load(f)
    return counties_by_state.get(state.upper(), [])
