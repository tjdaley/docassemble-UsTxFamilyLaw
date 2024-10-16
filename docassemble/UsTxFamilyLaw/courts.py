"""
courts.py - Classes and methods for retrieving court information.
"""

import pandas as pd
import requests
from io import StringIO
import os
import json

from docassemble.base.util import DAFile

__all__ = [
    'TexasJPCourts'
]

class TexasJPCourts:
    def __init__(self, cache_file='jp_courts_cache.json'):
        self.url = 'https://card.txcourts.gov/ExcelExportPublic.aspx?type=C&export=E&SortBy=tblCounty.Sort_ID,%20tblCourt.Court_Identifier&Active_Flg=true&Court_Type_CD=56&Court_Sub_Type_CD=0&County_ID=0&City_CD=0&Court=&DistrictPrimaryLocOnly=0&AdminJudicialRegion=0&COADistrictId=0'
        self.cache_file = cache_file
        self.courts_data = None

    def _download_data(self):
        """Downloads the data from the URL and converts it to a pandas DataFrame"""
        response = requests.get(self.url)
        response.raise_for_status()  # Check if the request was successful

        # Read tab-delimited data into pandas DataFrame
        data = StringIO(response.text)
        df = pd.read_csv(data, delimiter='\t')
        return df

    def _load_cache(self):
        """Loads the data from the cache file if it exists"""
        da_cache_file = DAFile('jp_court_cache')
        da_cache_file.initialize(filename=self.cache_file, mimetype='application/json')
        if os.path.exists(da_cache_file.path()):
            with open(da_cache_file.path(), 'r', encoding='utf-8') as f:
                self.courts_data = json.load(f)
            return True
        return False

    def _save_cache(self, data):
        """Saves the data to the cache file"""
        da_cache_file = DAFile('jp_court_cache')
        da_cache_file.initialize(filename=self.cache_file, mimetype='application/json')
        with open(da_cache_file.path(), 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def _transform_data(self, df):
        """Transforms the DataFrame into the desired dictionary format"""
        courts_dict = {}
        for _, row in df.iterrows():
            county = f"{row['County']} County"
            record = {
                'Court': self._rename_court(row['Court']),
                'Court Type': row['Court Type'],
                'Website': row['Website'],
                'Address': row['Address'],
                'City': row['City'],
                'Zip Code': row['Zip Code'],
                'Phone': row['Phone'],
                'Email': row['Email']
            }
            if record['Court'] == "(do not use)":
                continue
            if county not in courts_dict:
                courts_dict[county] = []
            courts_dict[county].append(record)
        return courts_dict
    
    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        if court_name.lower().startswith('jail'):
            return "(do not use)"
        if court_name.lower().startswith('truancy'):
            return "(do not use)"
        return court_name
    
    def _refresh_cache(self):
        """Refreshes the cache by downloading new data and saving it"""
        try:
            df = self._download_data()
            self.courts_data = self._transform_data(df)
            self._save_cache(self.courts_data)
        except requests.RequestException as e:
            print(f"Error downloading data: {e}")
            raise RuntimeError("Failed to download and no cache available.") if not self._load_cache() else print("Loaded data from cache after failed download.")

    def get_courts_for_county(self, county_name, refresh=False):
        """Returns the list of court records for a given county"""
        if refresh:
            self._refresh_cache()

        if self.courts_data is None:
            # Load data from cache or download if necessary
            if not self._load_cache():
                self._refresh_cache()
        
        # Get the list of court records for the given county, or None if the county is not found
        courts = self.courts_data.get(county_name, [])

        # Transform list into dict with 'Court' as key
        return {court: court['Court'] for court in courts}
    
    def get_courts_dropdown_for_county(self, county_name, refresh=False):
        """Returns the list of court records for a given county in a dropdown format"""
        courts = self.get_courts_for_county(county_name, refresh)
        return {court['Court']: court['Court'] for court in courts}
    
    def get_court(self, county_name, court_name, refresh=False):
        """Returns the court record for a given court in a county"""
        courts = self.get_courts_for_county(county_name, refresh)
        return courts.get(court_name)

# Example usage:
if __name__ == "__main__":
    tc = TexasJPCourts()
    county_name = 'Anderson'  # Example county name
    courts_in_county = tc.get_courts_by_county(county_name)
    print(courts_in_county)
# Output:
# [
#     {
#        "Court": "Precinct 1 Place 1",
#        "Court Type": "Justice of the Peace",
#        "Website": "http://www.co.anderson.tx.us/",
#        "Address": "P O Box 348",
#        "City": "Elkhart",
#        "Zip Code": "75839",
#        "Phone": "(903)764-5661",
#        "Email": "gthomas@co.anderson.tx.us"
#    },
#    ...
#]