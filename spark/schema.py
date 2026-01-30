from pyspark.sql.types import *

RAW_SCHEMA = StructType([
    StructField("schema_version", StringType()),
    StructField("event_type", StringType()),
    StructField("article_id", StringType()),
    StructField("title", StringType()),
    StructField("summary", StringType()),
    StructField("link", StringType()),
    StructField("published_time", TimestampType()),
    StructField("source", StringType()),
    StructField("ingest_time", TimestampType())
])

ENRICHED_SCHEMA = StructType([
    StructField("schema_version", StringType()),
    StructField("article_id", StringType()),
    StructField("title", StringType()),
    StructField("summary", StringType()),
    StructField("source", StringType()),
    StructField("published_time", TimestampType()),
    StructField("language", StringType()),
    StructField("category", StringType()),
    StructField("sentiment_score", DoubleType()),
    StructField("processed_time", TimestampType())
])
