from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from schema import RAW_SCHEMA

spark = SparkSession.builder.appName("ValidateNews").getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "news.raw") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

parsed = df.select(
    from_json(col("value").cast("string"), RAW_SCHEMA).alias("data")
).select("data.*")

validated = parsed \
    .filter(col("article_id").isNotNull()) \
    .withWatermark("ingest_time", "10 minutes") \
    .dropDuplicates(["article_id"])

query = validated.selectExpr(
    "to_json(struct(*)) AS value",
    "source AS key"
).writeStream \
 .format("kafka") \
 .option("kafka.bootstrap.servers", "kafka:9092") \
 .option("topic", "news.validated") \
 .option("checkpointLocation", "hdfs://namenode:8020/checkpoints/validated") \
 .start()

query.awaitTermination()
