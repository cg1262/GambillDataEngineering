from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Lakehouse").getOrCreate()

# Load raw data (Bronze layer)
raw_df = spark.read.format("csv").option("header", "true").load("s3://bronze-layer/sales.csv")

# Clean and transform data (Silver layer)
cleaned_df = raw_df.filter(raw_df["sales_amount"] > 0).withColumnRenamed("sales_amount", "amount")

# Save to Silver layer
cleaned_df.write.format("delta").save("s3://silver-layer/sales_cleaned")