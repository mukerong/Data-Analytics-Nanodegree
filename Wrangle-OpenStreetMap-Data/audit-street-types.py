import re
from collections import defaultdict
import xml.etree.cElementTree as ET

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place',
            'Square', 'Lane', 'Road', 'Trail', 'Parkway', 'Commons']


def v_attrib_types(filename, k_value, pattern):
    types = defaultdict(set)

    for event, element in ET.iterparse(filename, events=('start',)):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                if tag.attrib['k'] == k_value:
                    v_value = tag.attrib['v']
                    search = pattern.search(v_value)
                    if search:
                        v_type = search.group(0)
                        if v_type not in expected:
                            types[v_type].add(v_value)
    return types
