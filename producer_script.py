from confluent_kafka import Producer # type: ignore
import json
import time
import random

# Kafka producer configuration
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Simulated data for heart rate, glucose, and other metrics
def generate_data():
    heart_rate = random.randint(60, 100)
    glucose_level = random.uniform(70, 180)
    blood_pressure = {'systolic': random.randint(100, 130), 'diastolic': random.randint(60, 90)}
    oxygen_level = random.uniform(95, 100)
    return {
        'heart_rate': heart_rate,
        'glucose_level': glucose_level,
        'blood_pressure': blood_pressure,
        'oxygen_level': oxygen_level
    }

# Callback to confirm message delivery
def on_delivery(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Produce data and send to Kafka
try:
    while True:
        data = generate_data()  # Generate random data
        print(f"Sending data: {data}")
        
        # Serialize the data and send to the respective Kafka topics
        producer.produce('health-data', value=json.dumps(data).encode('utf-8'), callback=on_delivery)
        producer.flush()
        
        # Sleep for 1 second to simulate real-time data generation
        time.sleep(1)
except KeyboardInterrupt:
    print("Producer stopped.")
finally:
    producer.flush()
