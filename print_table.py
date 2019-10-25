#!/usr/bin/env python3

import mysql.connector
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import base64
import io
import sys

import login


def main():
    cnx = mysql.connector.connect(user=login.USER, database=login.DATABASE,
                                  password=login.PASSWORD)
    cursor = cnx.cursor()

    assert len(sys.argv) == 3+1, "Script must be run with right number of arguments"

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    title_regex = sys.argv[3]
    if not start_date:
        start_date = "2000-01-01"
    if not end_date:
        end_date = datetime.date.today() + datetime.timedelta(days=3)
    if not title_regex:
        # Match any non-empty title. I don't think this slows down the query
        # (especially given the small number of projects) and it simplifies the
        # query structure (we don't need separate cases for whether the title
        # regex exists or not).
        title_regex = "."
    cursor.execute("""
           select
               project_title,
               sum(pageviews),
               year(pageviews_date),
               month(pageviews_date)
           from pageviews
           where (pageviews_date between %s and %s)
                 and (project_title REGEXP %s)
           group by
               project_title,
               year(pageviews_date),
               month(pageviews_date)""", (start_date, end_date, title_regex))
    pageviews_data = cursor.fetchall()

    cursor.execute("""select project_title, url from projects""")
    projects = cursor.fetchall()
    total_pageviews = get_total_pageviews(pageviews_data)
    print_table(projects, pageviews_data, total_pageviews)


def plot_data(projects, pageviews_data, total_pageviews):
    dash_styles = [(3,3), (5,2,20,2), (1,1)]
    style_index = 0
    for project_title, _ in sorted(total_pageviews.items(), key=lambda x: x[1], reverse=True):
        xs = []
        ys = []
        for title, views, year, month in pageviews_data:
            if title == project_title:
                xs.append(datetime.datetime(year, month, 1))
                ys.append(views)
        if xs:
            plt.plot(xs, ys, label=project_title, linestyle="--",
                     dashes=dash_styles[style_index])
            style_index = (style_index + 1) % len(dash_styles)
    plt.legend(loc='upper right', bbox_to_anchor=(2.3, 1), ncol=2)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def print_table(projects, pageviews_data, total_pageviews):
    all_months = sorted(set((year, month) for _, _, year, month in pageviews_data),
                        reverse=True)

    print('''<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
      <link rel="stylesheet" href="/tablesorter.css">
      <script src="/jquery.min.js"></script>
      <script src="/jquery.tablesorter.js"></script>
      <style type="text/css">
        body { }
        table {
          font-size: 12px;
          background-color: #f9f9f9;
          border-collapse: collapse;
        }
        table th {
          background-color: #f2f2f2;
          border: 1px solid #aaaaaa;
          padding: 5px 10px;
        }
        table td {
          border: 1px solid #aaaaaa;
          padding: 5px 10px;
        }
      </style>
      <title>Vipul’s Empire</title>
    </head>
    <body>
    ''')

    print_intro()

    print('''
        <img src="data:image/png;base64, %s" />
    ''' % plot_data(projects, pageviews_data, total_pageviews))

    print("<table>")
    print("<thead>")
    print("  <tr>")
    print("  <th>Project title</th>")
    print("  <th>Total</th>")
    for year, month in all_months:
        print("  <th>")
        print(datetime.date(year, month, 1).strftime("%B %Y"))
        print("  </th>")
    print("  </tr>")
    print("</thead>")
    print("<tbody>")
    project_title_to_url = {project_title: url for project_title, url in projects}
    for project_title, _ in sorted(total_pageviews.items(), key=lambda x: x[1], reverse=True):
        data = {(year, month): views for title, views, year, month in pageviews_data
                if title == project_title}
        print("<tr>")
        print('''<td><a href="%s">%s</a></td>''' % (project_title_to_url[project_title],
                                                    project_title))
        print('''<td style="text-align: right;">{:,}</td>'''.format(sum(data.values())))
        for month in all_months:
            if month in data:
                print('''<td style="text-align: right;">{:,}</td>'''.format(data[month]))
            else:
                print('''<td style="text-align: right;">n.a.</td>''')
        print("</tr>")

    print("</tbody>")
    print("</table>")
    print('''
        <script>
        $(function(){
            $("table").tablesorter({sortInitialOrder: "desc"});
          });
    </script>
    </body>
    </html>
    ''')


def get_total_pageviews(pageviews_data):
    """Given all the pageviews rows, produce a dictionary with project titles
    as keys and total pageviews (across all months) as values. This allows us
    to sort projects by pageviews."""
    total_pageviews = {}
    for row in pageviews_data:
        title, views, year, month = row
        if title in total_pageviews:
            total_pageviews[title] += views
        else:
            total_pageviews[title] = 0
    return total_pageviews


def print_intro():
    print("""<p>
                This website displays pageviews data for Vipul Naik’s online projects
                (as well as for some of Issa Rice’s projects).
                Pageviews data come from Google Analytics.
                The site exists to give people one measure of the impact the
                projects are having.
                Inclusion criteria of projects for this site are informal at the moment;
                the aim is to include all projects where Google Analytics tracking code
                can be added, though we may be missing some sites for whatever reason.
                The source code for this project is available on
                <a href="https://github.com/riceissa/analytics-table">GitHub</a>.
            </p>""")


if __name__ == "__main__":
    main()
