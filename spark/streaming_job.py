from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

spark = SparkSession.builder \
    .appName("NewsStreaming") \
    .getOrCreate()

schema = StructType() \
    .add("title", StringType()) \
    .add("summary", StringType()) \
    .add("published", StringType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news-topic") \
    .load()

json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

query = json_df.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:9000/news/raw") \
    .option("checkpointLocation", "hdfs://namenode:9000/news/checkpoint") \
    .outputMode("append") \
    .start()

query.awaitTermination()
