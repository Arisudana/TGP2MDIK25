# Tugas Group Project #2: Sistem Data Terintegrasi untuk Retail dan Customer Support

## Deskripsi Proyek

Proyek ini mengintegrasikan data penjualan ritel dan data keluhan pelanggan dari media sosial untuk membangun sistem data terintegrasi menggunakan pendekatan Data Warehouse, Data Lakehouse, dan Big Data Management.

### Kelompok 4:
- Nikolaus Vico Cristianto (5026211107)
- I Gusti Made Arisudana (5026211188)
- Fidela Jovita Kanedi (6026242016)

## Dataset yang Digunakan

1. **Superstore Sales Dataset (Structured)**
   - Format: CSV
   - Informasi: Transaksi penjualan, kategori produk, segmentasi pelanggan, wilayah, tanggal pesanan, nilai penjualan, dan profit.
   - Tujuan: Menganalisis performa penjualan.

2. **Customer Support Tweets (Unstructured)**
   - Format: CSV
   - Informasi: Teks tweet, waktu, metadata interaksi pelanggan via Twitter.
   - Tujuan: Analisis keluhan dan sentimen pelanggan.

## Arsitektur Sistem

Pipeline dibagi menjadi beberapa layer:
- **Ingestion Layer**: Apache Spark
- **Data Lake Layer**: Hadoop HDFS
- **ETL Layer**: PySpark
- **Storage Layer**: DuckDB (Star Schema)
- **Analytics & Visualization**: Apache Superset via Docker

## Architecture Diagram

![Architecture](docs/architecture_pipeline.png)

## Alur Implementasi

### 1. Setup Environment
- Java 8u351
- Python 3.12
- Spark 3.3.3
- Hadoop 3.2.4
- DuckDB 1.3.1
- Docker & Superset

### 2. Ingestion
- Data dibaca dengan Apache Spark dan disimpan di HDFS.

### 3. ETL
- Transformasi data:
  - Parsing tanggal, casting numerik, agregasi tweets
  - Gabungkan data penjualan & tweet berdasarkan tanggal (left join)
- Simpan ke DuckDB:
  - Tabel fakta: `fact_sales_complaints`
  - Tabel dimensi: `dim_product_category`, `dim_sub_category`, `dim_region`, `dim_customer_support`

### 4. Visualisasi di Superset
3 dashboard utama:
- **Overview**: Korelasi penjualan vs keluhan
- **Explore Sales**: Analisis profit dan penjualan per kategori/wilayah
- **Explore Complaints**: Pola keluhan harian, panjang teks, wilayah

## Insight Utama

- Korelasi positif antara volume penjualan dan jumlah keluhan
- November 2017 terjadi anomali dengan lonjakan jumlah dan kompleksitas keluhan
- Performa kategori produk menunjukkan margin dan keluhan yang bervariasi
- Panjang teks keluhan mencerminkan tingkat frustasi dan kompleksitas masalah pelanggan

## Tantangan & Solusi

- **Inkompatibilitas Kafka-HDFS** → Gunakan Spark untuk batching ingestion
- **Kompatibilitas antar versi tools** → Gunakan versi stabil yang telah teruji kompatibel
- **Kebutuhan storage besar** → Manajemen storage lokal dengan perencanaan awal
- **Konfigurasi port HDFS & Spark** → Periksa port dengan `netstat`, sesuaikan direktori dan izin


## Link Terkait

- [Presentasi YouTube](https://youtu.be/t2ICr6LrLRE)

## Pembagian Tugas

| Nama                     | Tanggung Jawab |
|--------------------------|----------------|
| Nikolaus Vico Cristianto | Arsitektur, ingestion, dokumentasi, video |
| I Gusti Made Arisudana   | EDA, ETL, ERD, DuckDB |
| Fidela Jovita Kanedi     | Docker, Delta Lake, Superset & Dashboard |

---

**Institut Teknologi Sepuluh Nopember – Manajemen Data, Informasi, dan Konten – Genap 2025**

