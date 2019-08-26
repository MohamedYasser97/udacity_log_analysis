# Log Analysis
A Python script that connects to a PostgreSQL database and runs some queries.


## Code Layout and Flow
This project consists of just one file (__log_analysis.py__). The program starts from the __main__ function, and from there, I connect to the PostgreSQL database called __news__. 

After that I automatically create the required views and handle view-duplication errors caused from rerunning the program __so that the code reviewer doesn't have to enter the SQL code manually__ while being able to run the program as much as they want.

Each query of the three required queries has its own function, __q1(), q2() and q3()__ respectively. Each of which takes the database cursor as an argument to be able to run the required query.

All the query results are printed to the STDOUT buffer and can be redirected to a file if needed (That's how I created __test_run.txt__).

## Execution
In order to run this program, please first make sure that you import the __news__ database by executing the following command in the project's directory after copying the __newsdata.sql__ file there:
`psql -d news -f newsdata.sql`

Then, all you have to do is execute the following command:
`python log_analysis.py`

__* You DO NOT have to create the views manually from the `psql` terminal because I already handle that from my code! *__ 

## Used Views
I've created and used these views to make my queries simpler and easier to read instead of nesting subqueries.

---

This view returns a table that consists of two columns: Every article's slug string and its respective view count.
```SQL
create view article_views as
select substring(path, 10) as parsed_slug, count(*) as views
from log
group by parsed_slug
order by views desc
```

---

This view returns a table that consists of two columns: A given day's date and the total number of requests sent on that day.
```SQL
create view log_count as
select to_char(time,'DD-MON-YYYY') as date, count(*) as requests
from log
group by date
```

---

This view returns a table that consists of two columns: A given day's date and the number of __failed__ requests sent on that day.
```SQL
create view log_errors as
select to_char(time,'DD-MON-YYYY') as date, count(*) as errors
from log
where status like '%404%'
group by date
```

## Sample Output
The following is the exact same content of __test_run.txt__.
```txt

What are the most popular three articles of all time?

"Candidate is jerk, alleges rival" - 338647 views.
"Bears love berries, alleges bear" - 253801 views.
"Bad things gone, say good people" - 170098 views.
------------------------------------------------------------

Who are the most popular article authors of all time?

Ursula La Multa - 507594 views.
Rudolf von Treppenwitz - 423457 views.
Anonymous Contributor - 170098 views.
Markoff Chaney - 84557 views.
------------------------------------------------------------

On which days did more than 1% of requests lead to errors?

17-JUL-2016 - 2.3% errors.
------------------------------------------------------------

```
