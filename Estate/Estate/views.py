"""
Routes and views for the flask application.

"""

import os
import sys
import uuid


from datetime import datetime, timedelta 

from flask import render_template,request,flash,redirect, url_for,send_file,copy_current_request_context
from werkzeug.utils import secure_filename
from Estate import app,db,mail
from .models import estates,User,estates_success,readed_estates
from flask_login import login_user, logout_user, login_required,current_user
from flask_mail import  Message
from threading import Thread



def GetMessages(filter=None,curr_date=None):
	
	q=db.session.query(estates,User).join(User,User.id==estates.id_org)	
	if curr_date!=None:
		days = timedelta(30)
		print('date=',curr_date)
		date=curr_date-days;
		print('date=',date)
		query_=q.filter(estates.dat_>=date).order_by(estates.dat_).all()
	else:
		query_=q.order_by(estates.dat_).all()
	dat=[]
	for i in range(len(query_)):
		r=readed_estates.query.filter(readed_estates.id_estate==query_[i].estates.id,readed_estates.id_org==current_user.id).first()
		if r!=None:
			query_[i].estates.state=1		
		else:
			query_[i].estates.state=0
		if filter=='all' or filter==None:
			dat.append(query_[i])
		elif filter=='readed' and query_[i].estates.state==1:
			dat.append(query_[i])
		elif filter=='unreaded' and query_[i].estates.state==0:
			dat.append(query_[i])
	return dat
'''@async
def send_async_email(msg):
	with app.app_context():
		mail.send(msg)'''

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    

    @copy_current_request_context
    def send_message(msg):
        mail.send(msg)    
    thr = Thread(name='mail_sender', target=send_message, args=(msg,))
    thr.start()



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/addmess')
def addmessview():
    return render_template('new_mess.html')
@app.route('/addmess', methods=['POST'])
def addmess():
	
	name_estate = request.form.get('name_estate')
	addr = request.form.get('addr')
	area = request.form.get('area')
	kadastr= request.form.get('kadastr')
	state_estate= request.form.get('state_estate')
	contact= request.form.get('contact')
	img= request.form.get('img')	
	print('img=',img)
	if not(name_estate and name_estate.strip()):
		flash('Введите наименование объекта!')
		return redirect(url_for('addmess'))
	if not(addr and addr.strip()):
		flash('Введите адрес объекта!')
		return redirect(url_for('addmess'))
	if not(area):
		flash('Введите площадь объекта!')
		return redirect(url_for('addmess'))
	if not(kadastr and kadastr.strip()):
		flash('Введите кадастровый номер!')
		return redirect(url_for('addmess'))        
	if not(state_estate and state_estate.strip()):
		flash('Введите описание состояния объекта!')
		return redirect(url_for('addmess'))        
	if not(contact and contact.strip()):
		flash('Введите контактные данные ответственного лица!')
		return redirect(url_for('addmess'))        	
	img = request.files['img']
	if img==None:
		flash('Не уадлось прочитать файл!')
		return redirect(url_for('addmess'))
	unique_filename = str(current_user.id)+'_'+str(uuid.uuid4())+'_'+request.files['img'].filename
	full_name=os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
	img.save(full_name)      		
	new_estate=estates(id_org=current_user.id,name_estate=name_estate,addr=addr,
					area=area,kadastr=kadastr,description=state_estate,
					contact=contact,img_path=full_name)
	db.session.add(new_estate)	
	db.session.commit()	
	users_=User.query.all()
	dst_emails=[]
	for user in users_:
		if current_user.id!=user.id:
			dst_emails.append(user.email)
	
	if len(dst_emails)>0:	
		
		msg_body="Наименование объекта: "+name_estate+"\n"+"Адрес: "+addr+"\n"+"Кадастровый номер: "+kadastr
		send_email("Появилась публикация о новом объекте имущества",app.config['MAIL_USERNAME'],dst_emails,msg_body)
		'''msg = Message("Данные о свободном имуществе", sender=app.config['MAIL_USERNAME'],  recipients=dst_emails)
		msg.body="Наименование объекта: "
		mail.send(msg)'''
	flash('Публикация успешно размещена в сервисе!')
	return redirect(url_for('profile'))        	

@app.route('/viewmess',methods=['POST'])
def viewmesspost():
	filter = request.form.get('filter')
	print('filter=',filter)
	
	dates=GetMessages(filter)
	
	return render_template('estatesviews.html',dates_esates=dates,filter=filter)
@app.route('/viewmess',)
def viewmess():
	#query_ = db.session.query(estates)
	#query_ = query_.join(User,User.id==estates.id_org).all()	
	'''q=db.session.query(estates,User).join(User,User.id==estates.id_org)
	
	query_=q.order_by(estates.dat_).all()
	for i in range(len(query_)):
		r=readed_estates.query.filter(readed_estates.id_estate==query_[i].estates.id,readed_estates.id_org==current_user.id).first()
		if r!=None:
			query_[i].estates.state=1		
		else:
			query_[i].estates.state=0'''
	dates=GetMessages()
	
	return render_template('estatesviews.html',dates_esates=dates)
@app.route('/viewmess_new',)
def viewmess_new():
	#query_ = db.session.query(estates)
	#query_ = query_.join(User,User.id==estates.id_org).all()	
	'''q=db.session.query(estates,User).join(User,User.id==estates.id_org)
	
	query_=q.order_by(estates.dat_).all()
	for i in range(len(query_)):
		r=readed_estates.query.filter(readed_estates.id_estate==query_[i].estates.id,readed_estates.id_org==current_user.id).first()
		if r!=None:
			query_[i].estates.state=1		
		else:
			query_[i].estates.state=0'''
	curr_date=datetime.today()
	dates=GetMessages(None,curr_date)
	
	return render_template('estatesviews.html',dates_esates=dates)
@app.route('/photoshow')
def photoshow():	
	id=request.args.get('id')
	estate_ = estates.query.filter(estates.id==id).first()
	return render_template('photoshow.html',name_estate=estate_.name_estate,addr_estate=estate_.addr,filename=estate_.img_path)
@app.route('/display/<filename>')
def display_image(filename):	
	return send_file(filename)
@app.route('/accept_estate')
def accept_estate():	
	id=request.args.get('id')
	accept_ = estates_success.query.filter(estates_success.id_org==current_user.id,estates_success.id_estate==id).first()
	if accept_!=None:
		flash('Ошибка!Вы уже дали заявку принять данный объект!')
		q=db.session.query(estates,User).join(User,User.id==estates.id_org)	
		query_=q.order_by(estates.dat_).all()	
		return render_template('estatesviews.html',dates_esates=query_)
	estate_ = estates.query.filter(estates.id==id).first()
	return render_template('success.html',name_estate=estate_.name_estate,addr_estate=estate_.addr,filename=estate_.img_path,id=id)
@app.route('/add_accept', methods=['POST'])
def add_accept():
	
	res = request.form.get('res')
	id = request.form.get('id')
	print('res=',res)
	print('id=',id)
	if res=='ok':
		new_accept=estates_success(id_org=current_user.id,id_estate=id)
		db.session.add(new_accept)	
		estate_ = estates.query.filter(estates.id==id).first()
		estate_.count_succes=estate_.count_succes+1        
		db.session.commit()	
	return redirect(url_for('profile'))        	
@app.route('/view_accepts')
def view_accepts():
	#query_ = db.session.query(estates)
	#query_ = query_.join(User,User.id==estates.id_org).all()	
	id=request.args.get('id')
	
	q=db.session.query(estates_success,User).join(User,User.id==estates_success.id_org)
	
	print('query_=',q)
	query_=q.filter(estates_success.id_estate==id).order_by(estates_success.dat_).all()

	print('query_=',query_)
	
	return render_template('showaccepts.html',dates=query_)
@app.route('/readed_mess')
def readed_mess():	
	id=request.args.get('id')
	new_r=readed_estates(id_org=current_user.id,id_estate=id)
	db.session.add(new_r)	
	db.session.commit()	
	dates=GetMessages()
	flash('Запись отмечена как прочитанная!')
	return render_template('estatesviews.html',dates_esates=dates)

@app.route('/profile')
@login_required
def profile():	
	dates=GetMessages('unreaded')
	count_unread=len(dates)
	return render_template('profile.html', name=current_user.name,count_unread=count_unread)