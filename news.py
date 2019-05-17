#!/usr/bin/env python3
#code for the logs analysis project

import psycopg2

DATABASE = "news"

def mostPopularArticles():
    db = psycopg2.connect(dbname=DATABASE)
    c = db.cursor()
    c.execute('''
                SELECT articles.title, mostpopular.numviews FROM (
                    SELECT 
                        SUBSTRING (path, 10) AS "slug", count(*) AS "numviews"
                        FROM log WHERE path != '/' AND status = '200 OK' GROUP BY SUBSTRING (path, 10)
                        ORDER BY count(*) DESC LIMIT 3
                    ) AS mostpopular, articles
                    WHERE mostpopular.slug = articles.slug
                    ORDER BY mostpopular.numviews DESC;
                ''')
    articles = c.fetchall()
    db.close()
    return articles

def mostPopularAuthors():
    db = psycopg2.connect(dbname=DATABASE)
    c = db.cursor()
    c.execute('''
                SELECT popular.name, SUM(popular.numviews) AS views FROM (
                    SELECT authors.name, idpopular.slug, idpopular.numviews FROM (
                        SELECT articles.author, articles.slug, mostpopular.numviews FROM (
                            SELECT 
                                SUBSTRING (path, 10) AS "slug", count(*) AS "numviews"
                                FROM log WHERE path != '/' AND status = '200 OK' GROUP BY SUBSTRING (path, 10)
                                ORDER BY count(*) DESC
                            ) AS mostpopular, articles
                            WHERE mostpopular.slug = articles.slug
                            ORDER BY mostpopular.numviews DESC
                        ) AS idpopular, authors 
                        WHERE idpopular.author = authors.id
                        ORDER BY numviews
                    ) AS popular
                    GROUP BY popular.name
                    ORDER BY views DESC;
                ''')
    authors = c.fetchall()
    db.close()
    return authors


def requestErrors():
    db = psycopg2.connect(dbname=DATABASE)
    c = db.cursor()
    c.execute('''
                SELECT SUBSTRING(CAST(errors.day AS TEXT), 1, 10), 100*CAST(errors.count AS FLOAT)/successes.count AS "Error_Rate" FROM (
                        SELECT day,count(*) FROM (select date_trunc('day', time) AS "day", SUBSTRING (status, 1, 3) FROM log WHERE status
                        != '200 OK' ORDER BY time ASC) AS "errors" GROUP BY day ORDER BY day ASC
                    ) AS "errors", 
                    (
                        SELECT day,count(*) FROM (select date_trunc('day', time) AS "day", SUBSTRING (status, 1, 3) FROM log ORDER BY time ASC)
                        AS "successes" GROUP BY day ORDER BY day ASC
                    ) AS "successes"
                    WHERE 100*CAST(errors.count AS FLOAT)/successes.count > 1;
    ''')
    errors = c.fetchall()
    db.close()
    return errors


if __name__ == "__main__":
    print("Top 3 Articles by Views")
    articles = list(mostPopularArticles())
    for article in articles:
        print('"{}" -- {} views'.format(article[0], article[1]))
    print("\n")
    print("Authors Listed by Views")
    authors = list(mostPopularAuthors())
    for author in authors:
        print('{} -- {} views'.format(author[0], author[1]))
    print("\n")
    print("Days Where Error Rates Surpassed 1 Percent")
    errors = list(requestErrors())
    for error in errors:
        print('{0} -- {1:.1f}% errors'.format(error[0], error[1]))

    