from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import  explode, from_unixtime, from_json
from pyspark.sql import SQLContext, column, SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import DateType
from pyspark import SparkConf, SparkContext  # for running spark-submit job
import time
import pytz
import datetime
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.feature import VectorIndexer,StringIndexer, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
__author__ = 'Jonathan Hilgart'


# bring in the current bart and weather data to make a prediction against
# convert string into datetime format


def change_time_format(time):
    """Take in a month, day, year format and return year, month,
    day format as DateType"""
    month = time[:2]
    day = time[3:5]
    year = time[6:]
    date_time = datetime.datetime(int(year), int(month), int(day))
    return date_time


def bart_station_map(col):
    """Change the station names from BART historical data into an index"""
    if col == 'NCON':
        return 0
    elif col == 'POWL':
        return 1
    elif col == 'CIVC':
        return 2
    elif col == '16TH':
        return 3
    elif col == 'UCTY':
        return 4
    elif col == 'DBRK':
        return 5
    elif col == 'PLZA':
        return 6
    elif col == 'CAST':
        return 7
    elif col == 'GLEN':
        return 8
    elif col == 'EMBR':
        return 9
    elif col == 'SANL':
        return 10
    elif col == 'ROCK':
        return 11
    elif col == 'SHAY':
        return 12
    elif col == 'FTVL':
        return 13
    elif col == 'LAKE':
        return 14
    elif col == 'DALY':
        return 15
    elif col == 'WCRK':
        return 16
    elif col == 'FRMT':
        return 17
    elif col == 'ASHB':
        return 18
    elif col == 'OAKL':
        return 19
    elif col == 'CONC':
        return 20
    elif col == 'SFIA':
        return 21
    elif col == 'PITT':
        return 22
    elif col == 'DELN':
        return 23
    elif col == 'WDUB':
        return 24
    elif col == '19TH':
        return 25
    elif col == 'SSAN':
        return 26
    elif col == 'SBRN':
        return 27
    elif col == "NBRK":
        return 28
    elif col == "PHIL":
        return 29
    elif col == "MONT":
        return 30
    elif col == "COLM":
        return 31
    elif col == "DUBL":
        return 32
    elif col == "WOAK":
        return 33
    elif col == "MLBR":
        return 34
    elif col == "ORIN":
        return 35
    elif col == "MCAR":
        return 36
    elif col == "HAYW":
        return 37
    elif col == "LAFY":
        return 38
    elif col == "COLS":
        return 39
    elif col == "RICH":
        return 40
    elif col == "BAYF":
        return 41
    elif col == "BALB":
        return 42
    elif col == "24TH":
        return 43
    elif col == '12TH':
        return 44
    else:
        # we do not have this station
        pass


def live_bart_station_map(col):
    """Change the station names from BART live prediction data to integer to match historical data"""
    if col == "North Concord/Martinez":
        return 0
    elif col == 'Powell St.':
        return 1
    elif col == 'Civic Center/UN Plaza':
        return 2
    elif col == '16th St. Mission':
        return 3
    elif col == 'Union City':
        return 4
    elif col == 'Downtown Berkeley':
        return 5
    elif col == 'El Cerrito Plaza':
        return 6
    elif col == 'Castro Valley':
        return 7
    elif col == 'Glen Park (SF)':
        return 8
    elif col == 'Embarcadero':
        return 9
    elif col ==' San Leandro':
        return 10
    elif col == 'Rockridge':
        return 11
    elif col == 'South Hayward':
        return 12
    elif col ==  'Fruitvale':
        return 13
    elif col == 'Lake Merritt':
        return 14
    elif col ==' Daly City':
        return 15
    elif col ==' Walnut Creek':
        return 16
    elif col == 'Fremont':
        return 17
    elif col == 'Ashby':
        return 18
    elif col == "Oakland Int'l Airport":
        return 19
    elif col == 'Concord':
        return 20
    elif col == "San Francisco Int'l Airport":
        return 21
    elif col == 'Pittsburg/Bay Point':
        return 22
    elif col == 'El Cerrito del Norte':
        return 23
    elif col == 'West Dublin/Pleasanton':
        return 24
    elif col == '19th St. Oakland':
        return 25
    elif col == 'South San Francisco':
        return 26
    elif col == 'San Bruno':
        return 27
    elif col == "North Berkeley":
        return 28
    elif col == "Pleasant Hill/Contra Costa Centre":
        return 29
    elif col =="Montgomery St.":
        return 30
    elif col == "Colma":
        return 31
    elif col == "Dublin/Pleasanton":
        return 32
    elif col == "West Oakland":
        return 33
    elif col == "Millbrae":
        return 34
    elif col == "Orinda":
        return 35
    elif col == "MacArthur":
        return 36
    elif col == "Hayward":
        return 37
    elif col == "Lafayette":
        return 38
    elif col == "Coliseum":
        return 39
    elif col == "Richmond":
        return 40
    elif col == "Bay Fair":
        return 41
    elif col == "Balboa Park":
        return 42
    elif col == "24th St. Mission":
        return 43
    elif col == '12th St. Oakland City Center':
        return 44
    else:
        # we do not have this station
        pass

# Read in the bart data
def read_in_data():
    """Read in bart and weather historic data and
    return a dataframe ready for machine learning"""
    bart_df = spark.read.csv(
        "s3a://raw-data-2016-bart-weather/bart-data2016/date-hour-soo-dest-2016.csv")
    bart_trans_df = bart_df.select(
        col("_c0").alias('date'), col("_c1").alias("hour"), col("_c2").alias(
            "origin_station"), col("_c3").alias("destination_station"),
            col("_c4").alias("people"), dayofmonth(col("_c0")).alias(
                "day_of_month"), month(col("_c0")).alias("month_n"))
    bart_fix_types_df = bart_trans_df.withColumn(
        "people", bart_trans_df['people'].cast(IntegerType()))

    #grouped_bart_df =
    bart_grouped = bart_fix_types_df.groupby(
        "month_n", 'day_of_month', 'destination_station').sum('people')
    bart_grouped_rename = bart_grouped.select(
        "month_n", "day_of_month", "destination_station",
                col("sum(people)").alias("total_exits"))

    ### read in the weather data
    weather_df = spark.read.csv(
        "s3a://raw-data-2016-bart-weather/weather-data-2016/weather-historical-2016-sf"
        , header=True)
    weather_select = weather_df.select(
        "temp-avg", 'temp-low', 'temp-high',
        'humidity-avg', 'seapress-avg', 'wind-avg', 'precip-inches',
        dayofmonth(col('Month')).alias("day_of_month_weather"),
        month(col("Month")).alias("month_n_weather"))
    grouped_data = weather_select.join(bart_grouped_rename, on =
        [weather_select["month_n_weather"] == bart_grouped_rename["month_n"], \
        weather_select["day_of_month_weather"] ==
        bart_grouped_rename["day_of_month"]])

    # create a final DF for the ML model
    ml_df = grouped_data.select("temp-avg", "temp-low", "temp-high",
                                "humidity-avg", "seapress-avg", "wind-avg",
                        "precip-inches", "month_n", "day_of_month",
                        "destination_station", "total_exits")


    ##cast to the preset integers per station
    # index the bart station
    ml_df = ml_df.withColumn("indexed_stations_udf",
                    bart_indexer_historic(ml_df['destination_station']))

    bart_trans_df.withColumn("people",
                             bart_trans_df['people'].cast(IntegerType()))
    # set columns as integers
    ml_df = ml_df.withColumn("temp-avg", ml_df['temp-avg'].cast(IntegerType()))
    ml_df = ml_df.withColumn("temp-low", ml_df['temp-low'].cast(IntegerType()))
    ml_df = ml_df.withColumn("temp-high", ml_df['temp-high'].cast(IntegerType()))
    ml_df = ml_df.withColumn("humidity-avg",
                             ml_df['humidity-avg'].cast(IntegerType()))
    ml_df = ml_df.withColumn("seapress-avg",
                             ml_df['seapress-avg'].cast(IntegerType()))
    ml_df = ml_df.withColumn("wind-avg",
                             ml_df['wind-avg'].cast(IntegerType()))
    ml_df = ml_df.withColumn("precip-inches",
                             ml_df['precip-inches'].cast(IntegerType()))
    return ml_df


def train_gb_model(input_df, number_iterations=2):
    """  Train a gradient boost model from the bart and weather data.
    Return the trained model, and the rmse from the train test split"""
    ml_df.cache()
    ### train test split
    trainingData, testData = ml_df.randomSplit([0.7, 0.3])
    train_rows = trainingData.count()
    test_rows = testData.count()
    trainingData.cache()
    testData.cache()
    gb_assembler = VectorAssembler(inputCols=['temp-avg', 'temp-low',
                                              'temp-high', 'seapress-avg',
                                              'humidity-avg', 'wind-avg',
                                              'precip-inches', 'month_n',
                                              'day_of_month',
                                              'indexed_stations_udf'],
                                   outputCol="features")
    training = gb_assembler.transform(trainingData).select(
        col("features"),col("total_exits").alias("label-exits"))
    ## cache the model to test hyperparameters
    training.cache()
    # This takes ~15 minutes to run
    gb_model = GBTRegressor(labelCol="label-exits",
                            featuresCol="features",
                            maxIter=number_iterations,maxDepth=3,maxBins=50)
    gb_model_trained = gb_model.fit(training)
    testing = gb_assembler.transform(testData).select(
        col("features"), col("total_exits").alias("label-exits-true"))
    ## cache the model to test hyperparameters
    testing.cache()
    prediction = gb_model_trained.transform(testing)
    predicted = prediction.select(
        col("features"),"prediction","label-exits-true")
    evaluator = RegressionEvaluator(
    labelCol="label-exits-true", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predicted)
    print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)

    return gb_model_trained , rmse


def live_bart_weather_data(sf_year_yes,sf_month_yes,sf_day_yes):
    """Read in bart data and weather data from yesterday.
    Returns a combined dataframe ready to make predictions off of"""

    # bart data from yesterday
    bart_arrival = spark.read.parquet(
        "s3a://normalized-data-weather-bart/bart_arrival_0_{}/{}/{}/*".format(
        sf_year_yes, sf_month_yes, sf_day_yes))

    bart_physical = spark.read.parquet(
        "s3a://normalized-data-weather-bart/bart_physical_0_{}/{}/{}/*".format(
        sf_year_yes, sf_month_yes, sf_day_yes))
    # weather data from yesterday (would fix to today if given enough time)
    #wind_table = spark.read.parquet("s3a://normalized-data-weather-bart/wind_df2017/03/06/*")
    wind_table = spark.read.parquet(
        "s3a://normalized-data-weather-bart/wind_df{}/{}/{}/*".format(
        sf_year_yes, sf_month_yes, sf_day_yes))

    #main_temp_table = spark.read.parquet("s3a://normalized-data-weather-bart/main-temp2017/03/06/*")
    main_temp_table = spark.read.parquet(
        "s3a://normalized-data-weather-bart/main-temp{}/{}/{}/*".format(
        sf_year_yes, sf_month_yes, sf_day_yes))

    weather_description_table = spark.read.parquet(
        "s3a://normalized-data-weather-bart/weather-description{}/{}/{}/*".format(
        sf_year_yes, sf_month_yes, sf_day_yes))
    ## alias bart columns
    bart_arrival_renamed = bart_arrival.select(
        col('origin_station_0').alias('origin_station_arrival'),
        col("sf_time_0").alias("sf_time_arrival"),
        col("date_0").alias("date_arrival"),
        col("direction_0").alias("direction_arrival"),
        col("hour_0").alias("hour_arrival"),
        col("minutes_til_arrival_0").alias(
                            "minutes_til_arrival_bart_arrival"))
    #join bart tables together
    joined_bart_arrival_physical_df = bart_arrival_renamed.join(bart_physical,
        on = [bart_physical['origin_station_0'] ==
        bart_arrival_renamed['origin_station_arrival'],
        bart_physical['sf_time_0'] ==
        bart_arrival_renamed['sf_time_arrival'],
        bart_physical['direction_0'] ==
        bart_arrival_renamed['direction_arrival'],
        bart_physical['date_0'] ==
        bart_arrival_renamed['date_arrival']])
    #select columns I want
    final_joined_bart_df = joined_bart_arrival_physical_df.select(
        "origin_station_0", "sf_time_0", "date_0", "direction_0",
        "destination_0", "hour_0", "color_0", "bike_flag_0",
        "train_size_0", "capacity_0", "minutes_til_arrival_bart_arrival")
    #
    ## convert the string date to datetime format
    final_joined_bart_df_dt = final_joined_bart_df.withColumn(
        'date_0', change_time(col('date_0')))
    final_bart_df = final_joined_bart_df_dt.select(
        dayofmonth(col('date_0')).alias("day_of_month"),
        month(col("date_0")).alias("month_n"), "origin_station_0",
        "sf_time_0", "date_0", "direction_0", "hour_0", "bike_flag_0",
        "train_size_0", "capacity_0", "minutes_til_arrival_bart_arrival")
    # register as table to run SQL
    #sqlContext.registerDataFrameAsTable(final_bart_df, "final_bart")
    #final_bart_df.registerTempTable("final_bart")
    final_bart_df.createOrReplaceTempView("final_bart")
    #final_bart_df.createGlobalTempView("final_bart")

    final_bart_df = sqlContext.sql("""SELECT count(bike_flag_0) as
        total_number_of_trains, origin_station_0, date_0,direction_0,
        SUM (train_size_0) as total_number_train_cars,
        sum(capacity_0) as total_capacity, month_n, day_of_month
         FROM final_bart
            WHERE minutes_til_arrival_bart_arrival <5
            GROUP BY origin_station_0,date_0,direction_0, month_n, day_of_month
            ORDER BY total_capacity DESC""")
    # bring in weather data to ultimately join with bart data
    # and feed into our ML model
    wind_table_alias = wind_table.select(col("hour").alias("hour_wind"),
                                         col("date").alias("date_wind"),
                                         "speed", "deg")
    wind_temp_table = wind_table_alias .join(main_temp_table,
        on = [wind_table_alias['hour_wind'] == main_temp_table['hour'],
        wind_table_alias['date_wind'] == main_temp_table['date']])
    wind_temp_table_final = wind_temp_table.select("hour",
                                                   "date", 'humidity',
                                                   "speed", "deg",
                                                   "pressure", "temp",
                                                   "temp_max", "temp_min")
    weather_des_final = weather_description_table.select(
        col("col").alias('weather_des'), "hour", "date")
    weather_des_final.registerTempTable("weather_des_final")
    weather_des_ints = sqlContext.sql("""SELECT hour as hour_des,date as
                                      date_des,weather_des,
         CASE WHEN weather_des = 'Rain' THEN 1.0
             WHEN weather_des = 'Mist' THEN .1
             ELSE 0.0 end as weather_precip
           FROM  weather_des_final
            """)
    weather_des_ints_final = weather_des_ints.select("hour_des",
                                                      "date_des",
                                                      "weather_precip")
    # join weather des with the other two weather tables

    combo_df = wind_temp_table_final.join(weather_des_ints_final,
                                        on = [wind_temp_table_final['date']
                                        == weather_des_ints_final['date_des'],
                                        wind_temp_table_final['hour']
                                        == weather_des_ints_final['hour_des']])
    #select the columns you want
    final_df = combo_df.select("hour",
                               "date", "speed", "deg", "pressure", "temp",
                               "temp_max", "temp_min", "weather_precip")
    #change date string to date format
    # convert the date string into the date format for spark
    combo_df = combo_df.withColumn('date', change_time(col('date')))
    ## finally, select all of the columns
    ## drop duplicates to ensure we only have only weather forecast per hour
    final_weather_df = combo_df.select(dayofmonth(col('date')).alias(
        "day_of_month_weather"), month(col("date")).alias("month_n_weather"),
        "hour", "date", "speed", "deg", "pressure", "temp", "temp_max",
        "temp_min", "weather_precip", "humidity").dropDuplicates(
        ['day_of_month_weather', 'month_n_weather', 'hour'])
    final_weather_df.cache()
    final_bart_df.cache()
    temp_table = final_weather_df.join(final_bart_df,
        on = [final_weather_df['date'] == final_bart_df['date_0']])
    final_bart_weather_table = temp_table.select("day_of_month", "month_n",
        "total_capacity", "total_number_train_cars", "direction_0",
        "date_0", "origin_station_0", "weather_precip", "speed", "deg",
        "pressure", "temp", "temp_max", "temp_min", "humidity")
    ## index our bart stations to match the order in our ML algorithm
    final_bart_weather_table_stat = final_bart_weather_table.withColumn(
        "indexed_stations", bart_data_reformat_columns(col("origin_station_0")))
    # 150 people per train is a more realistic assumption of
    final_bart_weather_table_ml = final_bart_weather_table_stat.withColumn(
        'final_capacity', col("total_number_train_cars")*150).dropna()
    return final_bart_weather_table_ml


def make_predictions_today(input_df,historic_bart_df,trained_model):
    """Take in the bart data and weather data from yesterday (input df)
    and generate predictions
    of station capacity using the trained model"""
    bart_weather_current_assembler = VectorAssembler(inputCols=['temp',
     'temp_min',
     'temp_max',
     'humidity',
     'pressure',
     'speed',
     'weather_precip',
     'month_n',
     'day_of_month',
     'indexed_stations'], outputCol="features")
    # Can only do total exits per station,not direction of exits (i.e.
    # north or south)
    live_bart_weather_testing = bart_weather_current_assembler.transform(
        input_df).select(
        col("features"), col("origin_station_0"), col("date_0"))
    ## create predictions
    prediction_live = trained_model.transform(live_bart_weather_testing)
    predicted_live = prediction_live.select("prediction", "origin_station_0",
                                            "date_0")
    ## get the capacity prediction for yesterday and change prediction to exits
    predicted_live = predicted_live.withColumn("total-predicted-exits",
                                               col("prediction"))
    predicted_live = predicted_live.where(col('date_0') ==
                                          KeyFileName_yesterday)
    live_ridership = predicted_live.toPandas()
    total_capacity = input_df.select("origin_station_0",
                                     "final_capacity", "date_0").toPandas()
    #historic_df = historic_bart_df.select("origin_station_0","date_0",)
    final_historic_live_df = total_capacity.merge(live_ridership,
                                                  on=['origin_station_0',
                                                      'date_0'])
    ## ensure one prediction per station for the date
    final_historic_live_grouped = final_historic_live_df.groupby(
        ['origin_station_0', 'date_0']).mean().reset_index()
    ## get the percent occupancy
    final_historic_live_grouped['percent_capacity'] = \
    final_historic_live_grouped.apply(lambda x:
                                      x['total-predicted-exits']/
                                      x['final_capacity'] if \
                            x['total-predicted-exits']/
                            x['final_capacity']<=1.0 else 1.0, axis=1)

    final_historic_live_grouped.sort_values("percent_capacity",inplace=True)
    return final_historic_live_grouped



if __name__ =='__main__':
    # get the current day, and yesterday information to make predictions off
    # of
    ## use yseterday's capacity per bart station for the prediction
    # of today's capacity
    #(This assumes all days are the same for number of trains per station)

    # # when running spark-submit, need to create the spark context
    sc = SparkContext()
    spark = SparkSession(sc)
    sqlContext = SQLContext(sc)

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

    if len(str(sf_month_today)) < 2:
        sf_month_today = '0'+str(sf_month_today)
    if len(str(sf_day_today)) < 2:
        sf_day_today= '0'+str(sf_day_today)

    #to group against for the bart and weather data
    KeyFileName_today = "{}-{}-{}".format(
        sf_year_today, sf_month_today, sf_day_today)
    KeyFileName_yesterday = "{}-{}-{}".format(
        sf_year_yesterday, sf_month_yesterday, sf_day_yesterday)

    # define the UDFs
    bart_data_reformat_columns = udf(live_bart_station_map, IntegerType())
    bart_indexer_historic = udf(bart_station_map, IntegerType())
    change_time = udf(change_time_format, DateType())
    ## read in historical data
    ml_df = read_in_data()
    ## train the gboost model
    trained_gb_model, rmse_gb = train_gb_model(ml_df)
    ## combine the live data from bart and the weather
    final_bart_weather_df = \
    live_bart_weather_data(sf_year_yesterday,sf_month_yesterday,sf_day_yesterday)
    #create predictions from the live data
    final_df_predicted_capacity = \
    make_predictions_today(final_bart_weather_df,ml_df ,trained_gb_model)
    # save to html
    with open("predicted_capacity","wr") as fp:
        fp.write(final_df_predicted_capacity.to_html())
        fp.write("Current SF time {}".format(SF_time))
