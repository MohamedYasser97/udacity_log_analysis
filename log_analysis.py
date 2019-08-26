#!/usr/bin/env python

import sys
import psycopg2


def q1(c):
    print("\nWhat are the most popular three articles of all time?\n")

    query = ''' select title, views
                from articles, article_views
                where articles.slug = parsed_slug
                order by views desc
                limit 3;
            '''
    c.execute(query)
    result = c.fetchall()

    for row in result:
        print('"{}" - {} views.'.format(row[0], row[1]))


def q2(c):
    print("\nWho are the most popular article authors of all time?\n")

    query = ''' select name, sum(views) as total_views
                from authors, articles, article_views
                where authors.id = articles.author
                and articles.slug = parsed_slug
                group by name
                order by total_views desc
            '''
    c.execute(query)
    result = c.fetchall()

    for row in result:
        print('{} - {} views.'.format(row[0], row[1]))


def q3(c):
    print("\nOn which days did more than 1% of requests lead to errors?\n")

    query = ''' select log_errors.date,
                round(errors*100.0/requests, 1) as percentage
                from log_errors,log_count
                where log_errors.date = log_count.date
                and errors*100.0 > requests
            '''
    c.execute(query)
    result = c.fetchall()

    for row in result:
        print('{} - {}% errors.'.format(row[0], row[1]))


def main(argv):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # A view that extracts article slugs with respective views from the log
    article_views_query = ''' create view article_views as
                              select substring(path,10) as parsed_slug,
                              count(*) as views
                              from log
                              group by parsed_slug
                              order by views desc
                          '''
    # A view that extracts the date and total number of requests
    log_count_query = ''' create view log_count as
                          select to_char(time,'DD-MON-YYYY') as date,
                          count(*) as requests
                          from log
                          group by date
                      '''
    # A view that extracts the date and number of request errors
    log_errors_query = ''' create view log_errors as
                           select to_char(time,'DD-MON-YYYY') as date,
                           count(*) as errors
                           from log
                           where status like '%404%'
                           group by date
                      '''

    # Prevents throwing a duplication error when re-running the program
    try:
        c.execute(article_views_query)
        c.execute(log_count_query)
        c.execute(log_errors_query)
    except psycopg2.errors.DuplicateTable as e:
        db.rollback()

    db.commit()

    q1(c)

    print("-" * 60)
    q2(c)

    print("-" * 60)
    q3(c)
    print("-" * 60)

    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
