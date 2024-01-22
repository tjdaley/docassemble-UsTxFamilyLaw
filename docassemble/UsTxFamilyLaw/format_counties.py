"""
format_counties.py - format county names for use in docassemble
"""

"""
The original data file is from:

https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-county/exports/json?select=ste_code%2C%20ste_name%2C%20coty_name%2Ccoty_type&limit=-1&timezone=UTC&use_labels=false&epsg=4326

The data is in the public domain.

This data contains the FIPS codes for each state, but not the state two-letter codes.

STATE_CODES was created by hand from the data at:

https://www.bls.gov/respondents/mwr/electronic-data-interchange/appendix-d-usps-state-abbreviations-and-fips-codes.htm
"""

import json

INPUT_FILE =  r'C:\Users\tdale\Documents\Local Projects\docassemble-UsTxFamilyLaw\docassemble\UsTxFamilyLaw\data\georef-united-states-of-america-county (2).json'
OUTPUT_FILE = r'C:\Users\tdale\Documents\Local Projects\docassemble-UsTxFamilyLaw\docassemble\UsTxFamilyLaw\data\us_counties.json'

STATE_CODES = {
    "01": "AL","02": "AK","04": "AZ","05": "AR","06": "CA","08": "CO","09": "CT","10": "DE",
    "11": "DC","12": "FL","13": "GA","15": "HI","16": "ID","17": "IL","18": "IN","19": "IA",
    "20": "KS","21": "KY","22": "LA","23": "ME","24": "MD","25": "MA","26": "MI","27": "MN",
    "28": "MS","29": "MO","30": "MT","31": "NE","32": "NV","33": "NH","34": "NJ","35": "NM",
    "36": "NY","37": "NC","38": "ND","39": "OH","40": "OK","41": "OR","42": "PA","72": "PR",
    "44": "RI","45": "SC","46": "SD","47": "TN","48": "TX","49": "UT","50": "VT","51": "VA",
    "78": "VI","53": "WA","54": "WV","55": "WI","56": "WY",
}

json_data = open(INPUT_FILE).read()
data = json.loads(json_data)

counties_by_state = {}
for county in data:
    fips_code = county['ste_code'][0]
    state_code = STATE_CODES.get(fips_code)
    if not state_code:
        continue
    county_name = county['coty_name'][0]
    county_type = county.get('coty_type', 'county') or 'county'
    county_type = county_type[0].upper() + county_type[1:]
    if state_code not in counties_by_state:
        counties_by_state[state_code] = []
    counties_by_state[state_code].append(f"{county_name} {county_type}")

with open(OUTPUT_FILE, 'w') as output:
    output.write(json.dumps(counties_by_state, indent=4))
