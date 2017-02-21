#! usr/bin/endvpython
__author__='Jonathan Hilgart'
import requests
import yaml
import os
import json


def weather_data_to_s3():
    credentials = yaml.load(open(os.path.expanduser('~/data_engineering_final_credentials.yml')))
    # SF city id 5391997
    weather_key = credentials['open_weather'].get('key')
    # units:imperial returns temp in fahrenheit
    payload = {'id':'5391997','units':'imperial','APPID':weather_key}
    # This is the id for San Francisco
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


if __name__ == "__main__":
    weather_data_to_s3()
