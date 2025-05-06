# kafka Tutorial

[medium link](https://medium.com/@amberkakkar01/getting-started-with-apache-kafka-on-docker-a-step-by-step-guide-48e71e241cf2)

### Start the kafka and zookeeper container

```powershell
docker-compose up -d
```

### Start new Topic with zookeepr

```powershell
docker exec -it <kafka-container-id> /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic my-topic
```

### Start to produce to that topic

```powershell
docker exec -it <kafka-container-id> /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```

### Start to Consume that topic

```powershell
docker exec -it <kafka-container-id> /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning
```

### Clean After finish working

```powershell
docker-compose down
```
