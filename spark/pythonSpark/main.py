#!/usr/bin/env python3
import os
import findspark

SPARK_HOME = r"D:/spark/spark-3.2.4-bin-hadoop2.7"
HADOOP_HOME = r"D:/hadoop"
JAVA_HOME   = r"C:/Program Files/Java/jre1.8.0_431"

findspark.init(SPARK_HOME)
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["JAVA_HOME"]   = JAVA_HOME

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

# ───────────────────────────────────────────────────────────────────────────
# 3) Build SparkSession with the Kafka connector
spark = (
    SparkSession.builder
        .appName("KafkaSQLStreaming")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4"
        )
        .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.shuffle.partitions", "1")

# ───────────────────────────────────────────────────────────────────────────
# 4) Read from Kafka as a streaming

kafka_df = (
    spark.readStream
         .format("kafka")
         .option("kafka.bootstrap.servers", "localhost:9092")
         .option("subscribe", "pagesLiked")
         .option("startingOffsets", "earliest")
         .option("failOnDataLoss", "false")
         .load()
)

# ───────────────────────────────────────────────────────────────────────────
# 5) Parse JSON into a column named "category"

schema = StructType().add("category", StringType())
parsed = (
    kafka_df
      .select(from_json(col("value").cast("string"), schema).alias("data"))
      .select(col("data.category").alias("category"))
)

# ───────────────────────────────────────────────────────────────────────────
# 6) Register that streaming DF as a temp view

parsed.createOrReplaceTempView("streaming_pages")

# ───────────────────────────────────────────────────────────────────────────
# 7) Build a *new* streaming DF via Spark SQL
#     (this is equivalent to parsed.groupBy("category").count() but in SQL)
aggregated = spark.sql("""
    SELECT
      category,
      COUNT(*) AS total_likes
    FROM streaming_pages
    GROUP BY category
    ORDER BY total_likes DESC
""")

# ───────────────────────────────────────────────────────────────────────────
# 8) Write the SQL results back to console every second
query = (
    aggregated.writeStream
              .outputMode("complete")                # show full table each time
              .format("console")
              .option("truncate", False)
              .option("numRows", 1000)
            #   .option("checkpointLocation", "kafka_continuous_chk")
              .trigger(processingTime="1 second")
              .start()
)

# ───────────────────────────────────────────────────────────────────────────
# 9) Wait until the stream is stopped
query.awaitTermination()
