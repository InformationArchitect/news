#!/usr/bin/env python3

import psycopg2

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
    <head>
        <title>
        </title>
        <style>
            h1, form { text-align: center; }
        </style>
    </head>
    <body>
        <h1>News Data Query</h1>
        <form method=post>
            <div><textarea id="query" name="query"></textarea></div>
        </form>
    </body>
</html>
'''

def mostPopularArticles(self, parameter_list):
    pass

def mostPopularAuthors(self, parameter_list):
    pass

if __name__ == "__main__":
    pass