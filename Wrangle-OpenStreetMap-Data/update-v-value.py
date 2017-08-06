import re
from collections import defaultdict
import xml.etree.cElementTree as ET


def v_attrib_types(filename, k_attrib_value, pattern, expected):
    '''
    This function will seperate the k attribute value based on their patterns
    within a .osm file.

    Parameters
    ---
    filename (.xml or .osm): The file that is going to be parsed.
    k_attrib_value (str): The k attribute value you are looking for.
    pattern (re): The regex pattern used to categorize the k attribute value
    expected (list or re): the expected value list or pattern

    Return
    ---
    A dictionary conatains the category of the k values.
    '''
    types = defaultdict(set)

    for event, element in ET.iterparse(filename, events=('start',)):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                if tag.attrib['k'] == k_attrib_value:
                    v_value = tag.attrib['v']
                    search = pattern.search(v_value)
                    if search:
                        v_type = search.group(0)
                        try:
                            if v_type not in expected:
                                types[v_type].add(v_value)
                        except:
                            if not expected.search(v_type):
                                types[v_type].add(v_value)
    return types


def update_street_value(types, mapping):
    for st_types, names in types.items():
        for name in names:
            old_name = name.split(' ')[-1]
            if old_name in mapping:
                better_name = mapping[old_name]
                name = name.replace(old_name, better_name)
    return name


def update_phone_value(types, pattern):
    for phone_types, numbers in types.items():
        for number in numbers:
            if mapping.search(number):
                number = re.sub(mapping, r'^\d\d\d-\d\d\d-\d\d\d\d$')
    return
