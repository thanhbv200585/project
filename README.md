# News Big Data Analytics Pipeline

## 1. Giới thiệu

Dự án **News Big Data Analytics Pipeline** xây dựng một hệ thống thu thập, lưu trữ và phân tích dữ liệu lớn từ các nguồn tin tức online theo thời gian thực. Project được thực hiện nhằm áp dụng các kiến thức trong môn **IT4931 – Lưu trữ và xử lý dữ liệu lớn (HUST)**, bao gồm Kafka, HDFS, Spark Streaming, Spark SQL, Spark ML và kiến trúc Kappa.

Hệ thống cho phép ingest dữ liệu tin tức liên tục, xử lý dữ liệu dạng stream, lưu trữ vào Data Lake và phục vụ phân tích/khai phá tri thức.

---

## 2. Mục tiêu

* Thu thập dữ liệu tin tức liên tục từ RSS / Web crawl.
* Xây dựng pipeline xử lý dữ liệu lớn theo **kiến trúc Kappa**.
* Lưu trữ dữ liệu thô (raw data) trong Data Lake (HDFS).
* Xử lý dữ liệu thời gian thực bằng Spark Structured Streaming.
* Phân tích dữ liệu bằng Spark SQL và Spark ML.
* Triển khai demo bằng Docker Compose.

---

## 3. Đặc trưng Big Data (5V)

* **Volume**: Hàng chục nghìn bài báo theo thời gian.
* **Velocity**: Dữ liệu sinh liên tục từ các nguồn tin.
* **Variety**: Dữ liệu văn bản, metadata (nguồn, thời gian, chủ đề).
* **Veracity**: Dữ liệu có thể nhiễu, cần làm sạch.
* **Value**: Phát hiện xu hướng, chủ đề nóng, cảm xúc xã hội.

---

## 4. Kiến trúc hệ thống

Hệ thống được thiết kế theo **kiến trúc Kappa**, sử dụng một pipeline xử lý luồng duy nhất cho cả dữ liệu thời gian thực và dữ liệu lịch sử.

Luồng dữ liệu:

```
News Sources (RSS / Crawl)
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

**Lý do chọn Kappa**:

* Giảm độ phức tạp so với Lambda.
* Phù hợp với dữ liệu tin tức real-time.
* Dữ liệu lịch sử có thể xử lý lại bằng cách replay Kafka stream.

---

## 5. Công nghệ sử dụng

* **Apache Kafka**: Hệ thống truyền thông điệp phân tán.
* **Apache Spark**: Structured Streaming, Spark SQL, Spark ML.
* **HDFS**: Lưu trữ dữ liệu lớn dạng Data Lake.
* **Python**: Crawl dữ liệu và viết Spark job.
* **Docker & Docker Compose**: Triển khai và demo hệ thống.

---

## 6. Dataset

### Nguồn dữ liệu chính

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
│   └── producer.py
├── spark/
│   └── streaming_job.py
├── hdfs/
│   ├── namenode/
│   └── datanode/
└── README.md
```

---

## 8. Hướng dẫn chạy demo

### Yêu cầu

* Docker >= 20.x
* Docker Compose
* RAM khuyến nghị >= 8GB

### Các bước chạy

```bash
docker-compose up -d
```

### Kiểm tra

* **HDFS UI**: [http://localhost:9870](http://localhost:9870)
* Dữ liệu lưu tại: `/news/raw` (HDFS)

---

## 9. Machine Learning (mở rộng)

Các bài toán ML có thể triển khai:

* Phân loại chủ đề bài báo (Politics, Tech, Sports...).
* Phân tích sentiment nội dung tin tức.

Spark ML Pipeline:

* Tokenizer
* HashingTF / TF-IDF
* Logistic Regression / Naive Bayes

---

## 10. Kết quả mong đợi

* Pipeline chạy ổn định với dữ liệu streaming.
* Dữ liệu được lưu trữ an toàn trong Data Lake.
* Có thể truy vấn và phân tích dữ liệu bằng Spark SQL.
* Demo end-to-end trong 15 phút presentation.

---

## 11. Hạn chế và hướng phát triển

* Chưa xử lý dữ liệu mạng xã hội.
* ML ở mức cơ bản.
* Có thể mở rộng thêm Dashboard (Superset / Kibana).

---

## 12. Tài liệu tham khảo

* Lecture Notes IT4931 – Đại học Bách Khoa Hà Nội
* Apache Kafka Documentation
* Apache Spark Documentation
