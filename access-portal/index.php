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

if ($_REQUEST['title_regex'] ?? '') {
  $title_regex = $_REQUEST['title_regex'];
  // Keep only printable ASCII characters. We may want to expand the allowed
  // character set later, but since our project titles only use ASCII
  // characters, this seems fine for now.
  $title_regex = preg_replace('/[^[:print:]]/', '', $title_regex);
} else {
  $title_regex = "";
}

// For some reason when Python is invoked through PHP, it runs into Unicode
// encoding issues when trying to print (because it defaults to some
// ASCII-only encoding). So we have to force it to use UTF-8 here.
$command = "PYTHONIOENCODING=utf-8 ../print_table.py " . escapeshellarg($start_date) . " " . escapeshellarg($end_date) . " " . escapeshellarg($title_regex);

$output = shell_exec($command);
echo $output;
