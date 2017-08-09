import xml.etree.cElementTree as ET
import csv
import codecs

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid',
               'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

street_mapping = {
    'Ave': 'Avenue',
    'Ave.': 'Avenue',
    'St': 'Street',
    'St.': 'Street',
    'Ln': 'Lane',
    'Dr': 'Drive',
    'Ct': 'Court'
    }


def fix_street_errors(error, mapping):
    update_name = error.split(' ')[-1]
    if update_name in mapping:
        error = mapping[update_name]
    return error


def shape_element(element,
                  node_attr_fields=NODE_FIELDS,
                  way_attr_fields=WAY_FIELDS,
                  default_tag_type='regular'):
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == 'node':
        for item in NODE_FIELDS:
            node_attribs[item] = element.get(item)
        for child in element:
            tag_dict = {}
            colon = child.get('k').find(':')
            if child.tag == 'tag':
                tag_dict['id'] = element.get('id')
                tag_dict['value'] = child.get('v')
                if colon != -1:
                    type_value = child.get('k')[:colon]
                    key_value = child.get('k')[colon+1:]
                    tag_dict['type'] = type_value
                    tag_dict['key'] = key_value
                    if child.attrib['k'] == 'addr:street':
                        tag_dict['value'] = fix_street_errors(
                                child.attrib['v'], street_mapping
                                )
                    else:
                        tag_dict['value'] = child.attrib['v']
                else:
                    tag_dict['key'] = child.get('k')
                    tag_dict['type'] = 'regular'
                tags.append(tag_dict)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for item in WAY_FIELDS:
            way_attribs[item] = element.get(item)

        n = 0
        for child in element:
            if child.tag == 'nd':
                nd_dict = {}
                nd_dict['id'] = element.get('id')
                nd_dict['node_id'] = child.get('ref')
                nd_dict['position'] = n
                n += 1
                way_nodes.append(nd_dict)

            if child.tag == 'tag':
                way_tag_dict = {}
                colon = child.get('k').find(':')
                way_tag_dict['id'] = element.get('id')
                way_tag_dict['value'] = element.get('v')
                if colon != -1:
                    type_value = child.get('k')[:colon]
                    key_value = child.get('k')[colon+1:]
                    way_tag_dict['type'] = type_value
                    way_tag_dict['key'] = key_value
                    if child.attrib['k'] == 'addr:street':
                        way_tag_dict['value'] = fix_street_errors(child.attrib['v'], street_mapping)
                    else:
                        way_tag_dict['value'] = child.attrib['v']
                else:
                    way_tag_dict['key'] = child.get('k')
                    way_tag_dict['type'] = 'regular'
                tags.append(way_tag_dict)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def get_element(osm_file, tags=('node', 'way', 'relation')):

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


class UnicodeDictWriter(csv.DictWriter, object):

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (str(v).encode('utf-8'))
            for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"


def process_map(file_in):
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
