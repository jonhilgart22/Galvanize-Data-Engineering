#! usr/bin/env python
from twitter import *
import os
import yaml
import psycopg2
import json
#credentials
credentials = yaml.load(open(os.path.expanduser('~/.ssh/api_credentials.yml')))
#authenticate with Twitter
twitter_stream = TwitterStream(auth=OAuth(credentials['twitter'].get('token'),\
 credentials['twitter'].get('token_secret'),\
               credentials['twitter'].get('consumer_key'),credentials['twitter'].get('consumer_secret')))

# end point for RDS system
database_endpoint = "twitter-streaming-tweets.cbx9xkfcpnfu.us-west-2.rds.amazonaws.com"
db_credentials = credentials['postgresstwitter'].get('db_name')
db_user = credentials['postgresstwitter'].get('user')
db_password=credentials['postgresstwitter'].get('password')
##connect to postgress
conn = psycopg2.connect(dbname=db_credentials,\
user=db_user,\
host=database_endpoint,\
password=db_password)
cur = conn.cursor()
# try:
#     cur.execute("""SELECT * from raw_tweets""")
# except:
#     print "I can't SELECT from bar"



sample=twitter_stream.statuses.sample()
### run through the tweets
while True:
    t = next(sample)
    try:
        print(t['delete']) ### this will find deleted tweets
    except:
        pass ### we want to insert into the database here (not deletions)
    ## insert item into the database
    #in case the while break
