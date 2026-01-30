from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from schema import RAW_SCHEMA

spark = SparkSession.builder.appName("EnrichNews").getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news.validated") \
    .load()

parsed = df.select(
    from_json(col("value").cast("string"), RAW_SCHEMA).alias("data")
).select("data.*")

enriched = parsed \
    .withColumn("language", lit("vi")) \
    .withColumn("category", lit("general")) \
    .withColumn("sentiment_score", rand()) \
    .withColumn("processed_time", current_timestamp())

query = enriched.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/news/enriched") \
    .option("checkpointLocation", "hdfs://namenode:8020/checkpoints/enriched") \
    .outputMode("append") \
    .start()

query.awaitTermination()
