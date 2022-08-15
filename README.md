# IONOS-Telemetry-Prometheus
This Python script has been written with the scope of transforming the information
from the IONOS Telemetry API which are in JSON, to the Prometheus Ingestion Format.

The IONOS Telemetry API is compatible with Grafana, but exposes only 14 days worth
of metrics.
With this script you will be able to record all the metric in a Prometheus server 
of your choice and keep metrics for as long as you like

How to run it:
In the same directory of the script create a file ionos.py containing the following line and a valid token:
token="<your token>"

Or, export the environment variable:
IONOS_TOKEN="<your token>"


The script will run on 127.0.0.1 on port 5000 
This behavior can be changed adding some options for app.run()
For example app.run(host="localhost", port=8000, debug=True)

