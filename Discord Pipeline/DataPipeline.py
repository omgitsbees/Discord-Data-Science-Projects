from kafka import KafkaProducer, KafkaConsumer
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import psycopg2
import plotly.express as px
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Step 1: Data Ingestion
def produce_messages(topic, messages):
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        for message in messages:
            producer.send(topic, message)
        producer.flush()
        logging.info("Messages produced successfully")
    except Exception as e:
        logging.error(f"Error producing messages: {e}")

def consume_messages(topic):
    try:
        consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        messages = []
        for message in consumer:
            messages.append(message.value)
            if len(messages) >= 10:  # Process in batches of 10
                break
        logging.info("Messages consumed successfully")
        return messages
    except Exception as e:
        logging.error(f"Error consuming messages: {e}")
        return []

# Step 2: Data Processing
def process_messages(messages):
    try:
        spark = SparkSession.builder.appName("DiscordDataProcessing").getOrCreate()
        df = spark.createDataFrame(messages)
        
        # Example transformation: filter messages from a specific user
        filtered_df = df.filter(col("user_id") == "123")
        
        # Example aggregation: count messages per user
        aggregated_df = df.groupBy("user_id").count()
        
        filtered_df.show()
        aggregated_df.show()
        
        logging.info("Messages processed successfully")
        return filtered_df.collect(), aggregated_df.collect()
    except Exception as e:
        logging.error(f"Error processing messages: {e}")
        return [], []

# Step 3: Data Storage
def store_messages(messages):
    try:
        conn = psycopg2.connect(
            dbname="discord_db",
            user="your_username",
            password="your_password",
            host="localhost"
        )
        cur = conn.cursor()
        
        for message in messages:
            cur.execute(
                "INSERT INTO messages (user_id, message, timestamp) VALUES (%s, %s, %s)",
                (message['user_id'], message['message'], message['timestamp'])
            )
        
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Messages stored successfully")
    except Exception as e:
        logging.error(f"Error storing messages: {e}")

# Step 4: Data Visualization
def visualize_messages(messages):
    try:
        df = pd.DataFrame(messages)
        
        fig = px.histogram(df, x="user_id", title="Messages per User")
        fig.show()
        logging.info("Messages visualized successfully")
    except Exception as e:
        logging.error(f"Error visualizing messages: {e}")

if __name__ == "__main__":
    # Example messages
    messages = [
        {"user_id": "123", "message": "Hello, world!", "timestamp": "2025-03-04T12:00:00Z"},
        {"user_id": "456", "message": "Hi there!", "timestamp": "2025-03-04T12:01:00Z"}
    ]
    
    # Step 1: Produce and consume messages
    produce_messages('discord_messages', messages)
    consumed_messages = consume_messages('discord_messages')
    
    # Step 2: Process messages
    filtered_messages, aggregated_messages = process_messages(consumed_messages)
    
    # Step 3: Store messages
    store_messages(consumed_messages)
    
    # Step 4: Visualize messages
    visualize_messages(consumed_messages)