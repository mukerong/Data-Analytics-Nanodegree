import re
from collections import defaultdict
import xml.etree.cElementTree as ET


def audit_street_type(street_types, street_name):
    match = street_type_re.search(street_name)
    if match:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_k_attrib(element, attrib_value):
    return (element.attrib['k'] == attrib_value)


def audit(filename):
    with open(filename, 'r') as f:
        street_types = defaultdict(set)
        for event, element in ET.iterparse(f, events=('start',)):
            if element.tag == 'node' or elment.tag == 'way':
                for tag in elment.iter('tag'):
                    if is_k_attrib(tag):
                        audit_street_type(street_types, tag.attrib['v'])
    return street_types
