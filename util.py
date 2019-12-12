
def print_head():
    print('''<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
      <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
      <link href="https://cdn.datatables.net/fixedcolumns/3.2.2/css/fixedColumns.dataTables.min.css" rel="stylesheet"/>
      <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
      <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/fixedcolumns/3.3.0/js/dataTables.fixedColumns.min.js"></script>
      <style type="text/css">
        table {
            font-size: 12px;
            font-family: sans-serif;
        }
        a { text-decoration: none; }
        a:hover, a:active { text-decoration: underline; }

        /* Ensure that the table scrolls;
           see https://datatables.net/extensions/fixedcolumns/examples/initialisation/two_columns.html */
        th, td { white-space: nowrap; }
        div.dataTables_wrapper {
            width: 1100px;
            margin: 0 auto;
        }
      </style>
      <title>Vipul’s Empire</title>
    </head>
    <body>
    ''')

def print_closing():
    print('''
    <script>
        $(document).ready(function() {
            var table = $('table').DataTable( {
                scrollY:        "400px",
                scrollX:        true,
                scrollCollapse: true,
                paging:         false,
                order:          false,
                fixedHeader: {
                    header: true,
                    footer: true
                },
                fixedColumns:   {
                    leftColumns: 2
                }
            } );
        } );
    </script>
    </body>
    </html>
    ''')
