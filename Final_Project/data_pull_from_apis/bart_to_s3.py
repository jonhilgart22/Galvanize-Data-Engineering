#!usr/bin/env python
# This will pull arrive times for every bart train for both directions, N and S
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=12th&key=MW9S-E7SL-26DU-VV8V
from StringIO import StringIO
import requests
from bart_station_list import bart_stations_dict
import yaml
import os
import boto3
import time
import xmltodict
import json
__author__ = 'Jonathan Hilgart'


def bart_real_time_departures_to_s3():
    """This function will return the estimated time of arrival for every bart
    train going north or south from every station. This information is
    collected inside a string and then sent to S3 to process at
     a later date. ~92 station combinations total"""
    client = boto3.client('firehose', region_name='us-east-1')
    direction_options = ['n', 's']
    for name, station_abr in bart_stations_dict.iteritems():  # every station
        for direction in direction_options:
            credentials = yaml.load(open(os.path.expanduser(
                '~/data_engineering_final_credentials.yml')))
            bart_key = credentials['bart'].get('key')
            origin_station_arg = station_abr
            direction_arg = direction
            # add in the terminal arguments to the payload for the bart api
            payload = {'cmd': 'etd', 'orig': origin_station_arg,
                       'dir': direction_arg, 'key': bart_key}
            r = requests.get('http://api.bart.gov/api/etd.aspx',
                    params = payload)
            content = r.content
            content = json.dumps(xmltodict.parse(content))
            print(json.loads(content)['root']['station']['etd'],'----')
            # client.put_record(
            #             DeliveryStreamName='bart-data-collection',
            #                    Record={'Data': content + "\n"})


if __name__ == '__main__':
    bart_real_time_departures_to_s3()
