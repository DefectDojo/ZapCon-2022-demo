# ZapCon-2022-demo
Code used in the demo from the "Final Frontier: Automating DYNAMIC Security Testing"

## Setting Up

Start DefectDojo and Juice Shop first

`docker-compose -f prequistes.yml up -d`

Access DefectDojo on 127.0.0.1:8888 with the credentials below 
```
U - admin
P - DefectDojo!0
```

Find the API key by visiting

`127.0.0.1:8888/api/key-v2`

And insert it on line 16 of `tools/defectdojo/defectdojo.bash`

Access Juice Shop on  127.0.0.1:3000 

## Running

In an environment that has docker and docker compose, run the line below and watch the following happen

1. Scan Juice Shop with SSLyze and ZAP
2. Push those results to DefectDojo
3. Clean up all the evidence (Remove scan containers and volumes)

`./demo.bash`