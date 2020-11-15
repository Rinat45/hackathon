from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message


import xml.etree.ElementTree as ET

CONFIG_MAIL={
	'MAIL_SERVER':None,
	'MAIL_PORT':None,
	'MAIL_USE_TLS':False,
	'MAIL_USERNAME':False,
	'MAIL_PASSWORD':False,
	}


PATH_IMAGES={
	'path':None,
	}

"""
The flask application package.
"""
POSTGRES = {
    'user': 'manager',
    'pw': '1234',
    'db': 'chatbotsystem',
    'host': '127.0.0.1',
    'port': '54',
}

WEB_conf={
	'HOST'	:'127.0.0.1',
	'PORT'	:5000,
	'CERT'	:'cert.pem',
	'KEY'	:'key.pem',
}

def ReadConfigFromXML(nameFileXML):
	try:
		tree = ET.parse(nameFileXML)
		root = tree.getroot()
		web=root.find('web_server')
		host=web.find('host').text
		WEB_conf['HOST']=host
		port=int(web.find('port').text)
		WEB_conf['PORT']=port
		cert=web.find('cert').text
		WEB_conf['CERT']=cert
		key=web.find('key').text
		WEB_conf['KEY']=key
		web=root.find('postgresql')	
		POSTGRES['db']=web.find('database').text
		POSTGRES['pw']=web.find('password').text
		POSTGRES['user']=web.find('user').text
		POSTGRES['host']=web.find('host').text
		POSTGRES['port']=web.find('port').text	
		PATH_IMAGES['path']=root.find('UPLOAD_FOLDER').text
		print('Path=',PATH_IMAGES['path'])
		mail=root.find('email')
		CONFIG_MAIL['MAIL_SERVER']=mail.find('MAIL_SERVER').text
		CONFIG_MAIL['MAIL_PORT']=mail.find('MAIL_PORT').text
		CONFIG_MAIL['MAIL_USE_TLS']=mail.find('MAIL_USE_TLS').text
		CONFIG_MAIL['MAIL_USERNAME']=mail.find('MAIL_USERNAME').text
		CONFIG_MAIL['MAIL_PASSWORD']=mail.find('MAIL_PASSWORD').text
	except Exception as e:
		print('Error read config:'+str(e))
		return False
	return True






from flask import Flask

ReadConfigFromXML('config.xml')

print('Postgresql=',POSTGRES)
app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['UPLOAD_FOLDER']=PATH_IMAGES['path']

app.config['MAIL_SERVER'] = CONFIG_MAIL['MAIL_SERVER']
app.config['MAIL_PORT'] = CONFIG_MAIL['MAIL_PORT']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = CONFIG_MAIL['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = CONFIG_MAIL['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = CONFIG_MAIL['MAIL_PASSWORD']



db = SQLAlchemy(app)

mail = Mail(app)



login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User
@login_manager.user_loader
def load_user(user_id):
	# since the user_id is just the primary key of our user table, use it in the query for the user
	return User.query.get(int(user_id))


import Estate.views
import Estate.auth
