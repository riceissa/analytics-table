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
    cursor.execute("""
           select
               project_title,
               sum(pageviews),
               year(pageviews_date),
               month(pageviews_date)
           from pageviews
           group by
               project_title,
               year(pageviews_date),
               month(pageviews_date)""")
    pageviews_data = cursor.fetchall()

    cursor.execute("""select project_title, url from projects""")
    projects = cursor.fetchall()
    print_table(projects, pageviews_data)


def plot_data(projects, pageviews_data):
    for project_title, _ in projects:
        xs = []
        ys = []
        for title, views, year, month in pageviews_data:
            if title == project_title:
                xs.append(datetime.datetime(year, month, 1))
                ys.append(views)
        plt.plot(xs, ys, label=project_title)
    plt.legend(loc='upper left')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def print_table(projects, pageviews_data):
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
        body { font-size: 12px; }
        table {
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

    print('''
        <img src="data:image/png;base64, %s" />
    ''' % plot_data(projects, pageviews_data))

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
    for project_title, url in projects:
        data = {(year, month): views for title, views, year, month in pageviews_data
                if title == project_title}
        print("<tr>")
        print('''<td><a href="%s">%s</a></td>''' % (url, project_title))
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


if __name__ == "__main__":
    main()
