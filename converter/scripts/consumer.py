import pika 
from pymongo import MongoClient
import os ,sys 
import gridfs
import to_mp3 


dbclient=MongoClient("mongodb://host.minikube.internal:27017/")
videodb=dbclient.videos
mp3sdb=dbclient.mp3s
fs_video = gridfs.GridFS(videodb)
fs_mp3 = gridfs.GridFS(mp3sdb)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='videl',durable=True)
def callback(ch, method, properties, body):
    err = to_mp3.start(body,fs_video,fs_mp3,ch)
    if err : 
        ch.basic_nack(delivery_tag=method.delivery_tag)
    else : 
        ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_consume(queue=os.getenv('VIDEO_QUEUE'), on_message_callback=callback)


if __name__ == '__main__':
    print('Waiting for Masseges')
    channel.start_consuming()