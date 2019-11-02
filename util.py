
def print_head():
    print('''<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
      <link rel="stylesheet" href="/tablesorter.css">
      <script src="/jquery.min.js"></script>
      <script src="/jquery.tablesorter.js"></script>
      <style type="text/css">
        body { }
        /*
         Freezing the first column and row, from https://stackoverflow.com/a/50516259/3422337
        */
        div.container {
          max-width: 100%;
          max-height: 500px;
          overflow: scroll;
        }
        thead th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          top: 0;
        }
        thead th:first-child {
          left: 0;
          z-index: 1;
        }
        tbody th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          left: 0;
        }


        table {
          font-size: 12px;
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
      <title>Vipul’s Empire</title>
    </head>
    <body>
    ''')

def print_closing():
    print('''
        <script>
        $(function(){
            $("table").tablesorter({
                sortInitialOrder: "desc"
            });
          });
    </script>
    </body>
    </html>
    ''')
