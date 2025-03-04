import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the directory containing DataPipeline.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataPipeline import produce_messages, consume_messages, process_messages, store_messages, visualize_messages

class TestDataPipeline(unittest.TestCase):

    @patch('DataPipeline.KafkaProducer')
    def test_produce_messages(self, MockKafkaProducer):
        producer = MockKafkaProducer.return_value
        produce_messages('test_topic', [{'user_id': '123', 'message': 'test', 'timestamp': '2025-03-04T12:00:00Z'}])
        producer.send.assert_called_once()

    @patch('DataPipeline.KafkaConsumer')
    def test_consume_messages(self, MockKafkaConsumer):
        consumer = MockKafkaConsumer.return_value
        consumer.__iter__.return_value = [MagicMock(value={'user_id': '123', 'message': 'test', 'timestamp': '2025-03-04T12:00:00Z'})]
        messages = consume_messages('test_topic')
        self.assertEqual(len(messages), 1)

    @patch('DataPipeline.SparkSession')
    def test_process_messages(self, MockSparkSession):
        spark = MockSparkSession.builder.getOrCreate.return_value
        df = spark.createDataFrame.return_value
        df.filter.return_value = df
        df.groupBy.return_value.count.return_value = df
        process_messages([{'user_id': '123', 'message': 'test', 'timestamp': '2025-03-04T12:00:00Z'}])
        df.show.assert_called()

    @patch('DataPipeline.psycopg2.connect')
    def test_store_messages(self, MockConnect):
        conn = MockConnect.return_value
        cur = conn.cursor.return_value
        store_messages([{'user_id': '123', 'message': 'test', 'timestamp': '2025-03-04T12:00:00Z'}])
        cur.execute.assert_called_once()

    def test_visualize_messages(self):
        visualize_messages([{'user_id': '123', 'message': 'test', 'timestamp': '2025-03-04T12:00:00Z'}])
        # Check if the visualization function runs without errors

if __name__ == '__main__':
    unittest.main()