A new high-level API for streaming
-----

Look at the source code for the [`structured_network_wordcount_windowed`](https://github.com/apache/spark/blob/v2.1.0/examples/src/main/python/sql/streaming/structured_network_wordcount_windowed.py) example and get it running on your Spark cluster.

Then take a look back at the [Structured Streaming In Apache Spark](https://databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html) blog post you read before class. Notice how you can stream data from an S3 bucket. Can you see how this could be useful with Kinesis Firehose (_i.e._ without having to develop a separate Kinesis stream consumer)? Time permitting (_i.e._ this is optional) adapt this to the S3 bucket where Kinesis Firehose is streaming data and use it to count distinct users for a given day.
