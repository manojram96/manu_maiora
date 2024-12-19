import pandas as pd
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
spark = SparkSession.builder \
        .appName("maiora") \
        .getOrCreate()
#reading the region A order file
region_A_file_path = "/Users/manoj/Desktop/Maiora/order_region_a(in).csv"
region_a_read = pd.read_csv(region_A_file_path)
#applying pandas in order to flatten the json column on region_a order file
region_a_json_parse = region_a_read["PromotionDiscount"].apply(json.loads)
#dropping the promotion discount from the original dataset and adding the parsed columns to the region_a order file
region_a_pd = pd.concat([region_a_read.drop(['PromotionDiscount'], axis=1), region_a_json_parse.apply(pd.Series)], axis=1)
#creating the dataframe structure
region_a_df = spark.createDataFrame(region_a_pd)
region_a_column = region_a_df.withColumn("Region",lit("Region A"))
#similar steps goes with region_b order file
region_B_file_path = "/Users/manoj/Desktop/Maiora/order_region_b(in).csv"
region_b_read = pd.read_csv(region_B_file_path)
region_b_json_parse = region_b_read["PromotionDiscount"].apply(json.loads)
region_b_pd = pd.concat([region_b_read.drop(['PromotionDiscount'], axis=1), region_b_json_parse.apply(pd.Series)], axis=1)
region_b_df = spark.createDataFrame(region_b_pd)
region_b_column = region_b_df.withColumn("Region",lit("Region B"))

#combining both tables
combined_df  = region_a_column.union(region_b_column)
#finding total_sales Amount
total_sales_df = combined_df.withColumn("total_sales",expr("QuantityOrdered * ItemPrice"))
#finding net_sales Amount
net_sales_df = total_sales_df.withColumn("net_sales",expr("total_sales-Amount"))
#dropping duplicate record based on OrderId
clean_df = net_sales_df.dropDuplicates(["OrderId"])
#filtering records which is non-negative and greater than 0
filter_df = net_sales_df.filter("net_sales > 0")
#creating temporary table to validate the data
filter_df.createOrReplaceTempView("Sales_data")
#finding total_no_records
total_count_sql = spark.sql("select count(*) as total_no_records from Sales_data ")
#finding total_sales_per_region
total_sales_per_region = spark.sql("select sum(total_sales) as total_sales_per_region,Region from Sales_data group by Region")
#finding average_sales_per_transaction
average_sales_per_region = spark.sql("select avg(total_sales) as avg_sales_per_transactions,Region from Sales_data group by Region")

#creating sqlite database and saving the data as table
db_url = "jdbc:sqlite:/mnt/data/sales_data.db"
table_name = "transformed_sales"
filter_df.write \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", table_name) \
    .option("driver", "org.sqlite.JDBC") \
    .mode("overwrite") \
    .save()

# Stop the Spark session
spark.stop()



























