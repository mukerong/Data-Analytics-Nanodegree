import re
from collections import defaultdict
import xml.etree.cElementTree as ET


def check_errors(v_value_types, v_value, pattern, expected):

    match = pattern.search(v_value)
    if match:
        v_value_type = match.group()
        try:
            if v_value_type not in expected:
                v_value_types[v_value_type].add(v_value)
        except:
            if not expected.search(v_value):
                v_value_types[v_value_type].add(v_value)
    return v_value_types


def is_k_attrib(element, k_attrib_value):
    return (element.attrib['k'] == k_attrib_value)


def audit(filename, k_attrib_value, pattern, expected):
    v_value_types = defaultdict(set)

    with open(filename, 'r') as f:
        for event, element in ET.iterparse(f, events=('start',)):
            if element.tag == 'node' or element.tag == 'way':
                for tag in element.iter('tag'):
                    if is_k_attrib(tag, k_attrib_value):
                        check_errors(v_value_types,
                                     tag.attrib['v'], pattern, expected)
    return v_value_types


def fix_street_errors(error, mapping):
    update_name = error.split(' ')[-1]
    if update_name in mapping:
        error = mapping[update_name]
    return error
