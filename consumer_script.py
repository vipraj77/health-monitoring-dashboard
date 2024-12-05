from confluent_kafka import Consumer, KafkaException # type: ignore
import json
from pymongo import MongoClient # type: ignore

# Consumer configuration
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'health-monitor-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the health data topic
consumer.subscribe(['health-data'])

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['health_db']
collection = db['sensor_data']

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Timeout is in seconds
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        
        # Process the message
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Received data: {data}")
        
        # Save the data to MongoDB
        collection.insert_one(data)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
