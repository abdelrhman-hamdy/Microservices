import pika 
import json 

def upload(file,fs,channel,access):
    try:
        video_id=fs.put(file)
    except: 
        return "Internal server Error", 500
    
    massege = {
        "video_id":str(video_id),
        "mp3_id" : None, 
        "username": access['username']
    }

    try : 
        channel.basic_publich(
            echange='',
            routing_key= "videl",
            body=json.dumps(massege),
            properties=pika.BasicProperties(delivery_mode= pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except:
        fs.delete(video_id)
        return "Internal server Error", 500