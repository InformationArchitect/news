#!/usr/bin/env python3
#code for the logs analysis project

import psycopg2

DATABASE = "news"

def mostPopularArticles():
    db = psycopg2.connect(dbname=DATABASE)
    c = db.cursor()
    c.execute('''
                select articles.title, mostpopular.numviews from (
                    select 
                        SUBSTRING (path, 10) as "slug", count(*) as "numviews"
                        from log where path != '/' and status = '200 OK' group by SUBSTRING (path, 10)
                        order by count(*) desc limit 3
                    ) as mostpopular, articles
                    where mospopular.slug = articles.slug
                    order by mostpopular.numviews DESC;
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
                select errors.day, 100*cast(errors.count as FLOAT)/successes.count as "Error_Rate" from (
                        select day,count(*) from (select date_trunc('day', time) as "day", SUBSTRING (status, 1, 3) from log where status
                        != '200 OK' order by time asc) as "errors" group  by day order by day asc
                    ) as "errors", 
                    (
                        select day,count(*) from (select date_trunc('day', time) as "day", SUBSTRING (status, 1, 3) from log order by time asc)
                        as "successes" group by day order by day asc
                    ) as "successes"
                    where 100*cast(errors.count as FLOAT)/successes.count > 1;
    ''')
    errors = c.fetchall()
    db.close()
    return errors


if __name__ == "__main__":
    print(mostPopularArticles())
    print(mostPopularAuthors())
    print(requestErrors())


    