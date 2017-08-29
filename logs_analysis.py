import psycopg2


def get_query_results(query_string):
    """Queries database using the provided string"""
    db = psycopg2.connect(database="news")
    c = db.cursor()
    # connect and execute specified query
    c.execute(query_string)
    vals = c.fetchall()
    db.close()
    # close and return selected values
    return vals


def create_articles_view():
    """Creates a view aggregating all article visits by title and author"""
    db = psycopg2.connect(database="news")
    c = db.cursor()
    articles_query_string = (
     "CREATE OR REPLACE VIEW article_views AS "
     "SELECT articles.author, articles.title, count(log.path) AS visited "
     "FROM articles LEFT JOIN log "
     "ON position(articles.slug in log.path) > 0 "
     "GROUP BY articles.author, articles.title "
     "ORDER BY visited DESC;"
    )
    c.execute(articles_query_string)
    db.close()


def get_top_articles():
    """Fetches the 3 most visited articles"""
    top_articles_query_string = (
     "SELECT '\"' || title || '\"' as title, visited || ' views' "
     "FROM article_views LIMIT 3;"
    )
    return get_query_results(top_articles_query_string)


def get_top_authors():
    """Fetches the 3 most popular authors"""
    total_views = "sum(article_views.visited)"
    top_authors_query_string = (
     "SELECT authors.name, {0} || ' views' AS views "
     "FROM authors, article_views "
     "WHERE authors.id = article_views.author "
     "GROUP BY authors.name "
     "ORDER BY {0} DESC;"
    ).format(total_views)
    return get_query_results(top_authors_query_string)


def get_days_with_errors():
    """Fetches dates on which the error rate exceeded a threshold"""
    err_count = (
     "round((count(position('200' in status) = 0 OR null) / "
     "count(*)::float * 100)::numeric, 2)"
    )
    errors_query_string = (
     "SELECT to_char(time, 'fmMonth DD, YYYY') AS date, "
     "{0} || '% errors' AS err_count "
     "FROM log "
     "GROUP BY date "
     "HAVING {0} > 1;"
    ).format(err_count)
    return get_query_results(errors_query_string)


def write_results_to_file():
    """Write queried output to file"""
    top_articles = get_top_articles()
    top_authors = get_top_authors()
    days_with_errors = get_days_with_errors()
    results = [top_articles, top_authors, days_with_errors]

    with open("results.txt", "w") as f:
        i = 0
        for res_vals in results:
            for val in res_vals:
                f.write("{} -- {}\n".format(val[0], val[1]))
            i += 1

create_articles_view()
write_results_to_file()
