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
    WHERE nodes_tags.value = 'restaurants';
    '''

    results = cursor.execute(QUERY).fetchall()
    return results
