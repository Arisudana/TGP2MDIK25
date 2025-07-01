from pyspark.sql import SparkSession

# Inisialisasi SparkSession
spark = SparkSession.builder.appName("IngestCSVtoHDFS").getOrCreate()

# Langkah 1: Baca dari filesystem lokal (bisa juga gunakan path relatif/absolut)
df = spark.read.option("header", True).csv("C:/Users/Nikolaus/Desktop/fp_midk/Tweets.csv")

# (Opsional) Bisa tambahkan transformasi di sini misalnya cleaning
# df = df.withColumn(...)

# Langkah 2: Simpan langsung ke HDFS
df.write.mode("overwrite").option("header", True).csv("hdfs://localhost:9000/user/data/Tweets.csv")

# Selesai
spark.stop()
print("✅ File berhasil di-ingest ke HDFS.")
