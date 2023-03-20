import os, gridfs, pika,json  
from flask import Flask, request
from flask_pymongo import PyMongo
#from auth_svc import access
import requests 
#import ../auth/server  import validate
from  storage import  util
auth_pod_ip=os.getenv('AUTH_SERVICE_IP')
server= Flask(__name__) 

server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongodb= PyMongo(server)

fs=gridfs.GridFS(mongodb.db)    # inserting large document size in  MongoDB

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
@server.route("/login",methods=["POST"])
def login(): 
    url= f'http://{auth_pod_ip}/login'

    response = requests.post(url,auth=(request.authorization.username,request.authorization.password) )
    if response.status_code == 200 : 
        return response.text 
    else : 
        return response.text, response.status_code 


@server.route("/upload",methods=["POST"]) 
def upload():

    if "Authorization" not in request.headers: 
        return "missing credentails", 401
    
    encoded_jwt=request.headers["Authorization"]
    if not encoded_jwt: 
        return  "missing credentails", 401
    
    url= f'http://{auth_pod_ip}/validate'
    response = requests.post(url,headers={'Authorization': encoded_jwt})
    
    if response.status_code != 200 : 
        return response.text,response.status_code
    
    access = json.loads(response.txt) 
    
    if access['admin'] : 
        if len(request.files) > 1 or len(request.files) < 1 : 
            return "Exactly 1 file required" , 400
        
        for _, file in request.files.items():
            err = util.upload(file,fs,channel,access)
            
            if err : 
                return err 
        return "success!",200
    else : 
        return "Not Authorized", 401
    
    
@server.route("/download",methods=["GET"])
def download_mp3(): 

    if "Authorization" not in request.headers: 
        return "missing credentails", 401
    
    encoded_jwt=request.headers["Authorization"]
    if not encoded_jwt: 
        return  "missing credentails", 401
    
    url= f'http://{auth_pod_ip}/validate'
    response = requests.post(url,headers={'Authorization': encoded_jwt})
    
    if response.status_code != 200 : 
        return response.text,response.status_code
    

if __name__ == "__main__": 
    server.run(host='0.0.0.0',port=8080)
    