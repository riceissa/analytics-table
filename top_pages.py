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

    assert len(sys.argv) == 1+1, "Script must be run with right number of arguments"

    project_title = sys.argv[1]
    if not project_title:
        project_title = "Vipul Naik"
    cursor.execute("""
        select
            year(pageviews_date),
            month(pageviews_date),
            pagepath,
            sum(pageviews)
        from pageviews
        where
            project_title = %s
        group by
            year(pageviews_date),
            month(pageviews_date),
            pagepath
    """, (project_title,))
    data_dict = normalized_dict(cursor.fetchall())
    all_months = sorted(set((year, month) for year, month, _ in data_dict), reverse=True)
    all_pagepaths = sorted(set(pagepath for _, _, pagepath in data_dict))

    util.print_head()

    print('''<div class="container">''')
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
    for pagepath in all_pagepaths:
        print("<tr>")
        print('''<td>%s</td>''' % pagepath)
        print('''<td></td>''')
        for month in all_months:
            y, m = month
            if (y, m, pagepath) in data_dict:
                print('''<td style="text-align: right;">{:,}</td>'''.format(data_dict[(y, m, pagepath)]))
            else:
                print('''<td style="text-align: right;">n.a.</td>''')
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
        key = (year, month, pagepath)
        if key in result:
            result[key] = result[key] + pageviews
        else:
            result[key] = pageviews
    return result


if __name__ == "__main__":
    main()
