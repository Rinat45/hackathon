"""
This script runs the Estate application using a development server.
"""

from os import environ
from Estate import app
from Estate import WEB_conf

import ssl


if __name__ == '__main__':
	try:
		context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		context.load_cert_chain(WEB_conf.get('CERT'), WEB_conf.get('KEY'))
		app.run(ssl_context=context,host=WEB_conf.get('HOST'),port=WEB_conf.get('PORT'))
		printf('Web-server started!')
	except Exception as e:
		print('Error start server'+str(e))

	