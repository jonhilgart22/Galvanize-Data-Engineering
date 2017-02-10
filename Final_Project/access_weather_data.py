#! usr/bin/end python
__author__='Jonathan Hilgart'
import requests
import yaml
import os
import json
credentials = yaml.load(open(os.path.expanduser('~/data_engineering_final_credentials.yml')))
# SF city id 5391997
weather_key = credentials['open_weather'].get('key')
# units:imperial returns temp in fahrenheit
payload = {'id':'5391997','units':'imperial','APPID':weather_key}
#http://api.bart.gov/api/etd.aspx?cmd=etd&orig=12th&key=MW9S-E7SL-26DU-VV8V
r = requests.get('http://api.openweathermap.org/data/2.5/weather',\
params=payload)
content = json.loads(r.content)
print(content,'all content')
print([weather['main'] for weather in content['weather']],'total weather')
print([weather['id'] for weather in content['weather']],'weather codes')
sf_wind_speed = content['wind']['speed']
print(sf_wind_speed,'sf wind speed')
current_sf_temp = content['main']['temp']
print(current_sf_temp,'msf temp')
