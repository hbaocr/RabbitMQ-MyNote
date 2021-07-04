import pika
import sys
url="amqps://hynparma:PTe2P2sFmMVEEbD1rXc1xPOgKajGMBIT@snake.rmq2.cloudamqp.com/hynparma"

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()