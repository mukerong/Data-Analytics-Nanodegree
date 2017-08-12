# Define a function to return the # of cuisine_type within a map
def cuisine_number():
    '''This function will return the # of restaurants of each cuisine types
    within the osm database
    '''
    Q = '''
    SELECT value, COUNT DISTINCT(id)
    FROM nodes_tags
    WHERE key = 'cuisine'
    GROUP BY value
    ORDER BY 2 DESC
    '''

    return c.execute(Q).fetchall()


# Define a function to return the zipcode and # of cuisine_type in that area
def cuisine_location(cuisine_type):
    '''This function will return the postcode and the cuisine type
    '''
    QUERY = '''
    SELECT nodes_tags.value, count(*) as num
    FROM nodes_tags
    JOIN (SELECT DISTINCT (id) FROM nodes_tags
            WHERE key = 'cuisine' AND value = {}) as second_nodes_tags
    ON nodes_tags.id = second_nodes_tags
    WHERE nodes_tags.key = 'postcode'
    GROUP BY nodes_tags.value
    ORDER BY num DESC;
    '''.format(cuisine)

    results = c.execute(QUERY).fetchall()
    return results
