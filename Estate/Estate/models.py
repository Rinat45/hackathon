from flask_login import UserMixin
from sqlalchemy.sql import func
from Estate import db
import datetime


ROLE_USER = 0
ROLE_ADMIN = 1

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    org = db.Column(db.String(1000))
    tel = db.Column(db.String(30))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id,
                'email':self.email
            }
            return jwt.encode(
                payload,
                TOKEN.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    @staticmethod
    def decode_auth_token(auth_token):
        payload=None
        try:
            print('auth_token=',auth_token)
            payload = jwt.decode(auth_token, TOKEN.get('SECRET_KEY'))
            print('payload=',payload)
            return 0, payload
        except jwt.ExpiredSignatureError:
            print('expired')	
            return -1, payload
        except jwt.InvalidTokenError:
            print('invalid')	
            return -2, payload

class estates(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    id_org=db.Column(db.Integer)
    name_estate=db.Column(db.String(500))
    addr = db.Column(db.String(1000))
    area = db.Column(db.Float)
    kadastr = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    contact=db.Column(db.String(500))
    #img=db.Column(db.LargeBinary)
    img_path=db.Column(db.String(1000))
    dat_=db.Column(db.DateTime, default=func.now())
    state_=db.Column(db.Integer, default=0)
    count_succes=db.Column(db.Integer, default=0)

class readed_estates(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    id_org=db.Column(db.Integer)
    id_estate=db.Column(db.Integer)
    state=db.Column(db.Integer)  

class estates_success(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    id_org=db.Column(db.Integer)
    id_estate=db.Column(db.Integer)


    