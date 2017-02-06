#! usr/bin/env python
from twitter import *
import os
import yaml
import json
import boto3
#credentials
credentials = yaml.load(open(os.path.expanduser('~/.ssh/api_credentials.yml')))
#authenticate with Twitter
twitter_stream = TwitterStream(auth=OAuth(**credentials['twitter']))
#use boto here
client = boto3.client('firehose',region_name='us-east-1')
##get Twitter tweets
sample=twitter_stream.statuses.sample()
while True:
    for tweet in sample:
        try:
            tweet['delete'] ### this will find deleted tweets and not insert them into
            print('Found a deleted tweet')
        except:
            try:
                client.put_record(
                            DeliveryStreamName='twitter-streaming-data',
                            Record={'Data': json.dumps(str(tweet)+'\n')})
                print('wrote a tweet!')
            except:
                pass
print('Exited the while loop')