## Some note on Queue of RabbitMQ. 
* [amqp-concepts](https://www.rabbitmq.com/tutorials/amqp-concepts.html)


* PUB Data --> exchange ------>queue
* You can public the data to exchange along side with `routing_key` and let the rabbitMQ distribute your data to expected queue 
* The final target of data is queue which satisfy the binding condition. `If there is no binding queues, or no queues under exchange match the routing condition, the pub data will be ignore`.  The routing condition are: 

  * **In The `fanout` exchange type**: It will `ignore` the PUB data's `routing_key` and broadcast pub data to all the queues which bind to this exchange
  * **In the `direct` exchange type** : The queue will receive pub data if  queue's `routing_key` is matched pub data's `routing_key` 
  * **In the `topic` exchange type** : The queue will receive pub data if  queue's `routing_key` is matched pub data's `routing_key` by regex condition
  * **In the `header` exchange type** : The queue will receive pub data if the header para of queue is matched pub data's `header` 
  

* **`Exchange`**:
  * `Name`: is unique. When declaring the exchange, if this is `empty`, RabbitMQ will use the `default` built-in exchange.If you declare 2 `exchange` with same name, the 2nd declare will not create the new one, it use the previous declared exhange.
  * `Durability` (exchanges survive broker restart)
  * `Auto-delete` (exchange is deleted when last queue is unbound from it)
  * `Arguments` (optional, used by plugins and broker-specific features)
  * In the `default` exchange (name='') when publishing data with the `routing_key`='hello'. The binding queue should have the name ='hello' also to receive the data.[link](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
* **`Queue`**
  * `Name` : unique. When declaring the queue, if this is `empty`, RabbitMQ will auto gen the unique name for this queue. If you declare 2 queues with same name , the 2nd queue declaration will be error.
  * `Durable` (the queue will survive a broker restart)
  * `Exclusive` (used by only one connection and the queue will be deleted when that connection closes)
  * `Auto-delete` (queue that has had at least one consumer is deleted when last consumer unsubscribes)
  * `Arguments` (optional; used by plugins and broker-specific features such as message TTL, queue length limit, etc)
    


## Step to use the RabbitMQ

* **`Publisher`**
  * Declare the `exchange` and choose type of exchange 
  * Publish the message to to previous declared `exchange` with their expect `routing_key` : for example  `channel.basic_publish(exchange=exchange_name_,routing_key=routing_key_,body=message)`
  * Note that, if you don't have any `existing` binding queue to this `exchange` which satisfy the `routing_key` this message will be ignored.

  
* **`Subscriber/Consumer`**
  * Declare the `exchange` and choose type of exchange  `the same` with the `publisher`
  * Declare the `queue` with suitable paras.Note that, you can not declare the 2 queue having the same name ==>error
  * Bind the declared `queue` with the `exchange`, and point out the the routing rule by input the `routing_key` match with pub message. The moment when you call `channel.queue_bind(queue=queue_name,exchange=exchange_name_,routing_key=routing_key_)`, the queue will bind to your exchange and starting buffer the publishing msg ( if `routing_key` is matched)
  * Define the `QoS` of the binding queues: `channel.basic_qos(prefetch_size,prefetch_count)`
    * `prefetch_size`:  specify when the queue send  msg in queue to the consumer.The queue server will send a message to consumer in advance if it is equal to or smaller in size than the available `prefetch_size`. If 0, send immediately
    * `prefetch_count`: specify how many messages are being sent at the same time
  * Register the call_back to the declared `queue` to  receive the msg from the server: `channel.basic_consume(queue=queue_name,on_message_callback=callback,auto_ack=False,exclusive=False)`
  * In the call_back ==> ack msg if `auto_ack=False` when you registered the callback
  

