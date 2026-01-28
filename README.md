# News Streaming Big Data Pipeline

## 1. Project Overview

This project is a **production-like Big Data Streaming Pipeline** designed to simulate the workload, inspired by large-scale academic pipelines such as the *Spotify Big Data Pipeline*.

The system ingests real-time news data from **RSS feeds**, streams it through **Apache Kafka**, processes it using **Apache Spark Structured Streaming**, stores it in **HDFS**, and exposes analytical views through a **dashboard layer**.

The project emphasizes:

* End-to-end streaming architecture
* Fault tolerance & checkpointing
* Scalable data storage
* Observability & monitoring
* Clear separation of responsibilities (ingestion, processing, storage, analytics)

---

## 2. High-Level Architecture

### Data Flow

1. RSS feeds are polled periodically
2. Producer publishes parsed news events to Kafka topics
3. Spark Structured Streaming consumes Kafka topics
4. Data is validated, enriched, and aggregated
5. Processed data is written to HDFS (Parquet)
6. Analytics layer reads from HDFS for dashboards

### Architecture Diagram (Mermaid)

```mermaid
graph LR
    RSS[RSS Sources]
    P[Python Producer]
    K[Kafka Broker]
    S[Spark Streaming]
    H[HDFS]
    D[Dashboard / BI]

    RSS --> P
    P --> K
    K --> S
    S --> H
    H --> D
```

---

## 3. Technology Stack

| Layer             | Technology                                      |
| ----------------- | ----------------------------------------------- |
| Ingestion         | Python, feedparser                              |
| Messaging         | Apache Kafka                                    |
| Stream Processing | Apache Spark (Structured Streaming)             |
| Storage           | HDFS, Parquet                                   |
| Orchestration     | Docker, Docker Compose                          |
| Monitoring        | Spark UI, Kafka CLI, HDFS UI                    |
| Visualization     | (Planned) Superset / Grafana / Custom Dashboard |

---

## 4. Project Structure

```
.
├── docker-compose.yml        # Full cluster definition
├── producer.py               # RSS → Kafka producer
├── streaming_job.py          # Spark Structured Streaming job
├── README.md                 # Project documentation
└── data/
    ├── raw/                  # Raw ingested data
    ├── processed/            # Cleaned & enriched data
    └── analytics/            # Aggregated datasets
```

---

## 5. Data Ingestion Layer (Kafka Producer)

### Responsibilities

* Poll RSS feeds on a configurable interval
* Normalize news data (title, summary, timestamp, source)
* Serialize data as JSON
* Publish events to Kafka topic(s)

### Design Notes

* At-least-once delivery semantics
* Idempotent message keys (hash of title + timestamp)
* Backoff & retry on Kafka unavailability

---

## 6. Streaming Processing Layer (Spark)

### Core Features

* Spark Structured Streaming with Kafka source
* Schema enforcement using `StructType`
* Exactly-once processing semantics (via checkpoints)
* Output stored as partitioned Parquet files

### Fault Tolerance

* Checkpointing in HDFS
* Automatic recovery after Spark restart
* Kafka offset tracking

---

## 7. Storage Layer (HDFS)

### Data Zones

* **Raw Zone**: unmodified streaming output
* **Processed Zone**: cleaned & deduplicated data
* **Analytics Zone**: aggregated datasets

### Storage Format

* Parquet (columnar, compressed)
* Partitioned by date

---

## 8. Observability & Monitoring

| Component    | Access                                         |
| ------------ | ---------------------------------------------- |
| Spark UI     | [http://localhost:4040](http://localhost:4040) |
| Kafka Topics | kafka-topics.sh                                |
| HDFS UI      | [http://localhost:9870](http://localhost:9870) |

Metrics tracked:

* Kafka lag
* Spark batch duration
* Input rows per second
* HDFS storage growth

---

## 9. Dashboard & Analytics (Planned)

Planned analytics use cases:

* News volume over time
* Top news sources
* Keyword frequency analysis
* Near real-time trend detection

Possible tools:

* Apache Superset
* Grafana + Trino
* Custom React dashboard

---

## 10. Production-Like Considerations

* Service dependency ordering
* Health checks
* Safe-mode handling in HDFS
* Schema evolution readiness
* Horizontal scalability

---

## 11. Future Enhancements

* Multiple Kafka topics by category
* Spark watermarking & late data handling
* Elasticsearch sink for fast search
* CI/CD pipeline
* Data quality checks

---

## 12. How to Run

```bash
docker-compose up -d
```

Verify:

* Kafka topic exists
* Producer publishes messages
* Spark UI shows active query
* Parquet files appear in HDFS

---

## 13. Learning Outcomes

This project demonstrates:

* Real-time big data pipelines
* Distributed system debugging
* Production-style Spark streaming
* End-to-end data engineering workflow

---

## 14. References

* Apache Kafka Documentation
* Apache Spark Structured Streaming Guide
* HDFS Architecture
* Spotify Big Data Pipeline (Reference Project)
