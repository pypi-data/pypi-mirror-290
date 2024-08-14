import unittest
from rabbitmq_helper.connection import RabbitMQConnection
from rabbitmq_helper.queue import RabbitMQQueue


class TestRabbitMQQueue(unittest.TestCase):

    def setUp(self):
        self.conn = RabbitMQConnection(host='localhost', port=5672, username='guest', password='PASSWORD')
        self.conn.connect()
        self.queue = RabbitMQQueue(self.conn.channel)

    def test_declare_queue(self):
        self.queue.declare_queue('test_queue')
        # Verificar se a fila foi declarada, pode-se usar um método ou API para isso

    def test_bind_queue(self):
        self.queue.declare_queue('test_queue')
        # Criar um exchange para testar
        self.conn.channel.exchange_declare(exchange='test_exchange', exchange_type='direct')
        self.queue.bind_queue('test_queue', 'test_exchange', 'test_routing_key')
        # Verificar se a fila foi vinculada ao exchange

    def tearDown(self):
        self.conn.channel.queue_delete('test_queue')
        self.conn.channel.exchange_delete('test_exchange')
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
