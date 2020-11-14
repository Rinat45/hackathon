from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import xml.etree.ElementTree as ET

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
db = SQLAlchemy(app)

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
