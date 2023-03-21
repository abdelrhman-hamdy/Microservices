import pika 
import smtplib
import os 
import json 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue= os.getenv('QUEUE_NAME'),durable=True )

def callback(ch, method, properties, body):
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_TOKEN')

    body=json.loads(body)
    receiver_email=body['username']
    mp3_id = body['mp3_id']

    message = f"""\
    Subject: Your Video has been Converted Successfully! 

    you can Download the MP3 using this ID : {mp3_id}."""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login successful")
    try :
        server.sendmail(sender_email, receiver_email, message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Email has been sent to {receiver_email}")
    except: 
        ch.basic_nack(delivery_tag=method.delivery_tag)
        print(f"FAILED to send an Email to {receiver_email}")
    

channel.basic_consume(queue=os.getenv('QUEUE_NAME'), on_message_callback=callback)

if __name__ == '__main__':
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()