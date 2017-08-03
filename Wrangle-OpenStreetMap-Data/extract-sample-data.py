import xml.etree.cElementTree as ET

# Name the orgial dataset, export file, and the tags we are looking for
osm_file = 'chicago_illinois.osm'
sample_file = 'sample_chicago.osm'
tags = ['node', 'way', 'relation']


# Define a function to yield all the elements we need
def get_element(osm_file, tags=('node', 'way', 'relation')):
    '''
    This function will read an XML file, get the element from desired tags.

    Parameters
    ----------
    osm_file: .xml or .osm file
        the XML or OSM file to be parsed

    tags: string or list
        the tag name that you want to get elements from.
        default is ['node', 'way', 'relation']

    Return
    ------
    .xml or .osm file
    '''

    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)

    for event, elem in context:
        if (event == 'end') and (elem.tag in tags):
            yield elem
            root.clear()


# write the generated elements into sample.osm file
k = 1000  # We will extract 1/k of the original file
with open(sample_file, 'wb') as output:
    output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'UTF-8'))
    output.write(bytes('<osm>\n  ', 'UTF-8'))

    for i, element in enumerate(get_element(osm_file)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(bytes('</osm>', 'UTF-8'))
