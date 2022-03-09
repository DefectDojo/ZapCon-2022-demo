#!/bin/bash

# Add IP address of dojo and juice shop to ip.conf
echo "`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' juice-shop`:3000" > tools/ip.conf
echo "`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' defectdojo`:8888" >> tools/ip.conf
# Run the tess
docker-compose -f run_tests.yml up -d
# Wait until 
echo 'Wait unitl ZAP is finished running'
docker wait zap
# Remove the scanners
docker-compose -f run_tests.yml down
# Import results to dojo and clean the rest
docker-compose -f data_gather_clean.yml up -d
docker wait dojo_import
# Remove the importer and volumes
docker-compose -f data_gather_clean.yml down
docker volume rm zapcon-2022-demo_scan_data