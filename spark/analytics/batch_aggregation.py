from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from schema import RAW_SCHEMA

spark = SparkSession.builder \
    .appName("NewsAnalytics") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news.enriched") \
    .option("startingOffsets", "latest") \
    .load()

parsed = df.select(
    from_json(col("value").cast("string"), RAW_SCHEMA).alias("data")
).select("data.*")
