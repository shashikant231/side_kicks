import pika
import sys
import os
import time


def main():
    # connect to rabbitmq server
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # create a queue.
    # NOTE : since queue is already created in send.py file, we are just making sure that queue exist.

    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        print(type(body))
        print(f"worker recived task {body.decode()}")
        time.sleep(body.count(b"."))
        print("worker task performed")
        # message = body.decode()
        # print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
