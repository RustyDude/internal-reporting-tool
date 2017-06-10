#!/usr/bin/env python3

import psycopg2

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# query for question #1
# involves a view creation of viewcount(see README.md for more info)
c.execute("""
            select title, view_count
            from viewcount
            order by view_count desc
            limit 3
          """)
top_articles = c.fetchall()

# query for question #2
# invovles the view viewcount used in question #1(see README for more info)
c.execute("""
            select a.name, sum(vc.view_count) as overall_views
            from (select * from viewcount) as vc
            join authors as a on a.id = vc.id
            group by a.name
            order by overall_views desc
          """)
author_rank = c.fetchall()

# query for question #3
# involves view creation of log_errors and percentage(see README for more info)
c.execute("""
            select date, error_percentage
            from percentage
            where error_percentage>1.0
          """)
error_days = c.fetchall()

# prints out in a file called "reportfile"
with open('reportfile.txt', 'w') as results:
    # question #1
    results.write("1. What are the most popular three articles of all time?\n")
    for x in top_articles:
        results.write('"{0}" — {1} views\n'.format(x[0], x[1]))
    # question #2
    results.write(
        "\n2. Who are the most popular article authors of all time?\n")
    for x in author_rank:
        results.write('{0} — {1} views\n'.format(x[0], x[1]))
    # question #3
    results.write(
        "\n3. On which days did more than 1%% of requests lead to errors?\n"
    )
    for x in error_days:
        results.write('{0} — {1}% errors\n'.format(x[0], x[1]))

db.close()
