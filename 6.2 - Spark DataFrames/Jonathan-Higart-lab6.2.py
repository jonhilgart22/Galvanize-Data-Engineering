
# coding: utf-8

# In[34]:

from pyspark.sql.functions import split, explode


# In[3]:

spark_session = SparkSession     .builder     .appName("Python Spark SQL basic example")     .config("spark.some.config.option", "some-value")     .getOrCreate()


# In[6]:

dataframe_spark = spark_session.read.json("s3a://twitter-streaming02062017/twitter2017/02/23/02/twitter-streaming-data-1-2017-02-23-02-00-14-8fd5961f-e8fa-4ca5-aa5f-bc35c7e4ac2d")


# In[7]:

dataframe_spark.printSchema()


# In[21]:

dataframe_spark.selectExpr('id as tweet_id', 'timestamp_ms', 'user.id AS user_id', 'text').show()


# In[58]:

user_dataframe = dataframe_spark.selectExpr('user.id','user.name').distinct()
user_dataframe.show()


# In[50]:

tweet_dataframe = dataframe_spark.selectExpr('entities.hashtags.text as hashtags', 'id as tweet_id')
tweet_dataframe.show()


# In[62]:

exploded_tweet_dataframe = tweet_dataframe.select(tweet_dataframe['tweet_id'],explode(tweet_dataframe.hashtags).alias("hashtags"))
exploded_tweet_dataframe.show()


# In[66]:

#write parquet
exploded_tweet_dataframe.write.parquet("s3a://twitter-streaming02062017/parquet_files/exploded_tweet_dataframe.parquet")


# In[65]:

#Parquet
tweet_dataframe.write.parquet("s3a://twitter-streaming02062017/parquet_files/tweet_dataframe.parquet")
user_dataframe.write.parquet("s3a://twitter-streaming02062017/parquet_files/user_dataframe.parquet")


# In[ ]:



