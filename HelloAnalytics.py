#!/usr/bin/env python3

# Modified from
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
"""Hello Analytics Reporting API V4."""

import datetime
import csv
import sys
import pickle
import time

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = sys.argv[1]


def main():
    try:
        print("Trying to load pickle...", file=sys.stderr)
        with open("analytics_data.pickle", "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print("Pickle not found; querying again...", file=sys.stderr)
        analytics = initialize_analyticsreporting()

        data = []

        with open(sys.argv[2], newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                # print(row['project_title'])
                data.append((row['project_title'],
                             row['url'],
                             get_pageviews_for_project(analytics, row['view_id'], 2017, 10)))
        with open("analytics_data.pickle", "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


    print_table(data)


def print_table(data):
    all_months = sorted(set.union(*[set(pageviews_dict.keys()) for _, _, pageviews_dict in data]),
                        key=lambda x: datetime.datetime.strptime(x, "%B %Y"),
                        reverse=True)
    print('''<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">

      <link rel="stylesheet" href="./tablesorter.css">
          <script src="./jquery.min.js"></script>
          <script src="./jquery.tablesorter.js"></script>
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

        </head>
        <body>
      ''')

    print("<table>")
    print("<thead>")
    print("  <tr>")
    print("  <th>Project title</th>")
    print("  <th>Total</th>")
    for month in all_months:
        print("  <th>")
        print(month)
        print("  </th>")
    print("  </tr>")
    print("</thead>")
    print("<tbody>")
    for project_title, url, pageviews_dict in data:
        print("<tr>")
        print('''<td><a href="%s">%s</a></td>''' % (url, project_title))
        print('''<td style="text-align: right;">%s</td>''' % sum(pageviews_dict.values()))
        for month in all_months:
            if month in pageviews_dict:
                print('''<td style="text-align: right;">%s</td>''' % pageviews_dict[month])
            else:
                print('''<td style="text-align: right;">n.a.</td>''')
        print("</tr>")

    print("</tbody>")
    print("</table>")
    print('''
        <script>
        $(function(){
            $("table").tablesorter();
          });
    </script>
    </body>
    </html>
    ''')



def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def last_day_of_month(year, month):
    if month == 12:
        return datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        return datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)


def get_report(analytics, view_id, start_date, end_date):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    # time.sleep(2)
    print("Doing %s %s-%s" % (view_id, start_date, end_date), file=sys.stderr)

    return analytics.reports().batchGet(
        body={
          'reportRequests': [
          {
            'viewId': view_id,
            'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
            'metrics': [{'expression': 'ga:pageviews'}],
            # 'dimensions': [{'name': 'ga:pagePath'}]
          }]
        }
    ).execute()


def get_pageviews(response):
    result = []
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)

            for i, values in enumerate(dateRangeValues):
                # print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    result.append(value)
                    # print(metricHeader.get('name') + ': ' + value)
    return result


def get_pageviews_for_project(analytics, view_id, start_year, start_month):
    result = {}

    date_ranges = []
    for year in range(start_year, 2018+1):
        if year == start_year:
            months = range(start_month, 12+1)
        else:
            months = range(1, 12+1)
        for month in months:
            year_month_name = datetime.date(year, month, 1).strftime("%B %Y")
            first_day = datetime.date(year, month, 1).strftime("%Y-%m-%d")
            last_day = last_day_of_month(year, month).strftime("%Y-%m-%d")
            date_ranges.append((year_month_name, first_day, last_day))

    for year_month_name, start_date, end_date in date_ranges:
        response = get_report(analytics, view_id, start_date, end_date)
        pageviews = get_pageviews(response)
        assert len(pageviews) <= 1, (pageviews, year, month)
        if len(pageviews) == 1:
            result[year_month_name] = int(pageviews[0])

    return result


if __name__ == '__main__':
    main()
