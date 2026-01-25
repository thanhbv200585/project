# News Big Data Analytics Pipeline

## 1. Giới thiệu

Dự án **News Big Data Analytics Pipeline** xây dựng một hệ thống thu thập, lưu trữ và phân tích dữ liệu lớn từ các nguồn tin tức online theo thời gian thực. Project được thực hiện nhằm áp dụng các kiến thức trong môn **IT4931 – Lưu trữ và xử lý dữ liệu lớn (HUST)**.

Hệ thống áp dụng các công nghệ phổ biến trong hệ sinh thái Big Data như **Kafka, HDFS, Spark Structured Streaming, Spark SQL và Spark ML**, được thiết kế theo **kiến trúc Kappa**. Pipeline cho phép ingest dữ liệu liên tục, xử lý streaming, lưu trữ vào Data Lake và phục vụ phân tích/khai phá tri thức.

---

## 2. Mục tiêu

* Thu thập dữ liệu tin tức liên tục từ RSS Feed.
* Xây dựng pipeline xử lý dữ liệu lớn theo **kiến trúc Kappa**.
* Lưu trữ dữ liệu thô (raw data) trong **Data Lake (HDFS)**.
* Xử lý dữ liệu thời gian thực bằng **Spark Structured Streaming**.
* Phân tích dữ liệu bằng **Spark SQL và Spark ML**.
* Triển khai và demo toàn bộ hệ thống bằng **Docker Compose**.

---

## 3. Đặc trưng Big Data (5V)

* **Volume**: Hàng chục nghìn bài báo được thu thập theo thời gian.
* **Velocity**: Dữ liệu sinh liên tục từ các nguồn tin tức online.
* **Variety**: Dữ liệu văn bản, metadata (nguồn, thời gian, chủ đề).
* **Veracity**: Dữ liệu không đồng nhất, có thể nhiễu, cần làm sạch.
* **Value**: Phân tích xu hướng, chủ đề nóng và cảm xúc xã hội.

---

## 4. Kiến trúc hệ thống

Hệ thống được thiết kế theo **kiến trúc Kappa**, sử dụng **một pipeline xử lý luồng duy nhất** cho cả dữ liệu thời gian thực và dữ liệu lịch sử.

### Luồng dữ liệu

```
News Sources (RSS)
        ↓
      Kafka (Event Log)
        ↓
Spark Structured Streaming
        ↓
   HDFS Data Lake (Parquet)
        ↓
 Spark SQL / Spark ML
        ↓
   Serving Layer / Dashboard
```

### Lý do chọn kiến trúc Kappa

* Giảm độ phức tạp so với Lambda Architecture.
* Phù hợp với dữ liệu tin tức real-time.
* Dữ liệu lịch sử có thể xử lý lại bằng cách **replay Kafka stream**.

---

## 5. Công nghệ sử dụng

* **Apache Kafka**: Hệ thống truyền thông điệp phân tán (event streaming platform).
* **Apache Spark**: Structured Streaming, Spark SQL, Spark ML.
* **HDFS**: Lưu trữ dữ liệu lớn theo mô hình Data Lake.
* **Python**: Thu thập dữ liệu RSS và xây dựng Spark job.
* **Docker & Docker Compose**: Triển khai, orchestration và demo hệ thống.

---

## 6. Dataset

### Nguồn dữ liệu

* VNExpress RSS: [https://vnexpress.net/rss/tin-moi-nhat.rss](https://vnexpress.net/rss/tin-moi-nhat.rss)
* BBC News RSS: [https://www.bbc.com/news/rss.xml](https://www.bbc.com/news/rss.xml)

### Schema dữ liệu

```json
{
  "title": "string",
  "summary": "string",
  "published": "timestamp",
  "source": "string"
}
```

---

## 7. Cấu trúc thư mục

```
news-bigdata-pipeline/
├── docker-compose.yml
├── producer/
│   └── producer.py          # Kafka producer (RSS ingestion)
├── spark/
│   └── streaming_job.py     # Spark Structured Streaming job
├── hdfs/
│   ├── namenode/
│   └── datanode/
└── README.md
```

---

## 8. Hướng dẫn chạy demo

### Yêu cầu hệ thống

* Docker >= 20.x
* Docker Compose
* RAM khuyến nghị >= 8GB

### Các bước chạy

```bash
docker-compose up -d
```

### Kiểm tra hệ thống

* **HDFS NameNode UI**: [http://localhost:9870](http://localhost:9870)
* **Spark UI**: [http://localhost:4040](http://localhost:4040) (khi Spark job đang chạy)
* **Kafka Topic**: `news-topic`
* **Dữ liệu HDFS**: `/news/raw`

---

## 9. Machine Learning (Mở rộng)

Các bài toán ML có thể triển khai trên dữ liệu đã lưu trữ:

* Phân loại chủ đề bài báo (Politics, Tech, Sports...).
* Phân tích sentiment nội dung tin tức.

### Spark ML Pipeline (ví dụ)

* Tokenizer
* StopWordsRemover
* HashingTF / TF-IDF
* Logistic Regression / Naive Bayes

---

## 10. Kết quả mong đợi

* Pipeline streaming chạy ổn định.
* Dữ liệu được lưu trữ an toàn trong Data Lake (HDFS, Parquet).
* Có thể truy vấn dữ liệu bằng Spark SQL.
* Demo end-to-end hoàn chỉnh trong ~15 phút presentation.

---

## 11. Hạn chế và hướng phát triển

### Hạn chế

* Chưa xử lý dữ liệu mạng xã hội (Twitter, Facebook...).
* Machine Learning ở mức cơ bản.
* Chưa có giao diện dashboard trực quan.

### Hướng phát triển

* Bổ sung Dashboard (Apache Superset / Grafana).
* Mở rộng thêm nhiều nguồn dữ liệu.
* Triển khai multi-node HDFS & Spark cluster.

---

## 12. Tài liệu tham khảo

* Lecture Notes IT4931 – Đại học Bách Khoa Hà Nội
* Apache Kafka Documentation
* Apache Spark Documentation
* Hadoop HDFS Documentation

flowchart LR
    subgraph Data Sources
        RSS1[VNExpress RSS]
        RSS2[BBC News RSS]
    end

    subgraph Ingestion Layer
        P[Python Producer<br/>feedparser]
    end

    subgraph Messaging Layer
        K[(Apache Kafka<br/>news-topic)]
    end

    subgraph Processing Layer
        SS[Spark Structured Streaming<br/>JSON → DataFrame]
    end

    subgraph Storage Layer
        HDFS[(HDFS Data Lake<br/>Parquet Files)]
    end

    subgraph Analytics Layer
        SQL[Spark SQL]
        ML[Spark ML<br/>Topic / Sentiment]
    end

    subgraph Serving Layer
        UI[Analytics / Dashboard]
    end

    RSS1 --> P
    RSS2 --> P
    P --> K
    K --> SS
    SS --> HDFS
    HDFS --> SQL
    HDFS --> ML
    SQL --> UI
    ML --> UI
