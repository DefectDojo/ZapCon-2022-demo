#!/bin/bash

DOJO_SCAN_NAME="Sslyze Scan"
REPORTS="/opt/reports/imports"
DIR="$REPORTS/to_do/$DOJO_SCAN_NAME"
FILE_NAME="$(cat /proc/sys/kernel/random/uuid).json"


# Create the tool directory if needed
if [ ! -d "$DIR" ]; then
  mkdir -p "$DIR"
fi

cd "$DIR"
JUICE_IP=$(cat /app/tools/ip.conf | head -n 1)
echo "Upgrading sslyze" 
/usr/local/bin/python -m pip install --force-reinstall sslyze
echo "Running sslyze"
# Run the tool here where the dojo uploader expects it
/usr/local/bin/python -m sslyze $JUICE_IP --json_out=$FILE_NAME

exit 0