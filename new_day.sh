#!/bin/sh

year="$1"
day="$2"
dir=$(dirname $0)

if [ -z "$year" ] || [ -z "$day" ]; then
  echo "Usage: $0 <year> <day>"
  exit 1
fi

base="${year}_${day}"

dest="$dir/${base}.py"

# check if desktop file exists
if [ -f "$dest" ]; then
  echo "File $dest already exists"
  exit 1
fi

cp "$dir/template.py" "$dest"
touch "$dir/${base}.txt"
touch "$dir/${base}_sample.txt"
