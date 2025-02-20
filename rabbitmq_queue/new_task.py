import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# create a queue , named hello
channel.queue_declare(queue="hello")

# send msg to queue .
# rabbitmq passes msg to queue through exchange .
# exchange specified by empty string ("") is special exchange.it allows us to specify exactly to which queue the message should go.


message = "".join(sys.argv[1:]) or "hello world"
channel.basic_publish(exchange="", routing_key="hello", body=message)

print(f"hello queue sent message : {message}")

connection.close()
