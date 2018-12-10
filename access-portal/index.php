<?php

$command = "PYTHONIOENCODING=utf-8 ../print_table.py ";
$output = shell_exec($command);
echo $output;
