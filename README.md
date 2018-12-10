# Analytics table for Vipul Naik's projects

TODO:

- add instructions for generating email address to add to GA accounts

## Project layout

- `fetch_pageviews.py`: this script queries Google Analytics using its API, and
  stores the data in a local database. This script should be run in a cron job.
- `print_table.py`: this script queries the local database and prints pageviews
  data in an HTML table.
- `sql/`: table schema and some data for the local database.
- `access-portal/`: if this project is served over the web, this is where users
  will access the site.

## Database layout

## How to give access to the script

from the analytics home page, you can go to admin -> then under the View column User Management -> and then the (+) in the upper right corner -> "Add new users" -> and use email address above, and make sure "Read & Analyze" is checked, then click Add

## How to find the view ID

admin -> under the View column "View Settings" -> under "Basic Settings" there should be a "View ID" heading
