import unittest
from rabbitmq_helper.connection import RabbitMQConnection
from rabbitmq_helper.publisher import RabbitMQPublisher
from rabbitmq_helper.queue import RabbitMQQueue


class TestRabbitMQPublisher(unittest.TestCase):

    def setUp(self):
        self.conn = RabbitMQConnection(host='localhost', port=5672, username='guest', password='PASSWORD')
        self.conn.connect()
        self.publisher = RabbitMQPublisher(self.conn.channel)
        self.queue = RabbitMQQueue(self.conn.channel)
        self.queue.declare_queue('test_queue')

    def test_publish_message(self):
        self.publisher.publish('', 'test_queue', 'Hello, RabbitMQ!')

        # Verificar se a mensagem foi publicada corretamente
        method_frame, header_frame, body = self.conn.channel.basic_get('test_queue')
        self.assertIsNotNone(method_frame)
        self.assertEqual(body.decode(), 'Hello, RabbitMQ!')

    def tearDown(self):
        self.conn.channel.queue_delete('test_queue')
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
