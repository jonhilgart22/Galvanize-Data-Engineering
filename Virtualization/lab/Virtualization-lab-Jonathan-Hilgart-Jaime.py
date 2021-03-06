
# coding: utf-8
import os
import yaml
import pandas as pd
from twitter import *
credentials = yaml.load(open(os.path.expanduser('~/api_credentials.yml')))
def top_n_tweets_us(n):
    """Return the top 10 tweets from the US"""
    t = Twitter(
    auth=OAuth(credentials['twitter'].get('token'), credentials['twitter'].get('token_secret'),\
               credentials['twitter'].get('consumer_key'),credentials['twitter'].get('consumer_secret')))
    us_trends = t.trends.place(_id=23424977)
    trending_tweets_us = pd.DataFrame([i for i in us_trends[0]['trends']])
    trending_tweets_us = trending_tweets_us.sort_values(by='tweet_volume',ascending=False)
    return trending_tweets_us[:n].to_html('top10.html')
error_html = """
<html>
  <head><title>Something is wrong</title></head>
  <body><h2>Something is terribly wrong with my S3-based website</h2></body>
</html>"""
Html_file= open("error.html","w")
Html_file.write(error_html)
Html_file.close()
index_html = top_n_tweets_us(10)
Html_file= open("index.html","w")
Html_file.write(index_html)
Html_file.close()
