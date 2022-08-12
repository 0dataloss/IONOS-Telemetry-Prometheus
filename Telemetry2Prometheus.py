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
    autHead={'Authorization': 'Bearer ' + token}
    telemetryUrl="https://api.ionos.com/telemetry/api/v1/series"
    seriesResp = requests.get(telemetryUrl, headers=autHead)
    seriesRespJson=(seriesResp.json())
    extractData=seriesRespJson['data']
    singledata=[]
    for value in extractData:
        value=value['__name__']
        if str(value) in singledata:
            continue
        else:
          singledata.append(value)
    return singledata

def retrieveSeries(catalog,token):
    prometheusPagePrintadd="# This script is interrogating IONOS Telemetry API"
    autHead={'Authorization': 'Bearer ' + token}
    for serie in catalog:
        telemetryUrl="https://api.ionos.com/telemetry/api/v1/query?query=" + serie
        seriesResp = requests.get(telemetryUrl, headers=autHead)
        seriesRespJson=seriesResp.json()
        seriesRespJson=seriesRespJson['data']['result']
        for index in seriesRespJson:
          metricName=index['metric']['__name__']
          metricDc=index['metric']['dc']
          metricUuid=index['metric']['uuid']
          metricValue=index['value'][1]
          printValue=metricName + "{DCName=\""+metricDc+"\",ResourceUUID=\""+metricUuid+"\"}"+ str(metricValue)
          prometheusPagePrintadd=prometheusPagePrintadd +"\n" + printValue
    return prometheusPagePrintadd

@app.route('/metrics')
def main():
  tokenFromConfig=(config())
  catalog=(get_catalog(tokenFromConfig))
  return(retrieveSeries(catalog,tokenFromConfig))
if __name__ == '__main__':
  app.run()

