#!/usr/bin/env python3

import pdb

import mysql.connector
import datetime
import sys
import re

import login
import util


def main():
    cnx = mysql.connector.connect(user=login.USER, database=login.DATABASE,
                                  password=login.PASSWORD)
    cursor = cnx.cursor()

    assert len(sys.argv) == 4+1, "Script must be run with right number of arguments"

    project_title = sys.argv[1]
    if not project_title:
        project_title = "Vipul Naik"
    try:
        limit_pagepaths = int(sys.argv[2])
    except ValueError:
        limit_pagepaths = 100
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    if not start_date:
        start_date = "2000-01-01"
    if not end_date:
        end_date = datetime.date.today() + datetime.timedelta(days=3)
    cursor.execute("""
        select
            year(pageviews_date),
            month(pageviews_date),
            pagepath,
            sum(pageviews)
        from pageviews
        where
            project_title = %s
            and pageviews_date between %s and %s
        group by
            year(pageviews_date),
            month(pageviews_date),
            pagepath
    """, (project_title, start_date, end_date))
    data_dict = normalized_dict(cursor.fetchall())
    all_months = sorted(set((year, month) for year, month, _ in data_dict), reverse=True)
    all_pagepaths = sorted(set(pagepath for _, _, pagepath in data_dict))

    cursor.execute("""select project_title, url from projects""")
    projects = cursor.fetchall()
    project_title_to_url = {project_title: url for project_title, url in projects}

    util.print_head()

    print("""<p>A value of 0 in the table below includes the possibility that the
                page did not exist in that month. If viewing the table with a
                limit to the number of pagepaths shown (which includes the
                default view of showing the top <em>n</em> = 100 pages of all time),
                sorting by a month may not show the actual
                top pages for that month; rather it shows the top <em>n</em>
                pages of all time sorted by pageviews for that month. (So for
                instance if a page received a huge number of views in one
                month but received no views in all other months, it may not
                make it to the top <em>n</em> pages of all time even if it
                actually was the most viewed page for some month. Such a
                page would not be shown in the table.)</p>""")

    print('''<div class="container">''')
    print("<table>")
    print("<thead>")
    print("  <tr>")
    print("  <th>Pagepath</th>")
    print("  <th>Total</th>")
    for year, month in all_months:
        print("  <th>")
        print(datetime.date(year, month, 1).strftime("%B %Y"))
        print("  </th>")
    print("  </tr>")
    print("</thead>")
    print("<tbody>")
    total_pageviews = {}
    for (y, m, pp) in data_dict:
        total_pageviews[pp] = total_pageviews.get(pp, 0) + data_dict[(y, m, pp)]
    for pagepath, total_for_pagepath in sorted(total_pageviews.items(), key=lambda x: x[1], reverse=True)[:limit_pagepaths]:
        print("<tr>")
        project_url = project_title_to_url[project_title]
        # pagepath already begins with a slash, so remove it from the project
        # url if it exists
        if project_url.endswith('/'):
            project_url = project_url[:-1]
        print('''<th><a href="%s%s">%s</a></th>''' % (project_url,
                                                      pagepath,
                                                      abbreviated(pagepath)))
        print('''<td style="text-align: right;">{:,}</td>'''.format(total_for_pagepath))
        for month in all_months:
            y, m = month
            if (y, m, pagepath) in data_dict:
                print('''<td style="text-align: right;">{:,}</td>'''.format(data_dict[(y, m, pagepath)]))
            else:
                print('''<td style="text-align: right;">0</td>''')
        print("</tr>")
    print("</tbody>")
    print("</table>")
    print("</div>")


    util.print_closing()

def normalized_dict(data):
    result = {}
    fbclid_pat = re.compile(r'\?fbclid=[a-zA-Z0-9_-]+$')
    printable_pat = re.compile(r'\?printable=')
    for (year, month, pagepath, pageviews) in data:
        pagepath = fbclid_pat.sub('', pagepath)
        pagepath = printable_pat.sub('', pagepath)
        pagepath = pagepath.replace(' ', '_')
        key = (year, month, pagepath)
        if key in result:
            result[key] = result[key] + pageviews
        else:
            result[key] = pageviews
    return result


def abbreviated(string):
    if len(string) < 100:
        return string
    else:
        return string[:100] + "…"


if __name__ == "__main__":
    main()
