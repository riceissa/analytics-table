# Analytics table for Vipul Naik's projects

Live at https://analytics.vipulnaik.com/

## Project layout

- `fetch_pageviews.py`: this script queries Google Analytics using its API, and
  stores the data in a local database. This script should be run in a cron job.
- `print_table.py`: this script queries the local database and prints pageviews
  data in an HTML table.
- `sql/`: table schema and some data for the local database.
- `access-portal/`: if this project is served over the web, this is where users
  will access the site.

## Database layout

The database should be named `analyticstable`.

The database has two tables:

- `projects`: this stores some metadata about each project. The data for this
  is stored directly in the SQL file.
- `pageviews`: this stores the pageviews. The data for this is inserted by
  `fetch_pageviews.py`.

## Setting up Google Analytics

There are several parts to this:

1. You must set up a project on the Google developers console. From the
   project, you will create a service account, which will have an **email
   address** associated with it as well as a **credentials JSON file**.
2. For each website tracked via Google Analytics, you must give your special
   email address access to the analytics data.
3. For each website tracked via Google Analytics, you must add the project
   metadata to `sql/projects.sql`.
4. Optional: change the Google Analytics quota.

Each step is covered below.

### Set up a Google developers project and a service account

A _project_ seems to be some sort of umbrella thing for the Google developers
console, whereas a _service account_ is a thing that gets an email. You will
create a single project and a single service account for that project.

1. Go to https://console.developers.google.com
2. Create a new project somehow (I can't go back to the screen displayed before
   I had any projects, so I can't write up the exact steps).
3. Enable analytics API for your project:
   https://www.dundas.com/support/learning/documentation/connect-to-data/how-to/connecting-to-google-analytics
4. Go to https://console.developers.google.com/iam-admin/serviceaccounts
5. Click "create service account". You can enter arbitrary stuff here; you don't
   need to give the service account any permissions.
6. Create a key for the service account. **If you're creating a new service
   account**, there should be a section called "Create key (optional)". Click
   "create key", and make sure JSON is selected. Now create the key and save it
   as `key.json` (I think Google's documentation refers to this file as `client_secrets.json`) in this repo's directory.
   **If you already have a service account**, in the table that lists your
   service accounts, there is a column called "Actions". Click the hamburger
   and select "Create key", and save as `key.json` (I think Google's documentation refers to this file as `client_secrets.json`).

### How to give access to the script

For this step, you will need the email address associated with your service
account.

From the analytics home page, you can go to admin → then under the View column
User Management → and then the (+) in the upper right corner → "Add new users"
→ and use email address for your service account, and make sure "Read &
Analyze" is checked, then click Add.

### How to find the view ID

Admin → under the View column "View Settings" → under "Basic Settings" there
should be a "View ID" heading.

### Change Google Analytics quota

1. Go to https://console.developers.google.com/iam-admin/serviceaccounts
2. In left bar, click "Quotas"
3. Under services dropdown, restrict to "Google Analytics Reporting API".
4. The one that might cause problems is "Google Analytics Reporting API - Requests
   per 100 seconds", so click that, and in the next screen you can click the
   pencil to change it up to 50,000.

## Setting up the portal

### Set up the database

```bash
# Create database
mysql -e "create database analyticstable"

# Create tables
mysql analyticstable < sql/projects.sql
mysql analyticstable < sql/pageviews.sql
mysql analyticstable < sql/path_pageviews.sql
```

### Create login file

In this repo's directory, create a file called `login.py` with the database login info.
For example:

```python
USER = "issa"
DATABASE = "analyticstable"
PASSWORD = ""
```

### Install Google Analytics API library and MySQL connector

Run:

```bash
sudo pip install --upgrade google-api-python-client mysql-connector-python oauth2client
```

([source](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py#2_install_the_client_library))

### Run the data fetching script

If everything is set up correctly, you should now be able to run the data
fetching script:

```bash
./fetch_pageviews.py key.json
```

If it works, try running it again:

```bash
./fetch_pageviews.py key.json
```

The script checks the most recently stored date for each project, and only
queries for more recent data, so the second run should be much quicker. (If a
website got zero pageviews on the most recent days, it might try to query a
small number of dates.)

### Fetch auxiliary files

```bash
make fetch_tablesorter
```

### Serve the website

If you're trying to run the website locally, run from the `access-portal/` directory:

```bash
php -S localhost:8000
```

If you're trying to serve the website over the web, edit your nginx/apache
config; make sure the root directory is `access-portal/`.

## See also

- https://github.com/riceissa/timelines-wiki-main-page-table
