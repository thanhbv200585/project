from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, count

spark = SparkSession.builder \
    .appName("RealtimeNewsAggregation") \
    .getOrCreate()

news_df = spark.readStream \
    .format("parquet") \
    .load("hdfs://namenode:8020/news/clean")

agg_df = news_df \
    .withWatermark("published", "10 minutes") \
    .groupBy(
        window(col("published"), "5 minutes"),
        col("source")
    ) \
    .agg(
        count("*").alias("news_count")
    )

query = agg_df.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/news/analytics/realtime") \
    .option("checkpointLocation", "hdfs://namenode:8020/news/checkpoint/realtime_agg") \
    .outputMode("append") \
    .start()

query.awaitTermination()
