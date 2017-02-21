#!usr/bin/end python
# This will pull arrive times for every bart train for both directions, N and S
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=12th&key=MW9S-E7SL-26DU-VV8V
from StringIO import StringIO
import requests
import argparse
from bart_station_list import bart_stations_dict
import yaml
from lxml import etree
import os
import boto3
import pytz
import datetime
import time
__author__ = 'Jonathan Hilgart'


def bart_real_time_departures_to_s3():
    """This function will return the estimated time of arrival for every bart
    train going north or south from every station. This information is
    collected inside a string and then sent to S3 to process at
     a later date. ~92 station combinations total"""
    client = boto3.client('firehose', region_name='us-east-1')
    direction_options = ['n', 's']
    all_bart_stations = ''
    for name, station_abr in bart_stations_dict.iteritems():  # every station
        for direction in direction_options:
            print(station_abr, direction)
            credentials = yaml.load(open(os.path.expanduser(
                '~/data_engineering_final_credentials.yml')))
            bart_key = credentials['bart'].get('key')
            origin_station_arg = station_abr
            direction_arg = direction
            # add in the terminal arguments to the payload for the bart api
            payload = {'cmd': 'etd', 'orig': origin_station_arg,
                       'dir': direction_arg, 'key': bart_key}
            r = requests.get('http://api.bart.gov/api/etd.aspx',
            params=payload)
            content = r.content
            all_bart_stations += content+'|||'  ## to split on later
            client.put_record(
                        DeliveryStreamName='bart-data-collection',
                        Record={'Data': all_bart_stations})



if __name__ == '__main__':
    bart_real_time_departures_to_s3()
