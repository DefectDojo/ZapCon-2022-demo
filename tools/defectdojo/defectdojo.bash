#!/bin/bash

TOOLS="/app/tools"
REPORTS="/opt/reports/imports"
DOJO_IP=$(cat /app/tools/ip.conf | tail -n 1)

# Copy the reports directory over to the defectdojo area
cp -r $REPORTS $TOOLS/defectdojo/
# Move the defectdojo tooling
cd $TOOLS/defectdojo
# Install requests
pip3 install requests
# Run the importer
python3 dojo_import.py \
--url "http://$DOJO_IP" \
--token "API_KEY" \
--project_name "Juice Shop"

cp -r $TOOLS/defectdojo/imports /opt/reports
rm -rf $TOOLS/defectdojo/imports