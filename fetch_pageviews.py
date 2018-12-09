#!/usr/bin/env python3

# Modified from
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
"""Hello Analytics Reporting API V4."""

import pdb
import datetime
import csv
import sys
import time
import mysql.connector

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = sys.argv[1]


def main():
    analytics = initialize_analyticsreporting()

    cnx = mysql.connector.connect(user='issa', database='analyticstable')
    cursor = cnx.cursor()

    cursor.execute("""select project_title, view_id, start_date from projects""")
    projects = cursor.fetchall()
    for project in projects[:1]:
        project_title, view_id, start_date = project
        # Get the date up to which we have recorded pageviews data for this project
        cursor.execute("""select * from pageviews where project_title = %s
                          order by pageviews_date limit 1""", (project_title,))
        lst = cursor.fetchall()
        if lst:
            last_date = lst[0][0]
        else:
            # This means we have no data for this project, so start from the
            # very beginning
            last_date = start_date

        pg = get_pageviews_for_project(analytics, view_id, last_date)
        print(get_pageviews(pg[1]))
        # pdb.set_trace()


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


def get_report(analytics, view_id, start_date, end_date, page_token=None):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    # time.sleep(2)
    print("Doing %s %s-%s" % (view_id, start_date, end_date), file=sys.stderr)

    report_dict = {
        'viewId': view_id,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'expression': 'ga:pageviews'}],

        # This makes the pageviews separated into daily granularity
        'dimensions': [{'name': 'ga:date'}],

        'pageSize': "1000",
    }

    # See https://developers.google.com/analytics/devguides/reporting/core/v4/basics#pagination
    if page_token:
        report_dict["pageToken"] = page_token

    return analytics.reports().batchGet(
        body={
          'reportRequests': [report_dict]
        }
    ).execute()


def extracted_pageviews(response):
    """Extract the GA response into a list of tuples containing pageviews data,
    e.g. [('2018-09-06', 4), ('2018-09-07', 15), ('2018-09-09', 15)]."""
    result = []
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            assert len(dimensions) == 1, dimensions

            dateRangeValues = row.get('metrics', [])
            assert len(dateRangeValues) == 1, dateRangeValues

            dim = dimensions[0]
            assert len(dim) == 8, dim

            date_string = dim[0:4] + "-" + dim[4:6] + "-" + dim[6:]

            pageviews_values = dateRangeValues[0]['values']
            assert len(pageviews_values) == 1, pageviews_values

            pageviews = int(pageviews_values[0])
            result.append((date_string, pageviews))

    return result


def get_pageviews_for_project(analytics, view_id, start_date):
    # result = {}

    # date_ranges = []
    # for year in range(start_date.year, 2018+1):
    #     if year == start_date.year:
    #         months = range(start_date.month, 12+1)
    #     else:
    #         months = range(1, 12+1)
    #     for month in months:
    #         year_month_name = datetime.date(year, month, 1).strftime("%B %Y")
    #         first_day = datetime.date(year, month, 1).strftime("%Y-%m-%d")
    #         last_day = last_day_of_month(year, month).strftime("%Y-%m-%d")
    #         date_ranges.append((year_month_name, first_day, last_day))

    # for year_month_name, start_date, end_date in date_ranges:
    #     response = get_report(analytics, view_id, start_date, end_date)
    #     pageviews = get_pageviews(response)
    #     assert len(pageviews) <= 1, (pageviews, year, month)
    #     if len(pageviews) == 1:
    #         result[year_month_name] = int(pageviews[0])

    # return result

    page_token = None

    result = []

    while True:
        response = get_report(analytics, view_id, start_date.strftime("%Y-%m-%d"),
                              "2018-12-09", page_token)

        result.append(response)

        if "nextPageToken" in response["reports"][0]:
            page_token = response["reports"][0]["nextPageToken"]
        else:
            break

    # pdb.set_trace()
    # pageviews = get_pageviews(response)

    return result


if __name__ == '__main__':
    main()
