# Analytics table for Vipul Naik's projects

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
3. Go to https://console.developers.google.com/iam-admin/serviceaccounts
4. Click "create service account". You can enter arbitrary stuff here; you don't
   need to give the service account any permissions.
5. Create a key for the service account. **If you're creating a new service
   account**, there should be a section called "Create key (optional)". Click
   "create key", and make sure JSON is selected. Now create the key and save it
   as `key.json` in this repo's directory.
   **If you already have a service account**, in the table that lists your
   service accounts, there is a column called "Actions". Click the hamburger
   and select "Create key", and save as `key.json`.

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

coming soon
