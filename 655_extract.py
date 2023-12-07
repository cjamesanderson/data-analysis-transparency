# Extract from OCR plain-text of 655 reports of Direct Military Expenditures

from __future__ import print_function
from nltk.corpus import gazetteers
import csv

# Generate list of country names
COUNTRIES = set([country.upper() for filename in ('isocountries.txt','countries.txt')
                 for country in gazetteers.words(filename)])
COUNTRIES.remove(u'US')
COUNTRIES.remove(u'USA')
COUNTRIES.remove(u'BOSNIA AND HERZEGOVINA')
COUNTRIES.add(u'BOSNIA HERZEGOVINA')
COUNTRIES.add(u'UNITED NATIONS')
COUNTRIES.add(u'VARIOUS')
COUNTRIES.add(u'ANTARCTICA')

REPLACEMENT_MAP = {'ST.': 'SAINT', 'IS.': 'ISLANDS', '&': 'AND', 
                   'TAJIKSTAN': 'TAJIKISTAN', 'NAMBIA': 'NAMIBIA',
                   'SEYCHILLES': 'SEYCHELLES'}

def imp_06(fname):
    new_name = False  # Track when new country names are found
    current_name = None
    country_totals = list()
    csv_file = open(fname+'-base.csv', 'w')
    csv_writer = csv.writer(csv_file, lineterminator='\n')
    with open(fname) as f:
        # Skip introduction material
        for line in f:
            if 'Authorized Defense Articles' in line:
                break
        for line in f:
            line = line.upper()
            # Replace key grams
            for kk in REPLACEMENT_MAP:
                line = line.replace(kk, REPLACEMENT_MAP[kk])
            # Build list of country names found in line
            found_names = [c_name for c_name in COUNTRIES if c_name in line]
            # Choose longest country name found
            if found_names:
                m_len = max([len(c_name) for c_name in found_names])
                country_name = [c_name for c_name in found_names if len(c_name) == m_len][0]
                if country_name != current_name:
                    current_name = country_name
                    new_name = True
            if 'COUNTRY TOTAL' in line:
                if not new_name:
                    raise ValueError('Country total found without country name: %s' % country_name)
                dollars = int(line.split()[-1].strip().replace('$', '').replace(',',''))
                country_totals += [[country_name, dollars]]
                new_name = False
            # Write interrum results and switch to defense services numbers
            if 'Authorized Defense Services'.upper() in line:
                csv_writer.writerows(country_totals)
                country_totals = list()
                current_name = None
                new_name = False
                csv_file = open(fname+'-services.csv', 'w')
                csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerows(country_totals)
    
def imp_07(fname):
    new_name = False  # Track when new country names are found
    current_name = None
    country_totals = list()
    csv_file = open(fname+'-base.csv', 'w')
    csv_writer = csv.writer(csv_file, lineterminator='\n')
    with open(fname) as f:
        # Skip introduction material
        for line in f:
            if 'Authorized Defense Articles' in line:
                break
        for line in f:
            line = line.upper()
            # Replace key grams
            for kk in REPLACEMENT_MAP:
                line = line.replace(kk, REPLACEMENT_MAP[kk])
            # Build list of country names found in line
            found_names = [c_name for c_name in COUNTRIES if c_name in line]
            # Choose longest country name found
            if found_names:
                m_len = max([len(c_name) for c_name in found_names])
                country_name = [c_name for c_name in found_names if len(c_name) == m_len][0]
                if country_name != current_name:
                    current_name = country_name
                    new_name = True
            if 'COUNTRY TOTAL' in line:
                if not new_name:
                    raise ValueError('Country total found without country name: %s' % country_name)
                dollars = int(line.split()[-1].strip().replace('$', '').replace(',',''))
                country_totals += [[country_name, dollars]]
                new_name = False
            # Write interrum results and switch to defense services numbers
            if 'Authorized Defense Services'.upper() in line:
                csv_writer.writerows(country_totals)
                country_totals = list()
                current_name = None
                new_name = False
                csv_file = open(fname+'-services.csv', 'w')
                csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerows(country_totals)
    
def imp_08(fname):
    services = False  # Services text different from materials
    new_name = False  # Track when new country names are found
    skip_line = False # Sometimes money values show up on next line
    current_name = None
    country_totals = list()
    csv_file = open(fname+'-base.csv', 'w')
    csv_writer = csv.writer(csv_file, lineterminator='\n')
    with open(fname) as f:
        # Skip introduction material
        for line in f:
            if 'Authorized Defense Articles' in line:
                break
        for line in f:
            line = line.upper()
            # Replace key grams
            for kk in REPLACEMENT_MAP:
                line = line.replace(kk, REPLACEMENT_MAP[kk])
            # Build list of country names found in line
            found_names = [c_name for c_name in COUNTRIES if c_name in line]
            # Choose longest country name found
            if found_names:
                m_len = max([len(c_name) for c_name in found_names])
                country_name = [c_name for c_name in found_names if len(c_name) == m_len][0]
                if country_name != current_name:
                    current_name = country_name
                    new_name = True
            if not services:
                if 'AUTHORIZED' in line and 'GLOBAL' not in line and 'SERVICES' not in line:
                    if not new_name:
                        raise ValueError('Country total found without country name: %s' % country_name)
                    try:
                        d_index = line.split().index('AUTHORIZED')+2
                        dollars = int(line.split()[d_index].strip().replace('$', '').replace(',',''))
                        country_totals += [[country_name, dollars]]
                        new_name = False
                    except IndexError:
                        print('IndexError parsing %s' % country_name)
            elif 'COUNTRY TOTAL' in line:
                if not new_name:
                    raise ValueError('Country total found without country name: %s' % country_name)
                try:
                    d_index = line.split().index('TOTAL')+2
                    dollars = int(line.split()[d_index].strip().replace('$', '').replace(',',''))
                    country_totals += [[country_name, dollars]]
                    new_name = False
                except IndexError:
                    skip_line = True
            elif skip_line:
                try:
                    dollars = int(line.split()[-1].strip().replace(',',''))
                    country_totals += [[country_name, dollars]]
                    new_name = False
                    skip_line = False
                except ValueError:
                    # Skipp another line
                    pass
            # Write interrum results and switch to defense services numbers
            if 'Authorized Defense Services'.upper() in line:
                services = True
                csv_writer.writerows(country_totals)
                country_totals = list()
                current_name = None
                new_name = False
                csv_file = open(fname+'-services.csv', 'w')
                csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerows(country_totals)