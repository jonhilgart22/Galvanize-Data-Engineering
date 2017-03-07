#! usr/bin/env python
import os
import yaml
from pymongo import MongoClient
from boto3 import client
import pytz
import datetime
import time
import boto
import boto.s3
import sys
from boto.s3.key import Key
__author__ = 'Jonathan Hilgart'

# get the time for saving and uploading files

SF_time = pytz.timezone('US/Pacific')
yesterday = datetime.datetime.now(SF_time)-datetime.timedelta(1)
today = datetime.datetime.now(SF_time)

date_sf, raw_time_sf = time.strftime('{}'.format(today)).split(' ')
sf_hour, sf_minute = int(raw_time_sf[:2]), int(raw_time_sf[3:5])

sf_year_yesterday = yesterday.year
sf_month_yesterday = yesterday.month
sf_day_yesterday = yesterday.day   # compute yesterday's files

if len(str(sf_month_yesterday)) < 2:
    sf_month_yesterday = '0'+str(sf_month_yesterday)
if len(str(sf_day_yesterday)) < 2:
    sf_day_yesterday = '0'+str(sf_day_yesterday)

# compute today's time
sf_year_today = today.year
sf_month_today = today.month
sf_day_today = today.day   # compute yesterday's files
# to make the naming convention of kinesis
if len(str(sf_month_today)) < 2:
    sf_month_today = '0'+str(sf_month_today)
if len(str(sf_day_today)) < 2:
    sf_day_today=  '0'+str(sf_day_today)
# connect to s3 via boto
s3_connection = boto.connect_s3()
bucket = s3_connection.get_bucket('normalized-data-weather-bart')

# get all of the data from s3 for yesterday's normalized data
bart_arrival_key = bucket.get_all_keys(
    prefix="bart_arrival_0_csv{}/{}/{}/part".format(
     sf_year_yesterday, sf_month_yesterday, sf_day_yesterday))

bart_arrival_key_name = ''
for k in bart_arrival_key:
    bart_arrival_key_name = k.name

bart_physical_key = bucket.get_all_keys(
    prefix="bart_physical_0_csv{}/{}/{}".format(
    sf_year_yesterday,sf_month_yesterday,sf_day_yesterday))

bart_physical_key_name = ''
for k in bart_physical_key:
    bart_physical_key_name = k.name

weather_main_temp_key = bucket.get_all_keys(
    prefix="main-temp-csv-{}/{}/{}".format(
    sf_year_yesterday,sf_month_yesterday,sf_day_yesterday))

weather_main_temp_key_name = ''
for k in weather_main_temp_key:
    bweather_main_temp_key_name = k.name

weather_wind_key = bucket.get_all_keys(
    prefix="wind_df-csv{}/{}/{}".format(
    sf_year_yesterday, sf_month_yesterday, sf_day_yesterday))

weather_wind_key_name = ''
for k in weather_wind_key:
    weather_wind_key_name = k.name



def insert_into_mongo(bart_arr_key,bart_phy_key,weather_main_temp_key
                      ,weather_wind_key,bucket_s3):
    """Take in the mongo db buckets and push their contents to mongo.
    Returns a success message if everything works"""
    ## connect to mongo db
    client_mongo = MongoClient()
    db_weather_bart = client_mongo.weather_bart # name of the database

    # db_bart_physical = client_mongo.bart_physical
    # # db_weather_description = client_mongo.weather_location
    # db_weather_main_temp = client_mongo.weather_main_temp
    # db_weather_wind = client_mongo.weather_wind
#
    ## insert into mongo db
    bart_arrival_info = bucket_s3.get_key(bart_arr_key).get_contents_as_string
    db_weather_bart.bart_arrival.insert(bart_arrival_info)

    bart_physical_info = bucket_s3.get_key(bart_phy_key).get_contents_as_string
    db_weather_bart.bart_physical.insert(art_physical_info)

    weather_main_temp_key_info = bucket_s3.get_key(
        weather_main_temp_key).get_contents_as_string
    db_weather_bart.weather_main_temp.insert(weather_main_temp_key_info)

    weather_wind_key_info = bucket_s3.get_key(
        weather_wind_key).get_contents_as_string
    db_weather_bart.weather_wind.insert(weather_wind_key_info)

    return 'Everything pushed to mongo'

if __name__ == '__main__':
    insert_into_mongo(bart_arrival_key_name,
                    bart_physical_key_name,
                     weather_main_temp_key,
                      weather_wind_key_name,
                      bucket)
