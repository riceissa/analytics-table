<?php

if ($_REQUEST['start_date'] ?? '') {
  $start_date = $_REQUEST['start_date'];
  $start_date = preg_replace('/[^0-9-]/', '', $start_date);
} else {
  $start_date = "";
}

if ($_REQUEST['end_date'] ?? '') {
  $end_date = $_REQUEST['end_date'];
  $end_date = preg_replace('/[^0-9-]/', '', $end_date);
} else {
  $end_date = "";
}

if (($start_date != "") || ($end_date != "")) {
  $command = "PYTHONIOENCODING=utf-8 ../print_table.py " . escapeshellarg($start_date) . " " . escapeshellarg($end_date);
} else {
  $command = "PYTHONIOENCODING=utf-8 ../print_table.py ";
}
$output = shell_exec($command);
echo $output;
