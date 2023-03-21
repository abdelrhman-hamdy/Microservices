import pika 
import json 
from bson import ObjectId
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
        channel.basic_publish(
            exchange='',
            routing_key= "videl",
            body=json.dumps(massege),
            properties=pika.BasicProperties(delivery_mode= pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except:
        fs.delete(video_id)
        return "Internal server Error1111", 500

def download(mp3_id,fs_mp3):
    try : 
       mp3_file =fs_mp3.get(ObjectId(mp3_id))
    except:
        return None,f'Error Cannot Get MP3 file using this ID : {mp3_id} '
    
    return mp3_file, None