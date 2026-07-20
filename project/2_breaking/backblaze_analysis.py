from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, count, datediff, min, floor

spark = SparkSession.builder.appName("Backblaze_Q1_2026_Analysis").getOrCreate()

# reading
raw_df = spark.read.csv("gs://my-cs131-bucket/project/raw_data/data_Q1_2026/*.csv", header=True, inferSchema=True)


# organize
df = raw_df.select(
    col("date").cast("date"),
    col("serial_number"),
    col("model"),
    col("capacity_bytes").cast("long"),
    col("failure").cast("int")
)

# classify Drive Type (HDD vs SSD)
# standard engineering baseline: Drives with capacity_bytes <= 0 or models containing "SSD" 
# represent solid-state storage in Backblaze data templates
df_classified = df.withColumn(
    "drive_type",
    when(col("model").contains("SSD") | (col("capacity_bytes") < 600000000000), "SSD").otherwise("HDD")
)

# calculate drive age
# find the oldest date for each unique serial number within this quarter to establish an operational baseline, then calculate age in days for every operational tracking record

birth_df = df_classified.groupBy("serial_number").agg(min("date").alias("start_date"))
df_with_age = df_classified.join(birth_df, on="serial_number", how="inner") \
                           .withColumn("age_days", datediff(col("date"), col("start_date")))

# group Age Days into 90-Day "Quarterly" Lifespan Cohorts
# drives into: 0-3 months old, 3-6 months old, 6-9 months old, etc.

df_with_cohorts = df_with_age.withColumn("lifespan_quarter", floor(col("age_days") / 90))

# Final Grouped Aggregation
# Calculate metrics per Drive Type (HDD vs SSD) across different Lifespan Quarters
final_metrics = df_with_cohorts.groupBy("drive_type", "lifespan_quarter").agg(
    sum("failure").alias("total_failures"),
    count("failure").alias("total_drive_days")
)

# standardize into Failure Rate per Million Drive Days
result_df = final_metrics.withColumn(
    "failure_rate_per_million",
    (col("total_failures") / col("total_drive_days")) * 1000000
).orderBy("drive_type", "lifespan_quarter")


result_df.write.mode("overwrite").csv("gs://my-cs131-bucket/project/2_breaking/aggregated_results", header=True)

spark.stop()
