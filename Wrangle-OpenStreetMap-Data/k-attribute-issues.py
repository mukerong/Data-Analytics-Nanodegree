import re
import xml.etree.cElementTree as ET

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}


def k_attrib_type(filename, keys):
    '''
    This function will read through the k element and return its catogory

    Parameters
    ---
    filename: .xml or .osm file
        the file that is going to be analyzed
    keys: a dictionary
        a dictionary to show the catogory

    Return
    ---
    the updated keys(a dictionary)
    '''
    for event, element in ET.iterparse(filename):
        if element.tag == 'tag':
            k = element.get('k')
            if lower.search(k):
                keys['lower'] += 1
            elif re.findall(lower_colon, k):
                keys['lower_colon'] += 1
            elif re.findall(problemchars, k):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1

    return keys
