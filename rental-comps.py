"""
Module for estimating rents in given zip code
Given zip codes, downloads list of properties from apartments.com and runs
multiple regression to predict rent based on:
property type (sfh, apt, etc.), # bedrooms, # bathrooms, square footage 

TODO
Ability to scrape multiple zip codes
Clean output list of properties to include those suitable for regression
Output property attributes to CSV
"""

# Web scraping packages

import urllib.request
from bs4 import BeautifulSoup

# Global variables

#ZIP_CODE = 54956 # Neenah, WI
ZIP_CODE = 54302 # Green Bay, WI (one of several)

# Helper classes/functions

class Property:
    """
    Class for storing details of properties
    """

    def __init__(self, url):
        self._url = url
        self._address = ''
        self._rent = ''
        self._property_type = ''
        self._num_bedrooms = ''
        self._num_bathrooms = ''
        self._square_footage = ''

    def __str__(self):
        output_str = 'url is ' + str(self._url)

        property_class_dict = {'address': self._address,
                       'rent': self._rent,
                       'property_type': self._property_type,
                       'num_bedrooms': self._num_bedrooms,
                       'num_bathrooms': self._num_bathrooms,
                       'square_footage': self._square_footage}

        for property_attribute in property_class_dict.keys():
            if property_class_dict[property_attribute] != '':
                output_str += "\n" + str(property_attribute) + " is "
                output_str += str(property_class_dict[property_attribute])
        return output_str

    def get_url(self):
        return self._url

    def set_address(self, address):
        self._address = address

    def get_address(self):
        return self._address
        
    def set_rent(self, rent):
        self._rent = rent

    def get_rent(self):
        return self._rent

    def set_type(self, property_type):
        self._property_type = property_type

    def get_type(self):
        return self._property_type

    def set_bedrooms(self, num_bedrooms):
        self._num_bedrooms = num_bedrooms

    def get_bedrooms(self):
        return self._num_bedrooms

    def set_bathrooms(self, num_bathrooms):
        self._num_bathrooms = num_bathrooms

    def get_bathrooms(self):
        return self._num_bathrooms

    def set_sqft(self, square_footage):
        self._square_footage = square_footage

    def get_sqft(self):
        return self._square_footage

def get_property_list(zip_code):
    """
    Takes int of zip code as input, returns list of trulia.com urls for available properties
    """

    # Generate trulia url with list of properties based on zip code
    property_list_url = 'https://www.trulia.com/for_rent/' + str(zip_code) + '_zip/'

    # Get and parse html data from url
    req = urllib.request.Request(
        property_list_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req)
    property_list_raw = f.read()
    property_list_parsed = BeautifulSoup(property_list_raw, 'html.parser') 
    
    # Add property urls to a set
    property_set = set()

    for a in property_list_parsed.select('a'):
        if 'class' in a.attrs:
            if a['class'][0] == "tileLink":
                if 'href' in a.attrs:
                    property_set.add(a['href'])
    
    # Create full urls and list
    property_list = []

    for partial_url in property_set:
        property_list.append('https://www.trulia.com' + partial_url)

    print("found " + str(len(property_list)) + " properties\n")

    return property_list

def create_property(url):
    """
    Given trulia url for rental, returns instance of Property class with as many attributes
    as possible populated
    """

    new_property = Property(url)

    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req)
    property_attrs_raw = f.read()
    property_attrs_parsed = BeautifulSoup(property_attrs_raw, 'html.parser')

    # Set address
    for div in property_attrs_parsed.select('div'):
        if 'id' in div.attrs:
            if div['id'] == 'address':
                for span in div.select('span'):
                    if 'class' not in span.attrs:
                        new_property.set_address(span.text)

    # Set rent
    for div in property_attrs_parsed.select('div'):
        if 'class' in div.attrs:
            if div['class'][0] == 'mvn':
                for span in div.select('span'):
                    if 'class' in span.attrs:
                        try:
                            rent = int(span.text.strip()[1:].replace(",",""))
                            if rent > 5000:
                                new_property.set_rent("ERROR")
                            else:
                                new_property.set_rent(span.text.strip()[1:].replace(",",""))
                        except:
                            new_property.set_rent("ERROR")

    # Set type, bedrooms, bathrooms, sqft where available
    for li in property_attrs_parsed.select('li'):
        if 'class' in li.attrs:
            if li['class'][0] == "iconHome":
                try:
                    new_property.set_type(li.text[1:])
                except:
                    new_property.set_type("ERROR")
            elif li['class'][0] == "iconBed":
                try:
                    new_property.set_bedrooms(int(li.text[1:-4]))
                except:
                    new_property.set_bedrooms("ERROR")
            elif li['class'][0] == "iconBath":
                try:
                    new_property.set_bathrooms(float(li.text[1:-5]))
                except:
                    new_property.set_bathrooms("ERROR")
            elif li['class'][0] == "iconFloorplan":
                try:
                    new_property.set_sqft(int(li.text[1:-4].replace(",","")))
                except:
                    new_property.set_sqft("ERROR")
    
    return new_property

# Example for ZIP_CODE

example_properties = get_property_list(ZIP_CODE)

for idx, page in enumerate(example_properties):
    new = create_property(page)
    print("PROPERTY #" + str(idx + 1))
    print(new)
    print("\n")