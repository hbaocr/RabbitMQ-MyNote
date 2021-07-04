#https://www.cloudamqp.com/blog/how-to-run-rabbitmq-with-python.html
#https://faun.pub/different-types-of-rabbitmq-exchanges-9fefd740505d

import pika
import time
import sys

from pika.exchange_type import ExchangeType

url="amqps://hynparma:PTe2P2sFmMVEEbD1rXc1xPOgKajGMBIT@snake.rmq2.cloudamqp.com/hynparma"

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)


exchange_name_='test_exchange'
routing_key_='key_1'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange=exchange_name_,exchange_type=ExchangeType.direct,durable=True)
#auto create the queue with unique name
result=channel.queue_declare(queue='hello',durable=False,exclusive=True)
queue_name = 'hello'#result.method.queue

#bind the queue to the exchange
channel.queue_bind(queue=queue_name,exchange=exchange_name_,routing_key=routing_key_)
print(' [*] wait data from '+ queue_name)

#declare QOS
channel.basic_qos(prefetch_size=0,prefetch_count=1)

channel.basic_consume(queue=queue_name,on_message_callback=callback,auto_ack=False,exclusive=False)

channel.start_consuming()