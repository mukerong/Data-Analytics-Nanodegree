import re
from collections import defaultdict
import xml.etree.cElementTree as ET

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place',
            'Square', 'Lane', 'Road', 'Trail', 'Parkway', 'Commons']


def audit_street_types(street_types, street_name):
    street_types = defaultdict(set)

    for event, element in ET.iterparse(filename, event=(start,)):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                if tag.attrib['k'] == 'addr:street':
                    street_name = tag.attrib['v']
                    search = street_type_re.search(street_name)
                    if search:
                        street_type = search.group(0)
                        if street_type not in expected:
                            street_types[street_type].add(street_name)
    return street_types
