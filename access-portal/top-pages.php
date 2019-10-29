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

// For some reason when Python is invoked through PHP, it runs into Unicode
// encoding issues when trying to print (because it defaults to some
// ASCII-only encoding). So we have to force it to use UTF-8 here.
$command = "PYTHONIOENCODING=utf-8 ../top_pages.py " . escapeshellarg($project_title);

$output = shell_exec($command);
echo $output;
