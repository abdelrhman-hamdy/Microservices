#import mysql.connector
from flask import Flask, request
import jwt, datetime, os    # create tokens and set expiration date
from flask import Flask, request

server= Flask(__name__)

#mydb= mysql.connector.connect(
#  host='localhost',
#  user='auth_user',
#  password='root'
#)

mysqlcuror=mydb.cursor()
@server.route('/login',methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Credentials" , 401

    mysqlcuror.execute( f'SELECT email,Password FROM auth.user WHERE email="{auth.username}"' )
    row_data=mysqlcuror.fetchone()
    if len(row_data) > 0 :
        if row_data[1] != auth.password:
            return "Wrong Credentials" , 401
        return createJWT(auth.username,os.getenv("JWT_SECRET"),True)
    else:
        return "Wrong Credentials" , 401

@server.route('/validate',methods=["POST"])
def validateJWT():
    encoded_jwt= request.headers["Authorization"]
    if not encoded_jwt :
        return "missing credentails", 401
    token = encoded_jwt.split(" ")[1]
    print(token )
    try :
        decoded = jwt.decode(token, os.getenv("JWT_SECRET"),algorithm=["HS256"] )
    except:
        return "Wrong Credentials",403
    return decoded


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username":username,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat":datetime.datetime.utcnow(),
            "admin": authz
        },
            secret,
            algorithm="HS256",

    )

if __name__ == "__main__" :
    server.run(host="0.0.0.0",port=5000)
