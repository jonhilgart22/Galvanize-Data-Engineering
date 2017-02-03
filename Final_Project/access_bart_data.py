#! usr/bin/env python
#http://www.blog.pythonlibrary.org/2010/11/20/python-parsing-xml-with-lxml/
__author__='Jonathan Hilgart'
import requests
from lxml import etree
from StringIO import StringIO
import pandas as pd
import datetime
import pytz
import time
from collections import defaultdict
## Get the current time in San Francisco
SF_time = pytz.timezone('US/Pacific')
current_sf_time = datetime.datetime.now(SF_time)
date_sf , raw_time_sf= time.strftime('{}'.format(current_sf_time)).split(' ')
sf_hour,sf_minute = int(raw_time_sf[:2]), int(raw_time_sf[3:5])
print('{}:{}'.format(sf_hour,sf_minute),'Current SF time')

## Access the bart api
bart_key = 'QUZL-PQ66-9XYT-DWE9'
payload = {'cmd': 'etd', 'orig': '16th','dir':'n','key':bart_key}

#http://api.bart.gov/api/etd.aspx?cmd=etd&orig=12th&key=MW9S-E7SL-26DU-VV8V
r = requests.get('http://api.bart.gov/api/etd.aspx',\
params=payload)
content = r.content
#print(type(content)),'content'
file = open('final_project_data.txt','wr')
file.write(content)
file.close()


##parse the XML returned by the BART api
tree = etree.parse(StringIO(content))
context = etree.iterparse(StringIO(content))
minute_rows = 0
bart_df = pd.DataFrame()

def bart_xml_parser(xml_context):
    """Parse the xml for the bart api. Return two pandas dataframes.
    One that shows the arrival time (minutes) fora  destination station.
    The second that sows the number of train cars for a destination.
    If there are not three time projections for a given trainm a default estimate of 90 minutes is given."""
    destination_station=''
    destination_minutes =defaultdict(int)
    destination_train_size=defaultdict(int)
    for action, elem in context: ## go through the xml returned
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        if elem.tag =='name':
            origin_station=text
        elif elem.tag =='destination':
            destination_station=text
            destination_minutes[destination_station]=[]
            destination_train_size[destination_station]=[]
        elif elem.tag =='minutes':
            if text =='leaving': ## This train is leaving now!
                destination_minutes[destination_station].append(0)
            else:
                destination_minutes[destination_station].append(int(text))
        elif elem.tag =='length':
            destination_train_size[destination_station].append(int(text))
        print elem.tag + " => " + text
    for k,v in destination_minutes.iteritems(): # check if there are not the same number of trains coming
        if len(v)<3:
            [destination_minutes[k].append(90) for _ in range(3-len(v))]
    for k,v in destination_train_size.iteritems(): # check if there are not the same number of trains coming
        if len(v)<3:
            [destination_train_size[k].append(90) for _ in range(3-len(v))]
    destination_minutes_df = pd.DataFrame(destination_minutes)
    destination_train_size_df = pd.DataFrame(destination_train_size)
    print(destination_minutes_df , 'destination minutes df')
    print(destination_train_size_df,'train size df')
bart_xml_parser(context)
## NAME is the orig station, where the car is now, destination is where
#the train is heading


##stations
# 12th	12th St. Oakland City Center
# 16th	16th St. Mission (SF)
# 19th	19th St. Oakland
# 24th	24th St. Mission (SF)
# ashb	Ashby (Berkeley)
# balb	Balboa Park (SF)
# bayf	Bay Fair (San Leandro)
# cast	Castro Valley
# civc	Civic Center (SF)
# cols	Coliseum
# colm	Colma
# conc	Concord
# daly	Daly City
# dbrk	Downtown Berkeley
# dubl	Dublin/Pleasanton
# deln	El Cerrito del Norte
# plza	El Cerrito Plaza
# embr	Embarcadero (SF)
# frmt	Fremont
# ftvl	Fruitvale (Oakland)
# glen	Glen Park (SF)
# hayw	Hayward
# lafy	Lafayette
# lake	Lake Merritt (Oakland)
# mcar	MacArthur (Oakland)
# mlbr	Millbrae
# mont	Montgomery St. (SF)
# nbrk	North Berkeley
# ncon	North Concord/Martinez
# oakl	Oakland Int'l Airport
# orin	Orinda
# pitt	Pittsburg/Bay Point
# phil	Pleasant Hill
# powl	Powell St. (SF)
# rich	Richmond
# rock	Rockridge (Oakland)
# sbrn	San Bruno
# sfia	San Francisco Int'l Airport
# sanl	San Leandro
# shay	South Hayward
# ssan	South San Francisco
# ucty	Union City
# warm	Warm Springs/South Fremont
# wcrk	Walnut Creek
# wdub	West Dublin
# woak	West Oakland
