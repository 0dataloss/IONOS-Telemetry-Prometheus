#!/bin/python3
import sys
from urllib import request
import requests
import os
from flask import Flask
app = Flask(__name__)

def config():
  # Read Env Variables
  if os.getenv('IONOS_TOKEN'):
    token=os.getenv('IONOS_TOKEN')
  else:
    # File Exist so  Import .ionos.py
    if os.path.exists("ionos.py"):
      sys.path.append("ionos")
      import ionos as i
      token=i.token
    else:
      print("You can create a configuration file in your home directory\n"
      "This will make easy to run the script.\n"
      "Create the file ionos.py in this same directory with content:\n\n"
      "token=\"<replace with your username>\"\n")
  return token

def get_catalog(token):
    # Build Auth Headers
    autHead={'Authorization': 'Bearer ' + token}
    # Set URL for request
    telemetryUrl="https://api.ionos.com/telemetry/api/v1/series"
    # Execute Request
    seriesResp = requests.get(telemetryUrl, headers=autHead)
    # Extract Data and build list of unique values
    seriesRespJson=(seriesResp.json())
    extractData=seriesRespJson['data']
    singledata=[]
    for value in extractData:
        value=value['__name__']
        if str(value) in singledata:
            continue
        else:
          singledata.append(value)
    # Return List
    return singledata

def retrieveSeries(catalog,token):
    # Prepare Prometheus Help Line
    prometheusPagePrintadd="# This script is interrogating IONOS Telemetry API More Info to Come"
    # Prepare Auth Headers
    autHead={'Authorization': 'Bearer ' + token}
    # Send a query for each Item in List singleData
    for serie in catalog:
        telemetryUrl="https://api.ionos.com/telemetry/api/v1/query?query=" + serie
        seriesResp = requests.get(telemetryUrl, headers=autHead)
        seriesRespJson=seriesResp.json()
        # Extract the data
        seriesRespJson=seriesRespJson['data']['result']
        # Loop inside the list of Items (Servers and what not)
        for index in seriesRespJson:
          metricName=index['metric']['__name__']
          metricDc=index['metric']['dc']
          metricUuid=index['metric']['uuid']
          metricValue=index['value'][1]
          # Prepare the string Prometheus Likes
          printValue=metricName + "{DCName=\""+metricDc+"\",ResourceUUID=\""+metricUuid+"\"}"+ str(metricValue)
          # Arrange all the string together
          prometheusPagePrintadd=prometheusPagePrintadd +"\n" + printValue
    # Print all the strings as a single page
    return prometheusPagePrintadd

# Define and star the Flask server on port 5000

@app.route('/metrics')
def main():
  tokenFromConfig=(config())
  catalog=(get_catalog(tokenFromConfig))
  return(retrieveSeries(catalog,tokenFromConfig))
if __name__ == '__main__':
  app.run()

