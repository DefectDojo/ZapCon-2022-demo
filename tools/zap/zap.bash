#!/bin/bash

DOJO_SCAN_NAME="ZAP Scan"
REPORTS="/opt/reports/imports"
DIR="$REPORTS/to_do/$DOJO_SCAN_NAME"
FILE_NAME="$(cat /proc/sys/kernel/random/uuid).xml"

# Create the tool directory if needed
if [ ! -d "$DIR" ]; then
  mkdir -p "$DIR"
fi

cd "$DIR"
JUICE_IP=$(cat /zap/wrk/ip.conf | head -n 1)

# Run the tool here where the dojo uploader expects it
time zap-baseline.py -t "http://$JUICE_IP" --autooff -x $FILE_NAME

# Move the report to the correct location
mv /zap/wrk/"$FILE_NAME" "$DIR"
# Remove zap.out as precaution
rm -f "$DIR"/zap.out

exit 0