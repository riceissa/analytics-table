#!/usr/bin/env python3

# Originally modified from
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
# When switching from Universal Analytics (Reporting API v4) to Google
# Analytics 4 (Data API v1), I also referred to
# https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries

import datetime
import sys
import mysql.connector
import time

import login

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)


KEY_FILE_LOCATION = sys.argv[1]
LIMIT = 10000


def main():
    client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_LOCATION)

    cnx = mysql.connector.connect(user=login.USER, database=login.DATABASE,
                                  password=login.PASSWORD)
    cursor = cnx.cursor()

    cursor.execute("""select project_title, property_id, ga4_start_date from projects where property_id is not null""")
    projects = cursor.fetchall()

    # Google Analytics records pageviews for partial days, so make sure that we
    # only get fully completed days by setting the upper limit to four days
    # ago (to deal with potential timezone differences).
    upper_limit_date = datetime.date.today() - datetime.timedelta(days=4)

    # Fetch data into the pageviews table.
    for project in projects:
        project_title, property_id, ga4_start_date = project
        # Get the date up to which we have recorded pageviews data for this project
        cursor.execute("""select pageviews_date from pageviews where project_title = %s
                          order by pageviews_date desc limit 1""", (project_title,))
        lst = cursor.fetchall()
        if lst:
            last_date = lst[0][0] + datetime.timedelta(days=1)
        else:
            # This means we have no data for this project, so start from the
            # very beginning
            last_date = ga4_start_date

        try:
            pageviews = pageviews_for_project(client, property_id, "pageviews",
                                          last_date, upper_limit_date)
            records = [(project_title, date_string, views) for date_string, views in pageviews]

            insert_query = """insert into pageviews(project_title, pageviews_date, pageviews)
                              values (%s, %s, %s)"""
            cursor.executemany(insert_query, records)

        except Exception as e:
            print(f"!!! Error getting data for project: { project_title }")
            print(repr(e))

        cnx.commit()

    # Fetch data into the path_pageviews table.
    for project in projects:
        project_title, view_id, ga4_start_date = project
        # Get the date up to which we have recorded pageviews data for this project
        cursor.execute("""select pageviews_date from path_pageviews where project_title = %s
                          order by pageviews_date desc limit 1""", (project_title,))
        lst = cursor.fetchall()
        if lst:
            last_date = lst[0][0] + datetime.timedelta(days=1)
        else:
            # This means we have no data for this project, so start from the
            # very beginning
            last_date = ga4_start_date

        # It seems that if we try to query-and-insert too many days' worth of
        # pageviews data at a time, Google Analytics starts putting "(other)"
        # entries. So we will define a partial_progress_chunk_size that
        # specifies the maximum number of days' worth of data we will try to
        # query-and-insert at once. This will also allow us to save partial
        # progress. Of course, if last_date is very recent, this limit will
        # have no effect. See
        # https://support.google.com/analytics/answer/1009671?hl=en for more
        # about "(other)".
        partial_progress_chunk_size = 50

        lo = last_date
        hi = min(lo + datetime.timedelta(days=partial_progress_chunk_size),
                 upper_limit_date)

        while True:
            print("For %s (%s), querying and inserting from %s to %s (inclusive)" % (
                        project_title, view_id, lo.strftime("%Y-%m-%d"),
                        hi.strftime("%Y-%m-%d")), file=sys.stderr)
            pageviews = pageviews_for_project(client, view_id,
                                              "path_pageviews", lo, hi)
            records_ = [(project_title, date_string, pagepath, views)
                        for date_string, pagepath, views in pageviews]
            records = []
            for record in records_:
                (project_title, date_string, pagepath, views) = record
                # In order to be able to use pagepath as part of the "unique key"
                # in MySQL, we need to limit its varchar length. But if we do that,
                # sometimes there are pagepaths that are too long. These almost
                # always have low pageviews and are accidental/joke paths, so not
                # recording them in the database should cause no problems.
                if len(pagepath) > 500:
                    print("Too long pagepath: %s, %s, %s" % (project_title, date_string, pagepath),
                          file=sys.stderr)
                else:
                    records.append(record)

            insert_query = """insert into path_pageviews(
                                  project_title,
                                  pageviews_date,
                                  pagepath,
                                  pageviews
                              ) values (%s, %s, %s, %s)"""
            cursor.executemany(insert_query, records)
            cnx.commit()

            if hi == upper_limit_date:
                break

            lo = hi + datetime.timedelta(days=1)
            hi = min(lo + datetime.timedelta(days=partial_progress_chunk_size),
                     upper_limit_date)


def get_report(client, property_id, table, start_date, end_date, offset=0):
    """Queries the Google Analytics 4 Data API v1."""
    print("Doing PropertyID=%s [%s, %s] (offset: %s)" % (
                property_id, start_date, end_date, offset), file=sys.stderr)

    # For pagination, see
    # https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination

    if table == "pageviews":
        # This makes the pageviews separated into daily granularity
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            offset=offset,
            limit=LIMIT,
        )
    elif table == "path_pageviews":
        # This makes the pageviews separated into daily granularity for each
        # pagepath
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date"), Dimension(name="pagePathPlusQueryString")],
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            offset=offset,
            limit=LIMIT,
        )
    else:
        raise ValueError("Please specify a valid MySQL table.")
    response = client.run_report(request)
    return response


def extracted_pageviews(response):
    """Extract the GA response into a list of tuples containing pageviews data,
    e.g. [('2018-09-06', 4), ('2018-09-07', 15), ('2018-09-09', 15)]."""
    result = []
    for row in response.rows:
        dimensions = row.dimension_values  # the date and/or pagepath

        dim = dimensions[0].value
        assert len(dim) == 8, dim

        date_string = dim[0:4] + "-" + dim[4:6] + "-" + dim[6:]  # convert date to YYYY-MM-DD
        if len(dimensions) == 2:
            pagepath = dimensions[1].value
        else:
            pagepath = None

        pageviews_values = row.metric_values
        assert len(pageviews_values) == 1, pageviews_values

        pageviews = int(pageviews_values[0].value)
        if pagepath:
            result.append((date_string, pagepath, pageviews))
        else:
            result.append((date_string, pageviews))

    return result


def pageviews_for_project(client, property_id, table, start_date, end_date):
    result = []
    if start_date > end_date:
        # This means we already have all the most recent data, so don't query
        return result

    offset = 0
    while True:
        time.sleep(1)
        response = get_report(client, property_id, table, start_date.strftime("%Y-%m-%d"),
                              end_date.strftime("%Y-%m-%d"), offset)
        result.extend(extracted_pageviews(response))
        offset += LIMIT
        if offset >= response.row_count:
            # The comparison >= is the correct one here (not >) because
            # the first row is considered row 0 according to
            # https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.offset
            # So e.g. if there are five rows, they will be rows 0,1,2,3,4, and
            # if offset is >=5 then there will be no more rows to fetch. (I
            # also empirically checked that this is the actual behavior of the
            # API.)
            break
    return result


if __name__ == '__main__':
    main()
