from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, length, avg, count, when, to_timestamp
import duckdb

# ---------------------------
# INIT SPARK SESSION
# ---------------------------
spark = SparkSession.builder \
    .appName("RetailCustomerSupportETL") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# ---------------------------
# READ DATA FROM HDFS
# ---------------------------
superstore_df = spark.read.option("header", True).csv("hdfs://localhost:9000/user/data/Superstore.csv")
tweets_df = spark.read.option("header", True).csv("hdfs://localhost:9000/user/data/Tweets.csv")

# ---------------------------
# TRANSFORM SUPERSTORE
# ---------------------------
superstore_df = superstore_df \
    .withColumn("OrderDate", to_date(col("Order Date"), "MM/dd/yyyy")) \
    .withColumn("Sales", col("Sales").cast("float")) \
    .withColumn("Profit", col("Profit").cast("float")) \
    .withColumn("Discount", col("Discount").cast("float"))

# ---------------------------
# TRANSFORM TWEETS
# ---------------------------
tweets_df = tweets_df \
    .withColumn("CreatedAt", to_timestamp(col("created_at"), "E MMM dd HH:mm:ss Z yyyy")) \
    .withColumn("TextLength", length(col("text"))) \
    .withColumn("Inbound", when(col("inbound")=="True", 1).otherwise(0))

# ---------------------------
# AGGREGATE CUSTOMER SUPPORT
# ---------------------------
tweets_agg = tweets_df.groupBy("CreatedAt").agg(
    count(when(col("Inbound")==1, True)).alias("NumComplaints"),
    avg("TextLength").alias("AvgTextLength")
)

# ---------------------------
# JOIN DATA
# ---------------------------
joined_df = superstore_df.join(
    tweets_agg,
    superstore_df.OrderDate == tweets_agg.CreatedAt,
    how="left"
).select(
    "OrderDate", "Category", "Sub-Category", "Region", "Sales", "Profit", "Discount",
    "NumComplaints", "AvgTextLength"
)

joined_df = joined_df.fillna(0)

# ---------------------------
# SAVE TO DUCKDB
# ---------------------------
# Simpan fact table ke CSV (sementara)
joined_df.toPandas().to_csv("/tmp/fact_sales_complaints.csv", index=False)

# Buat koneksi DuckDB
con = duckdb.connect(database="/tmp/retail_support.duckdb")

# ---------------------------
# LOAD FACT TABLE & DIMENSIONS
# ---------------------------
con.execute("""
    CREATE TABLE fact_sales_complaints AS 
    SELECT * FROM read_csv_auto('/tmp/fact_sales_complaints.csv')
""")

# Dimension tables
con.execute("""
    CREATE TABLE dim_product_category AS 
    SELECT DISTINCT Category FROM fact_sales_complaints
""")
con.execute("""
    CREATE TABLE dim_sub_category AS 
    SELECT DISTINCT "Sub-Category" FROM fact_sales_complaints
""")
con.execute("""
    CREATE TABLE dim_region AS 
    SELECT DISTINCT Region FROM fact_sales_complaints
""")
con.execute("""
    CREATE TABLE dim_customer_support AS 
    SELECT OrderDate, NumComplaints, AvgTextLength 
    FROM fact_sales_complaints 
    GROUP BY OrderDate, NumComplaints, AvgTextLength
""")

# ---------------------------
# QUICK OLAP CHECK
# ---------------------------
result = con.execute("""
    SELECT Region, SUM(Sales) AS TotalSales, SUM(NumComplaints) AS TotalComplaints 
    FROM fact_sales_complaints 
    GROUP BY Region 
    ORDER BY TotalSales DESC
""").fetchdf()

print(result)

con.close()
