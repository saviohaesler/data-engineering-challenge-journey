# Data Engineering Fundamentals Challenge Journey

Welcome to the **Data Engineering Fundamentals Challenge Journey**! Follow the steps below to set up and execute the required services.

## Setup Instructions

### 1. Start Zookeeper and Kafka
```bash
zkServer.sh start
```
```bash
kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

### 2. Start Kafdrop
```bash
cd /opt/kafdrop
```
```bash
./start-kafdrop.sh &
```

### 3. Start Hadoop and Spark
```bash
start-dfs.sh
```
```bash
spark-start.sh
```

### 4. Start Redis
```bash
redis-server
```

### 5. Start Jupyter Notebook
```bash
pyspark \
    --master spark://localhost:7077 \
    --deploy-mode client \
    --conf spark.dynamicAllocation.enabled=false \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
```

### 6. Start the Server
```bash
python server.py
```

---

## Accessing Services

### Kafdrop
URL: [http://10.248.16.132:9999/](http://10.248.16.132:9999/)

### Jupyter Notebook
URL: [http://10.248.16.132:8889/](http://10.248.16.132:8889/)

---

## Topic Design Explanation

### Topic Separation by Data Type
Each sensor type is assigned a **separate Kafka topic** to ensure clean data separation:
- `light`
- `barometer`
- `pedometer`
- `location`

### Number of Partitions
- **Initial Setup:** Each topic will have **one partition** since we only have one broker available.
- **Scaling:** For larger user bases and higher data volumes, the system can scale by increasing the number of partitions.

### Number of Replications
- **Initial Setup:** Replication is not applicable due to having only one broker.
- **Ideal Scenario:** In a multi-broker setup, a replication factor of **3** is recommended for redundancy and fault tolerance.

### Design Considerations for High User Load
The topic structure is designed to scale horizontally:
- Each **partition** can handle a subset of the data.
- Example: Location data can be partitioned by **region** or **user ID**.
