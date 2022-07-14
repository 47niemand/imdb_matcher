#!/bin/sh

# This script extracts the data from the video files in the given directory.
# The data is stored in a file called "{file}.info".
# The data output is in text format.
#
# It requires the following programs:
# pip3 install hachoir

for file in $1/*
do
  case "$file" in
    (*.mp4 | *.avi | *.mkv | *.mov | *.wmv | *.flv | *.mpg | *.mpeg) 
    echo "Processing $file"
    hachoir-metadata "$file" > $file.info
    ;;
  esac 
done
