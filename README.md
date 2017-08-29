# FSND Logs Analysis Project

## Description
Queries a mock news website's database using PostgreSQL and outputs answers to the following:

1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of the requests lead to errors?

The database includes three tables:

- authors
- articles
- log

Queries make use of joins, aggregations and filters. The results are logged to a text file.


## Instructions
1. Install the zip or clone [the repo](https://github.com/udayanshevade/FSND-Logs-Analysis.git)
2. Get the mock data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. Load the data using the command `psql -d news -f newsdata.sql`
3. Run logs_analysis.py. It should create the required view, and generate the results.
4. Open results.txt in your preferred text editor and ensure the results were properly logged.


### Technologies used
- Vagrant 1.9.2
- VirtualBox
- SQL/PostgreSQL
- Python 3.6.2