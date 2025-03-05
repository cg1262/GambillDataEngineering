"""
Created by: Chris Gambill
Created On: 11/22/2024
Created For: Cirrus Aircraft

"""

from pyspark.sql.functions import col, regexp_replace, count, when, to_timestamp, expr 
from pyspark.sql.types import TimestampType, LongType, StringType
from delta.tables import DeltaTable
from datetime import datetime

def process_single_flight_file(file_path, target_table="bronze_dev.iq.flight_vitals"):

    start_time = datetime.now()
    metrics = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_path": file_path,
        "status": "started"
    }

    try:
        # Read the single parquet file
        source_df = spark.read.parquet(file_path)
        
        
        """
        Get the flight_id from the source data to use with metric metadata collection
        and to check to see if flight has already processed
        """
        flight_id = source_df.select("FlightID").limit(1).collect()[0]["FlightID"]
        print(f"Processing flight_id: {flight_id}")
        metrics["flight_id"] = flight_id
        
        # Check if flight_id already exists and count existing records
        existing_records = spark.table(target_table) \
            .filter(col("flight_id") == flight_id) \
            .count()
            
        metrics["existing_records"] = existing_records
        if existing_records > 0:
            print(f"Found {existing_records} existing records for flight_id {flight_id}")
        
        # Quick data validation
        row_count = source_df.count()
        metrics["source_row_count"] = row_count
        
        """
        Create and raise 0 record value error based on file length 
        (keeps from trying to process an empty file)
        """
        if row_count == 0:
            raise ValueError(f"Source file {file_path} is empty")
        
        """
        Map columns to match target schema with explicit casting
        tring to eliminate potential errors due to data type mismatch
        """
        mapped_df = source_df.select(
            to_timestamp(
                regexp_replace(col("EventDateTime"), " UTC$", ""),
                "yyyy-MM-dd HH:mm:ss Z"
            ).alias("event_date_time"),
            col("MSSinceStartup").cast(LongType()).alias("milliseconds_since_startup"),
            col("ICDID").cast(LongType()).alias("icd_id"),
            col("ParameterID").cast(LongType()).alias("parameter_id"),
            col("ParameterValue").cast(StringType()).alias("parameter_value"),
            col("FlightID").cast(StringType()).alias("flight_id"),
            col("AircraftID").cast(StringType()).alias("aircraft_id"),
            col("TailNumber").cast(StringType()).alias("tail_number")
        )

        # Checking for nulls in ids 
        null_counts = mapped_df.select([
            count(when(col(c).isNull(), True)).alias(c)
            for c in ["icd_id", "parameter_id", "flight_id"]
        ]).collect()[0]
        
        # Raise error if nulls are found
        for column, null_count in null_counts.asDict().items():
            if null_count > 0:
                raise ValueError(f"Found {null_count} null values in critical column {column}")

        # Setting delta table variable for use in insert
        delta_table = DeltaTable.forName(spark, target_table)

        """
        Delete existing records for flight_id if they exist in delta table
        so that we don't create duplicates if we reprocess a flight.
        """

        if existing_records > 0:
            print(f"Deleting existing records for flight_id: {flight_id}")
            delta_table.delete(condition=f"flight_id = '{flight_id}'")
            
        # Insert new records
        print(f"Inserting new records for flight_id: {flight_id}")
        mapped_df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .saveAsTable(target_table)

        # Validate records inserted match records in file and add to metrics
        inserted_count = spark.table(target_table) \
            .filter(col("flight_id") == flight_id) \
            .count()
        
        metrics.update({
            "inserted_records": inserted_count,
            "status": "success",
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_duration_seconds": (datetime.now() - start_time).total_seconds()
        })
        
        print(f"Successfully processed flight_id {flight_id}: {inserted_count} records inserted")
        
        # Optimize table after significant changes kind of like reindexing for table perfomance
        if existing_records > 10000 or inserted_count > 10000:
            spark.sql(f"""
                OPTIMIZE {target_table}
                ZORDER BY (icd_id, parameter_id, flight_id)
            """)
            metrics["table_optimized"] = True

        return metrics

    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        print(error_msg)
        metrics.update({
            "status": "error",
            "error_message": error_msg,
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_duration_seconds": (datetime.now() - start_time).total_seconds()
        })
        raise Exception(error_msg)

    finally:
        """
        Log metrics -- ask if we want to keep additiaonal 
        metrics/metadata somewhere for potential issue logging
        """
        print("\nProcessing Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")

full_file_path = '/Volumes/bronze_dev/iq/vol_stgflightdatasystemsdev_decoded-flight-data/SF50/SF50-0008/000086/*.parquet'
process_single_flight_file(full_file_path)