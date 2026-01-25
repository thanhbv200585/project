from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

spark = SparkSession.builder \
    .appName("NewsStreaming") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.stopGracefullyOnShutdown", "true")

schema = StructType() \
    .add("title", StringType()) \
    .add("summary", StringType()) \
    .add("published", StringType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news-topic") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("kafka.group.id", "news-streaming-v1") \
    .load()

json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).where(col("data").isNotNull()) \
 .select("data.*")

query = json_df.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/news/raw") \
    .option("checkpointLocation", "hdfs://namenode:8020/news/checkpoint/v1") \
    .outputMode("append") \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()
