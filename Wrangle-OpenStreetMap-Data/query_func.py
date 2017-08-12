# Define a function to return the # of cuisine_type within a map
def cuisine_number(cursor):
    '''
    This function will return the # of restaurants of each cuisine types
    within the osm database
    '''
    Q = '''
    SELECT value, COUNT (DISTINCT(id))
    FROM nodes_tags
    WHERE key = 'cuisine'
    GROUP BY value
    ORDER BY 2 DESC
    '''

    return cursor.execute(Q).fetchall()


# Define a function to return the zipcode and # of cuisine_type in that area
def cuisine_location(cursor, cuisine_type):
    '''
    This function will return the postcode and the cuisine type
    '''
    QUERY = '''
    SELECT nodes_tags.value, COUNT(*)
    FROM nodes_tags
    JOIN
        (SELECT DISTINCT (id) FROM nodes_tags
        WHERE key = 'cuisine' AND value = "{}") as second_nodes_tags
    ON nodes_tags.id = second_nodes_tags.id
    WHERE nodes_tags.key = 'postcode'
    GROUP BY 1
    ORDER BY 2 DESC;
    '''.format(cuisine_type)

    results = cursor.execute(QUERY).fetchall()
    return results


# Define a function to find the number of restaurants
def num_restaurant(cursor):
    '''
    This function will return the total number of restaurants
    within the database
    '''
    QUERY = '''
    SELECT COUNT (DISTINCT(id)) FROM nodes_tags
    WHERE nodes_tags.value = 'restaurant';
    '''

    results = cursor.execute(QUERY).fetchall()
    return results


# Define a function to find restaurants without a postcode
def cuisine_wo_code(cursor, cuisine_type):
    '''
    This function will return the id and # of restaurants that
    don't have a postcode.
    '''
    Q = '''
    SELECT nodes_tags.id, nodes_tags.value
    FROM nodes_tags
    WHERE (id NOT IN
        (SELECT DISTINCT(id) FROM nodes_tags
        WHERE key = 'postcode'))
    AND (key = 'cuisine')
    AND (value = "{}")
    '''.format(cuisine_type)

    results = cursor.execute(Q).fetchall()
    return results
