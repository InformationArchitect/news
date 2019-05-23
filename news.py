#!/usr/bin/env python3
# code for the logs analysis project
"""
A module that executes 3 queries that each provide an insight into a database.

The database is the http request log, authors, and articles of a newspaper.

Returns:
3 sorted lists of 2 element tuples and accompanying titles
"""

import psycopg2

DATABASE = "news"

QUERY1 = '''
SELECT articles.title, mostpopular.numviews FROM (
    SELECT
        SUBSTRING (path, 10) AS "slug", count(*) AS "numviews"
        FROM log WHERE path != '/' AND
        status = '200 OK' GROUP BY slug
        ORDER BY count(*) DESC LIMIT 3
    ) AS mostpopular, articles
WHERE mostpopular.slug = articles.slug
ORDER BY mostpopular.numviews DESC;
'''

QUERY2 = '''
SELECT authors.name AS "name", count(*) AS "views" FROM
articles, authors, log
WHERE SUBSTRING (log.path, 10) = articles.slug
AND articles.author = authors.id
AND status = '200 OK'
GROUP BY name
ORDER BY views DESC;
'''

QUERY3 = '''
SELECT TO_CHAR(errors.day, 'FMMonth DD, YYYY') as "date",
100*CAST(errors.count AS FLOAT)/total.count
AS "Error_Rate" FROM (
    SELECT day,count(*) FROM
        (select CAST(time AS DATE) AS "day",
        SUBSTRING (status, 1, 3) FROM log WHERE status
        != '200 OK' ORDER BY time ASC)
    AS "errors" GROUP BY day ORDER BY day ASC
) AS "errors",
(
    SELECT day,count(*) FROM
        (select CAST(time AS DATE)
        AS "day", SUBSTRING (status, 1, 3) FROM log
        ORDER BY time ASC)
    AS "total" GROUP BY day ORDER BY day ASC
) AS "total"
WHERE 100*CAST(errors.count AS FLOAT)/total.count > 1
AND errors.day = total.day
ORDER BY date ASC;
'''


def executeQuery(query):
    """
    Execute a SQL query which is provided as a parameter and return the result.

    Parameters:
    query -- the SQL query as a string

    Returns:
    a sorted list of 2 element tuples containing the data the query selected
    """
    db = psycopg2.connect(dbname=DATABASE)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == "__main__":
    print("Top 3 Articles by Views")
    articles = list(executeQuery(QUERY1))
    for article in articles:
        print('"{}" -- {} views'.format(article[0], article[1]))
    print("\n")
    print("Authors Listed by Views")
    authors = list(executeQuery(QUERY2))
    for author in authors:
        print('{} -- {} views'.format(author[0], author[1]))
    print("\n")
    print("Days Where Error Rates Surpassed 1 Percent")
    errors = list(executeQuery(QUERY3))
    for error in errors:
        print('{0} -- {1:.2f}% errors'.format(error[0], error[1]))
