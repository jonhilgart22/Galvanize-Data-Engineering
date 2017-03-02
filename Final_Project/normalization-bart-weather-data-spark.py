# coding: utf-8

## Here are the links to the normalized data
## weather
# 	https://s3.amazonaws.com/normalized-data-weather-bart/location2017/02/27/part-00000-0a9f0438-b65c-4d9e-b8ab-20ef1d0b37d9.csv
# 		https://s3.amazonaws.com/normalized-data-weather-bart/main-temp2017/02/27/part-00000-48bad1d8-4400-4309-8fbd-a735d4ae998b.csv
# https://s3.amazonaws.com/normalized-data-weather-bart/weather-description2017/02/27/part-00000-44f6bedd-b0cd-4e41-9590-4ce73eb28fde.csv
# 		https://s3.amazonaws.com/normalized-data-weather-bart/wind_df2017/02/27/part-00000-b02ec65e-946c-4e25-b5ce-85568f67115a.csv
## bart
# 	https://s3.amazonaws.com/normalized-data-weather-bart/bart-one-arrival2017/2/27/17/part-00000-7b169176-4c09-4fb4-b943-c328a64630d4.csv
# 	https://s3.amazonaws.com/normalized-data-weather-bart/bart-one-physical2017/2/27/17/part-00000-b3d0331e-0738-4e14-9196-2fc6d69575b3.csv

from pyspark.sql.functions import  explode, from_unixtime, from_json
from pyspark.sql import SQLContext, column
from pyspark.sql import DataFrame
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import DateType
from pyspark import SparkConf, SparkContext # for running spark-submit job
import time
import pytz
import datetime



# # when running spark-submit, need to create the spark context
sc = SparkContext()
spark = SparkSession(sc)
sqlContext = SQLContext(sc)

# get the time for saving and uploading files
yesterday = datetime.date.today()-datetime.timedelta(1)
SF_time = pytz.timezone('US/Pacific')
current_sf_time = datetime.datetime.now(SF_time)
date_sf, raw_time_sf = time.strftime('{}'.format(current_sf_time)).split(' ')
sf_hour, sf_minute = int(raw_time_sf[:2]), int(raw_time_sf[3:5])
sf_year = yesterday.year
sf_month = yesterday.month
sf_day = yesterday.day   # compute yesterday's files
if len(str(sf_month)) < 2:
    sf_month = '0'+str(sf_month)
if len(str(sf_day)) < 2:
    sf_day = '0'+str(sf_day)

## this is for the batch jobs to save the file location
KeyFileName = "{}/{}/{}".format(sf_year, sf_month, sf_day)
print(KeyFileName)
weather_path = "s3a://current-weather-data/{}/{}/{}/*/*".format(sf_year,
                                                                sf_month,
                                                                sf_day)
weather_df = spark.read.json(weather_path)
weather_description_df = weather_df.select(hour(from_unixtime("dt")
                                                ).alias('hour'),
                                           date_format(from_unixtime('dt'),
                                            'MM/dd/yyy').alias('date')
                                           , explode("weather.main"))
# weather data
main_temp_df = weather_df.select(hour(from_unixtime("dt")
            ).alias('hour'), date_format(from_unixtime('dt'),
                                        'MM/dd/yyy').alias('date'),
            "main.humidity", "main.pressure", "main.temp",
            "main.temp_max", "main.temp_min")
wind_df = weather_df .select(
    hour(from_unixtime("dt")).alias('hour'),
    date_format(from_unixtime('dt'),'MM/dd/yyy').alias('date'),
    "wind.speed", "wind.deg")
location_df = weather_df .select(
    hour(from_unixtime("dt")).alias('hour'),
    date_format(from_unixtime('dt'), 'MM/dd/yyy').alias('date'), "name")
weather_description_df.write.parquet(
    "s3a://normalized-data-weather-bart/weather-description{}".format(
        KeyFileName))
# save the weather data
main_temp_df.write.parquet(
    "s3a://normalized-data-weather-bart/main-temp{}".format(KeyFileName))
wind_df.write.parquet("s3a://normalized-data-weather-bart/wind_df{}".format(
    KeyFileName))
location_df.write.parquet("s3a://normalized-data-weather-bart/location{}".format(
    KeyFileName))
# onto bart data
bart_path = "s3a://bart-data-collection/{}/{}/{}/*/*".format(sf_year,
                                                             sf_month, sf_day)
bart_df = spark.read.json(bart_path)
bart_arrival_0 = bart_df.select(
    col("origin_station.0").alias("origin_station_0"),
    col("time.0").alias('sf_time_0'),
    col("date.0").alias("date_0"),
    col("direction.0").alias("direction_0"),
    col("destination.0").alias("destination_0"),
    hour(from_unixtime("unix_time.0")).alias("hour_0"),
    col("minutes.0").alias('minutes_til_arrival_0'))

bart_arrival_1 = bart_df.select(
    col("origin_station.1").alias("origin_station_1"),
    col("time.1").alias('sf_time_1'),
    col("date.1").alias("date_1"),
    col("direction.1").alias("direction_1"),
    col("destination.1").alias("destination_1"),
    hour(from_unixtime("unix_time.1")).alias("hour_1"),
    col("minutes.1").alias('minutes_til_arrival_1'))

bart_arrival_2 = bart_df.select(
    col("origin_station.2").alias("origin_station_2"),
    col("time.2").alias('sf_time_2'),
    col("date.2").alias("date_2"),
    col("direction.2").alias("direction_2"),
    col("destination.2").alias("destination_2"),
    hour(from_unixtime("unix_time.2")).alias("hour_2"),
    col("minutes.2").alias('minutes_til_arrival_2'))

bart_physical_0 = bart_df.select(
    col("origin_station.0").alias("origin_station_0"),
    col("time.0").alias('sf_time_0'),
    col("date.0").alias("date_0"), col("direction.0").alias("direction_0"),
    col("destination.0").alias("destination_0"),
    hour(from_unixtime("unix_time.0")).alias("hour_0"),
    col("color.0").alias("color_0"),col("bike_flag.0").alias("bike_flag_0"),
    col("train_size.0").alias("train_size_0"),
    col("capacity.0").alias("capacity_0"))

bart_physical_1 = bart_df.select(
    col("origin_station.1").alias("origin_station_1"),
    col("time.1").alias('sf_time_1'), col("date.1").alias("date_1"),
    col("direction.1").alias("direction_1"),
    col("destination.1").alias("destination_1"),
    hour(from_unixtime("unix_time.1")).alias("hour_1"),
    col("color.1").alias("color_1"),col("bike_flag.1").alias("bike_flag_1"),
    col("train_size.1").alias("train_size_1"),
    col("capacity.1").alias("capacity_1"))

bart_physical_2 = bart_df.select(
    col("origin_station.2").alias("origin_station_2"),
    col("time.2").alias('sf_time_2'),
    col("date.2").alias("date_2"),
    col("direction.2").alias("direction_2"),
    col("destination.2").alias("destination_2"),
    hour(from_unixtime("unix_time.2")).alias("hour_2"),
    col("color.2").alias("color_2"),col("bike_flag.2").alias("bike_flag_2"),
    col("train_size.2").alias("train_size_2"),
    col("capacity.2").alias("capacity_2"))
# write to csv for bart data
bart_arrival_0.write.parquet(
    "s3a://normalized-data-weather-bart/bart_arrival_0_{}".format(
        KeyFileName))
bart_arrival_1.write.parquet(
    "s3a://normalized-data-weather-bart/bart_arrival_1_{}".format(
        KeyFileName))
bart_arrival_2.write.parquet(
    "s3a://normalized-data-weather-bart/bart_arrival_2_{}".format(
        KeyFileName))
bart_physical_0.write.parquet(
    "s3a://normalized-data-weather-bart/bart_physical_0_{}".format(
        KeyFileName))
bart_physical_1.write.parquet(
    "s3a://normalized-data-weather-bart/bart_physical_1_{}".format(
        KeyFileName))
bart_physical_2.write.parquet(
    "s3a://normalized-data-weather-bart/bart_physical_2_{}".format(
        KeyFileName))
