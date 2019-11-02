<?php

if ($_REQUEST['project_title'] ?? '') {
  $project_title = $_REQUEST['project_title'];
  // Keep only printable ASCII characters. We may want to expand the allowed
  // character set later, but since our project titles only use ASCII
  // characters, this seems fine for now.
  $project_title = preg_replace('/[^[:print:]]/', '', $project_title);
} else {
  $project_title = "";
}

if ($_REQUEST['limit_pagepaths'] ?? '') {
  $limit_pagepaths = $_REQUEST['limit_pagepaths'];
  // Keep only digits.
  $limit_pagepaths = preg_replace('/[^0-9]/', '', $limit_pagepaths);
} else {
  $limit_pagepaths = "";
}

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

if ($_REQUEST['pagepath_regex'] ?? '') {
  $pagepath_regex = $_REQUEST['pagepath_regex'];
  // Keep only printable ASCII characters. We may want to expand the allowed
  // character set later.
  $pagepath_regex = preg_replace('/[^[:print:]]/', '', $pagepath_regex);
} else {
  $pagepath_regex = "";
}

// For some reason when Python is invoked through PHP, it runs into Unicode
// encoding issues when trying to print (because it defaults to some
// ASCII-only encoding). So we have to force it to use UTF-8 here.
$command = "PYTHONIOENCODING=utf-8 ../top_pages.py " . escapeshellarg($project_title) . " " . escapeshellarg($limit_pagepaths) . " " . escapeshellarg($start_date) . " " . escapeshellarg($end_date) . " " . escapeshellarg($pagepath_regex);

$output = shell_exec($command);
echo $output;
