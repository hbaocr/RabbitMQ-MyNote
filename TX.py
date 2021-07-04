#https://www.cloudamqp.com/blog/how-to-run-rabbitmq-with-python.html
#https://faun.pub/different-types-of-rabbitmq-exchanges-9fefd740505d

import pika
import time
import sys

from pika.exchange_type import ExchangeType

url="amqps://hynparma:PTe2P2sFmMVEEbD1rXc1xPOgKajGMBIT@snake.rmq2.cloudamqp.com/hynparma"

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

exchange_name_='test_exchange'
routing_key_='key_1'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange=exchange_name_,exchange_type=ExchangeType.direct,durable=True)

for i in range(0,10):
    channel.basic_publish(exchange=exchange_name_,routing_key=routing_key_,body=message+str(i))
connection.close()