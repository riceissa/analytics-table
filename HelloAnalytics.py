#!/usr/bin/env python3

# Modified from
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
"""Hello Analytics Reporting API V4."""

import datetime
import sys
import pprint

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = sys.argv[1]
VIEW_ID = sys.argv[2]


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


def get_report(analytics, start_date, end_date):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """

    return analytics.reports().batchGet(
        body={
          'reportRequests': [
          {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
            'metrics': [{'expression': 'ga:pageviews'}],
            # 'dimensions': [{'name': 'ga:pagePath'}]
          }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
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
                print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)
                    print("=====")


def main():
    analytics = initialize_analyticsreporting()

    start_year = 2017
    start_month = 10
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
        response = get_report(analytics, start_date, end_date)
        # print(type((response)))
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(response)
        print(year_month_name)
        print_response(response)

if __name__ == '__main__':
    main()
