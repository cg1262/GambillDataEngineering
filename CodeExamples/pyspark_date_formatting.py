# Import necessary PySpark functions
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, date_format, from_unixtime, regexp_replace, concat, lit, expr

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Date Formatting in PySpark") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Section 1: Parse standard date formats with to_date
data1 = [('12/26/2024',)]
df1 = spark.createDataFrame(data1, ['raw_date'])
df1 = df1.withColumn('formatted_date', to_date('raw_date', 'MM/dd/yyyy'))
df1.show()

# Section 2: Format dates to a specific string format with date_format
df1 = df1.withColumn('display_date', date_format('formatted_date', 'MMMM dd, yyyy'))
df1.show()

# Section 3: Handle Unix Epoch time
data2 = [(1706303400,)]  # Epoch timestamp
df2 = spark.createDataFrame(data2, ['epoch_time'])
df2 = df2.withColumn('readable_date', from_unixtime('epoch_time'))
df2.show()

# Section 4: Handle partial dates like "Oct 25th"
data3 = [('Oct 25th',)]
df3 = spark.createDataFrame(data3, ['raw_date'])
df3 = df3.withColumn('clean_date', regexp_replace('raw_date', 'th', '')) \
         .withColumn('complete_date', concat('clean_date', lit(' 2024'))) \
         .withColumn('parsed_date', to_date('complete_date', 'MMM dd yyyy'))
df3.show()

# Section 5: Convert Excel serial dates to readable dates
data4 = [(45000,)]  # Excel serial date
df4 = spark.createDataFrame(data4, ['serial_date'])
df4 = df4.withColumn('excel_date', expr("date_add('1900-01-01', serial_date - 2)"))
df4.show()

# Best practices reminder: Validate and document assumptions in your pipeline
print("Date formatting examples completed. Always validate and standardize your dates early in the pipeline!")
