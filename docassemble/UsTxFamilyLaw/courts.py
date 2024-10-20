"""
courts.py - Classes and methods for retrieving court information.
"""

import pandas as pd
import requests
from io import StringIO
import os
import json

from docassemble.base.util import DAFile, DAObject

__all__ = [
    'TexasJPCourts',
    'TexasDistrictCourts',
    'TexasDistrictClerks'
]

class Courts:
    county_field = 'County'
    court_fields = {
        'Court': 'Court',
        'Court_Type': 'Court Type',
        'Website': 'Website',
        'Address': 'Address',
        'City': 'City',
        'Zip_Code': 'Zip Code',
        'Phone': 'Phone',
        'Email': 'Email'
    }

    def __init__(self, url, cache_file):
        self.url = url
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
        da_cache_file = DAFile('court_cache')
        da_cache_file.initialize(filename=self.cache_file, mimetype='application/json')
        if os.path.exists(da_cache_file.path()):
            with open(da_cache_file.path(), 'r', encoding='utf-8') as f:
                self.courts_data = json.load(f)
            return True
        return False

    def _save_cache(self, data):
        """Saves the data to the cache file"""
        da_cache_file = DAFile('court_cache')
        da_cache_file.initialize(filename=self.cache_file, mimetype='application/json')
        with open(da_cache_file.path(), 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def _transform_data(self, df):
        """Transforms the DataFrame into the desired dictionary format"""
        courts_dict = {}
        for _, row in df.iterrows():
            county = f"{row[Courts.county_field]} County"
            record = {field: row[Courts.court_fields[field]] for field in Courts.court_fields}
            record['Court'] = self._rename_court(row[Courts.court_fields['Court']])
            if record['Court'] == "(do not use)":
                continue
            if county not in courts_dict:
                courts_dict[county] = []
            courts_dict[county].append(record)
        return courts_dict

    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        # This method can be overridden in the subclass to provide custom renaming logic
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

    def get_courts_for_county(self, county_name, refresh=False) -> list:
        """Returns the list of court records for a given county"""
        if refresh:
            self._refresh_cache()

        if self.courts_data is None:
            # Load data from cache or download if necessary
            if not self._load_cache():
                self._refresh_cache()

        # Get the list of court records for the given county, or None if the county is not found
        return self.courts_data.get(county_name, [])

    def get_courts_dropdown_for_county(self, county_name, refresh=False)-> list:
        """Returns the list of court records for a given county in a dropdown format"""
        courts = self.get_courts_for_county(county_name, refresh)
        return [court['Court'] for court in courts]

    def get_court(self, county_name, court_name, refresh=False) -> DAObject:
        """Returns the court record for a given court in a county"""
        courts = self.get_courts_for_county(county_name, refresh)

        # Find the court record with the given court name
        for court in courts:
            if court['Court'] == court_name:
                da_court = DAObject('Court')
                da_court.init(**court)
                return da_court

        da_court = DAObject('Court')
        da_court.init(Court="Court not found", Court_Type="", Website="", Address="", City="", Zip_Code="", Phone="", Email="")
        return da_court


class TexasJPCourts(Courts):
    def __init__(self):
        super().__init__(
            url='https://card.txcourts.gov/ExcelExportPublic.aspx?type=C&export=E&SortBy=tblCounty.Sort_ID,%20tblCourt.Court_Identifier&Active_Flg=true&Court_Type_CD=56&Court_Sub_Type_CD=0&County_ID=0&City_CD=0&Court=&DistrictPrimaryLocOnly=0&AdminJudicialRegion=0&COADistrictId=0',
            cache_file='jp_courts_cache.json'
        )

    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        if court_name.lower().startswith('jail') or court_name.lower().startswith('truancy'):
            return "(do not use)"
        return court_name


class TexasCountyCourtsAtLaw(Courts):
    def __init__(self):
        super().__init__(
            url='https://card.txcourts.gov/ExcelExportPublic.aspx?type=C&export=E&SortBy=tblCounty.Sort_ID,%20tblCourt.Court_Identifier&Active_Flg=true&Court_Type_CD=54&Court_Sub_Type_CD=1613&County_ID=0&City_CD=0&Court=&DistrictPrimaryLocOnly=0&AdminJudicialRegion=0&COADistrictId=0',
            cache_file='county_courts_cache.json'
        )

    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        lower_court_name = court_name.lower()
        if lower_court_name.startswith('ccl no.'):
            # Remove "& Probate Court" from the court name
            court_name = court_name.replace(' & Probate Court', '')
            court_name = court_name.replace('CCL No.', 'County Court at Law No.')
            return court_name
        if 'criminal' in lower_court_name or 'crim.' in lower_court_name:
            return "(do not use)"
        return court_name


class TexasDistrictCourts(Courts):
    def __init__(self):
        super().__init__(
            url='https://card.txcourts.gov/ExcelExportPublic.aspx?type=C&export=E&SortBy=tblCounty.Sort_ID,%20tblCourt.Court_Identifier&Active_Flg=true&Court_Type_CD=55&Court_Sub_Type_CD=0&County_ID=0&City_CD=0&Court=&DistrictPrimaryLocOnly=1&AdminJudicialRegion=0&COADistrictId=0',
            cache_file='district_courts_cache.json'
        )

    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        if court_name.lower().startswith('district clerk'):
            return "(do not use)"
        return court_name


class TexasDistrictClerks(TexasDistrictCourts):
    def _rename_court(self, court_name):
        """Renames the court name to a more readable format"""
        if court_name.lower().startswith('district clerk'):
            return court_name
        return "(do not use)"

    def get_clerk(self, county_name, refresh=False):
        clerk = self.get_court(county_name, 'District Clerk Office', refresh)
        da_clerk = DAObject('DistrictClerk')
        try:
            da_clerk = clerk
        except KeyError:
            da_clerk.init(Name="District Clerk Office", Website="", Address="", City="", Zip_Code="", Phone="", Email="")
        return da_clerk

# Example usage:
if __name__ == "__main__":
    jp_courts = TexasJPCourts()
    district_courts = TexasDistrictCourts()

    # Example county name
    county_name = 'Anderson'

    # Get Justice of the Peace courts for a county
    jp_courts_in_county = jp_courts.get_courts_for_county(county_name)
    print(jp_courts_in_county)

    # Get District courts for a county
    district_courts_in_county = district_courts.get_courts_for_county(county_name)
    print(district_courts_in_county)
