HyperLogLog
-----------

As you read in the [Approximate Algorithms in Apache Spark](https://databricks.com/blog/2016/05/19/approximate-algorithms-in-apache-spark-hyperloglog-and-quantiles.html) blog post, HyperLogLog is implemented in Spark as [countApproxDistinct](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.RDD.countApproxDistinct). Apply this to your tweets dataset to get an approximate count of daily active users (DAUs). Compare this to a true count (_i.e._ not using `countApproxDistinct`). What's the time difference? What's the accuracy tradeoff?
 
