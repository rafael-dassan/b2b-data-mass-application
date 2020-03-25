#!/bin/bash

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
dir_logs="$dir_path/logs"
file_debug="$dir_logs/debug.log"

# Check for the logs dir, if not found create it using `mkdir`
[ ! -d "$dir_logs" ] && mkdir -p "$dir_logs"

# Check for the debug.log file, if not found create it using `touch`
[ ! -e "$file_debug" ] && touch "$file_debug"

# Init
python3 main.py