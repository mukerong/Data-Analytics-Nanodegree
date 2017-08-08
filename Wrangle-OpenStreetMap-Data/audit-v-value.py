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


def shape_element(element,
                  node_attr_fields=NODE_FIELDS,
                  way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS,
                  default_tag_type='regular'):
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == 'nodes':
        for item in NODE_FIELDS:
            node_attrib[item] = element.get(item)
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
                else:
                    way_tag_dict['key'] = child.get('k')
                    way_tag_dict['type'] = 'regular'
                tags.append(way_tag_dict)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
