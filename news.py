#!/usr/bin/env python3
#code for the logs analysis project

import psycopg2

DBNAME = "news"

def mostPopularArticles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("")
    articles = c.fetchall()
    db.close()
    return articles

def mostPopularAuthors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute()
    authors = c.fetchall()
    db.close()
    return authors


def requestErrors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute()
    errors = c.fetchall()
    db.close()
    return errors


if __name__ == "__main__":
    mostPopularArticles()
    mostPopularAuthors()
    requestErrors()