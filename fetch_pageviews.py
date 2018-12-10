#!/usr/bin/env python3

# Modified from
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

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
    for project in projects:
        project_title, view_id, start_date = project
        # Get the date up to which we have recorded pageviews data for this project
        cursor.execute("""select pageviews_date from pageviews where project_title = %s
                          order by pageviews_date desc limit 1""", (project_title,))
        lst = cursor.fetchall()
        if lst:
            last_date = lst[0][0] + datetime.timedelta(days=1)
        else:
            # This means we have no data for this project, so start from the
            # very beginning
            last_date = start_date

        pageviews = pageviews_for_project(analytics, view_id, last_date)
        records = [(project_title, date_string, views) for date_string, views in pageviews]

        insert_query = """insert into pageviews(project_title, pageviews_date, pageviews)
                          values (%s, %s, %s)"""
        cursor.executemany(insert_query, records)
        cnx.commit()


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
    print("Doing ViewID=%s [%s, %s] (page token: %s)" % (
                view_id, start_date, end_date, page_token), file=sys.stderr)

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


def pageviews_for_project(analytics, view_id, start_date):
    result = []
    today = datetime.date.today()
    if start_date > today:
        # This means we already have all the data up until today, so don't
        # query
        return result

    page_token = None
    while True:
        response = get_report(analytics, view_id, start_date.strftime("%Y-%m-%d"),
                              today.strftime("%Y-%m-%d"), page_token)
        result.extend(extracted_pageviews(response))
        if "nextPageToken" in response["reports"][0]:
            page_token = response["reports"][0]["nextPageToken"]
        else:
            break
    return result


if __name__ == '__main__':
    main()
