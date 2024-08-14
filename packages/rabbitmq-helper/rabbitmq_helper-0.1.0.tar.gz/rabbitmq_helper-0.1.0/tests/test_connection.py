import unittest
from rabbitmq_helper.connection import RabbitMQConnection


class TestRabbitMQConnection(unittest.TestCase):

    def setUp(self):
        self.conn = RabbitMQConnection(host='localhost', port=5672, username='guest', password='PASSWORD')

    def test_connection_established(self):
        self.conn.connect()
        self.assertIsNotNone(self.conn.connection)
        self.assertIsNotNone(self.conn.channel)

    def test_connection_closed(self):
        self.conn.connect()
        self.conn.close()
        self.assertIsNone(self.conn.connection)
        self.assertIsNone(self.conn.channel)

    def tearDown(self):
        try:
            self.conn.close()
        except:
            pass


if __name__ == '__main__':
    unittest.main()
