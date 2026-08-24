import gc
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_col(df_columns, target_col, default_val=0.0):
    cols_lower = {c.lower(): c for c in df_columns}
    target_lower = target_col.lower()

    if target_lower in cols_lower:
        if default_val is not None:
            return F.coalesce(F.col(cols_lower[target_lower]), F.lit(default_val))
        return F.col(cols_lower[target_lower])

    return F.lit(default_val)


spark = (SparkSession
         .builder
         .appName("NYC_taxi")
         .master("local[4]")
         .config("spark.driver.memory", "4g")
         .config("spark.executor.memory", "4g")
         .config("spark.driver.maxResultSize", "2g")
         .getOrCreate())

years = [str(yr) for yr in range(2020, 2025)]  # 2020 - 2025
months = [f"{m:02d}" for m in range(1, 13)]


input_dir = "C:/Users/igapo/Downloads"
output_dir = "C:/Users/igapo/Documents/Projects/data_source"
os.makedirs(output_dir, exist_ok=True)

taxi_types = {
    'green': 'lpep',
    'yellow': 'tpep'
}

for taxi_type, prefix in taxi_types.items():
    pickup_column = f'{prefix}_pickup_datetime'
    dropoff_column = f'{prefix}_dropoff_datetime'

    for year in years:
        for month in months:
            file_name = f"{input_dir}/{taxi_type}_tripdata_{year}-{month}.parquet"

            if not os.path.exists(file_name):
                print(f"No such file: {file_name}")
                continue

            print(f"Executing: {taxi_type} {year}-{month}")
            df = spark.read.parquet(file_name)
            cols = df.columns

            aggregated_data = (
                df.filter(
                    (F.col(pickup_column).isNotNull()) &
                    (F.date_format(F.col(pickup_column), 'yyyy-MM') == f"{year}-{month}") &
                    (get_col(cols, "fare_amount", 0.0) >= 0) &
                    (get_col(cols, "trip_distance", 0.0) >= 0)
                )
                .groupBy(
                    F.lit(taxi_type).alias("taxi_type"),
                    F.to_date(F.col(pickup_column)).alias("pickup_date"),
                    F.hour(F.col(pickup_column)).alias("pickup_hour"),
                    get_col(cols, "PULocationID", -1).cast("int").alias("pickup_location_key"),
                    get_col(cols, "DOLocationID", -1).cast("int").alias("dropoff_location_key"),
                    get_col(cols, "RatecodeID", -1).cast("int").alias("rate_code_key"),
                    get_col(cols, "payment_type", -1).cast("int").alias("payment_type")
                )
                .agg(
                    F.count('*').alias('trip_count'),
                    F.sum(get_col(cols, "passenger_count", 0)).alias('total_passengers'),
                    F.sum(get_col(cols, "trip_distance", 0.0)).alias('total_distance'),
                    F.round(
                        F.sum(
                            (F.unix_timestamp(F.col(dropoff_column)) - F.unix_timestamp(F.col(pickup_column))) / 60
                        ), 2
                    ).alias('total_duration_minutes'),
                    F.sum(get_col(cols, "fare_amount", 0.0)).alias('total_fare'),
                    F.sum(get_col(cols, "tip_amount", 0.0)).alias('tips_amount'),
                    F.sum(get_col(cols, "tolls_amount", 0.0)).alias('tolls_amount'),
                    F.sum(get_col(cols, "congestion_surcharge", 0.0)).alias('congestion_surcharge'),
                    F.sum(get_col(cols, "extra", 0.0)).alias('extra'),
                    F.sum(get_col(cols, "total_amount", 0.0)).alias('total_amount')
                )
            )

            output_path = f"{output_dir}/{year}_{month}_{taxi_type}_NYC_pickup.csv"
            aggregated_data.toPandas().to_csv(output_path, index=False)
            print(f"Saved: {output_path}")

            spark.catalog.clearCache()
            del df, aggregated_data
            gc.collect()

spark.stop()