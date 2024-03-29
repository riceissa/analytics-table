#!/usr/bin/env python3

import mysql.connector
import datetime
import sys
import re

import login
import util


def h_index(lst):
    lst = sorted(lst, reverse=True)
    i = 0
    while i < len(lst):
        new_i = i + 1
        # Access list at i rather than new_i because Python lists are 0-indexed
        if lst[i] >= new_i:
            i = new_i
        else:
            break
    return i


def main():
    cnx = mysql.connector.connect(user=login.USER, database=login.DATABASE,
                                  password=login.PASSWORD)
    cursor = cnx.cursor()

    assert len(sys.argv) == 5+1, "Script must be run with right number of arguments"

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
    pagepath_regex = sys.argv[5]
    if not pagepath_regex:
        # Match any non-empty pagepath. This might slow down the query but it
        # simplifies the query structure (we don't need separate cases for
        # whether the title regex exists or not). We might want to change this
        # later so that if there is no regex we do a different query that skips
        # the regex part.
        pagepath_regex = "."
    cursor.execute("""
        select
            year(pageviews_date),
            month(pageviews_date),
            pagepath,
            sum(pageviews)
        from path_pageviews
        where
            project_title = %s
            and pageviews_date between %s and %s
            and pagepath regexp %s
        group by
            year(pageviews_date),
            month(pageviews_date),
            pagepath
    """, (project_title, start_date, end_date, pagepath_regex))
    data_dict = normalized_dict(cursor.fetchall(), project_title)
    all_months = sorted(set((year, month) for year, month, _ in data_dict), reverse=True)
    all_pagepaths = sorted(set(pagepath for _, _, pagepath in data_dict))

    cursor.execute("""select project_title, url from projects""")
    projects = cursor.fetchall()
    project_title_to_url = {project_title: url for project_title, url in projects}

    util.print_head()

    print("""<p>A value of 0 in the table below includes the possibility that the
                page did not exist in that month. If viewing the table with a
                limit to the number of pagepaths shown (which includes the
                default view of showing the top <em>n</em>&nbsp;=&nbsp;100 pages of all time),
                sorting by a month may not show the actual
                top pages for that month; rather it shows the top <em>n</em>
                pages of all time sorted by pageviews for that month. (So for
                instance if a page received a huge number of views in one
                month but received no views in all other months, it may not
                make it to the top <em>n</em> pages of all time even if it
                actually was the most viewed page for some month. Such a
                page would not be shown in the table.)</p>""")

    print('''<div class="container">''')
    print('<table class="stripe row-border" cellspacing="0" width="100%">')
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
    total_pageviews_by_pagepath = {}
    total_pageviews_by_month = {}
    pageviews_list_by_month = {}
    grand_total = 0
    for (y, m, pp) in data_dict:
        total_pageviews_by_pagepath[pp] = (total_pageviews_by_pagepath.get(pp, 0) +
                                           data_dict[(y, m, pp)])
        total_pageviews_by_month[(y, m)] = (total_pageviews_by_month.get((y, m), 0) +
                                            data_dict[(y, m, pp)])
        pageviews_list_by_month[(y, m)] = (pageviews_list_by_month.get((y, m), []) +
                                           [data_dict[(y, m, pp)]])
        grand_total += data_dict[(y, m, pp)]

    # Unlike the above total counts, these count only pageviews on pagepaths
    # that are in the top N pagepaths, where N=limit_pagepaths. We will find
    # them in the loop below, where we restrict using the slice [:limit_pagepaths].
    total_of_shown = 0
    total_by_month_of_shown = {}

    for pagepath, total_for_pagepath in sorted(total_pageviews_by_pagepath.items(),
                                               key=lambda x: x[1],  # sort by pageviews
                                               reverse=True)[:limit_pagepaths]:
        total_of_shown += total_for_pagepath
        print("<tr>")
        project_url = project_title_to_url[project_title]
        # pagepath already begins with a slash, so remove it from the project
        # URL if it exists
        if project_url.endswith('/'):
            project_url = project_url[:-1]
        print('''<th><a href="%s%s" title="%s">%s</a></th>''' %
              (project_url, pagepath, pagepath, abbreviated(pagepath)))
        print('''<td style="text-align: right;">{:,}</td>'''.format(total_for_pagepath))
        for month in all_months:
            y, m = month
            if (y, m, pagepath) in data_dict:
                print('''<td style="text-align: right;">{:,}</td>'''.format(data_dict[(y, m, pagepath)]))
                total_by_month_of_shown[(y, m)] = (total_by_month_of_shown.get((y, m), 0) +
                                                   data_dict[(y, m, pagepath)])
            else:
                print('''<td style="text-align: right;">0</td>''')
        print("</tr>")
    print("</tbody>")
    print("<tfoot>")
    print("<tr>")
    print("<th>Total of shown rows</th>")
    print('''<th style="text-align: right;">{:,}</th>'''.format(total_of_shown))
    for month in all_months:
        print('''<th style="text-align: right;">{:,}</th>'''.format(total_by_month_of_shown[month]))
    print("</tr>")
    print("<tr>")
    print("<th>Total</th>")
    print('''<th style="text-align: right;">{:,}</th>'''.format(grand_total))
    for month in all_months:
        print('''<th style="text-align: right;">{:,}</th>'''.format(total_pageviews_by_month[month]))
    print("</tr>")
    print("<tr>")
    print("<th>h-index</th>")
    print('''<th style="text-align: right;">n.a.</th>''')
    for month in all_months:
        print('''<th style="text-align: right;">{:,}</th>'''.format(h_index(pageviews_list_by_month[month])))
    print("</tr>")
    print("</tfoot>")
    print("</table>")
    print("</div>")


    util.print_closing()

def normalized_dict(data, project_title):
    """Returns a dictionary (year, month, pagepath) -> pageviews where pagepath
    is normalized. Normalization rules can depend on the project title."""
    result = {}
    fbclid_pat = re.compile(r'\?fbclid=[a-zA-Z0-9_-]+$')
    printable_pat = re.compile(r'\?printable=')
    for (year, month, pagepath, pageviews) in data:
        pagepath = fbclid_pat.sub('', pagepath)
        if project_title == "Cause Prioritization Wiki":
            pagepath = printable_pat.sub('', pagepath)
            pagepath = pagepath.replace(' ', '_')
        key = (year, month, pagepath)
        if key in result:
            result[key] = result[key] + pageviews
        else:
            result[key] = pageviews
    return result


def abbreviated(string):
    if len(string) < 30:
        return string
    else:
        return string[:30] + "…"


if __name__ == "__main__":
    main()
