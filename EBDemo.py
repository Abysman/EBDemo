# -*- coding: UTF-8 -*-
import os, sqlite3, json
from flask_login import *

from flask import Flask, request, session, render_template, redirect ,url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

# from form import LoginForm
from sqlalchemy import func

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/logIn'
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
login_manager.init_app(app)

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:abysmaN169@127.0.0.1/EBDemo'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:456789@notebook.xuehan.me/EBDemo'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'you-can-not-guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.json_encoder = MyJSONEncoder

db.init_app(app)
# engine = = create_engine('mysql://root:456789@notebook.xuehan.me/EBDemo_t')
# conn = engine.connect()

@login_manager.user_loader
def load_user(uid):
	return User.query.filter_by(uid=uid).first()

@app.route('/')
def show_index():
	usr_info = json.dumps({'usrname':'not_logged_in'})
	if current_user.is_authenticated:
		usr_info = json.dumps({'usrname':current_user.uname})
	return render_template('index_on.html',usr_info=usr_info)

@app.route('/logIn', methods=['GET','POST'])
def logIn():
	# form = LoginForm()
	if request.method == 'POST':
		user_name = request.form.get('username')
		password = request.form.get('password')

		user = User(user_name, password)
		
		d = User.query.filter_by(uname=user_name).first()
		if d:
			if password==d.upwd:
				login_user(d)
				app.logger.debug('Logged in user %s', user.uname)
				return redirect(url_for('show_index'))
	return render_template('logIn.html')

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == 'POST':
		usrname = request.form.get('username')
		pwd = request.form.get('password')
		uid = db.session.query(func.max(User.uid)).first()[0] + 1

		new_user = User(usrname.encode('utf-8'),pwd.encode('utf-8'))

		db.session.add(new_user)
		db.session.commit()

		return redirect(url_for('logIn'))
	return render_template('register.html')

@app.route('/productList',methods=['POST'])
def productList():
	productSearched = request.form.get('productSearched').encode('utf-8')
	presult = Product.query.filter(Product.pname.like('%'+productSearched+'%')).all()

	usr_info = json.dumps({'usrname':'not_logged_in'})
	if current_user.is_authenticated:
		usr_info = json.dumps({'usrname':current_user.uname})

	ptmp=[p.serialize() for p in presult]

	for p in ptmp:
		pid = p['pid']
		numReview = db.session.query(Review).filter_by(pid=pid).count()
		p.update({'numReview':numReview})

	return render_template('productList.html',usr_info=usr_info,product_info=ptmp)

@app.route('/productDTG',methods=['POST','GET'])
def productDTG():
	return render_template('productDaTianGou.html')

@app.route('/product',methods=['POST','GET'])
def product():
	usr_info = json.dumps({'usrname':'not_logged_in'})
	if current_user.is_authenticated:
		usr_info = json.dumps({'usrname':current_user.uname})

	pname = request.form.get('pname')
	presult = Product.query.filter_by(pname=pname).first()
	ptmp = presult.serialize()

	pid = presult.pid
	reviews = Review.query.filter_by(pid=pid).all()
	rtmp = [r.serialize() for r in reviews]

	for r in rtmp:
		uid = r['uid']
		user_name = User.query.filter_by(uid=uid).first().uname
		r.update({"uname":user_name})

	return render_template('productFormat.html',usr_info=usr_info,productInfo = ptmp,reviews=rtmp)

@app.route('/generateOrder',methods=['POST','GET'])
def generateOrder():
	usr_info = json.dumps({'usrname':'not_logged_in'})
	if current_user.is_authenticated:
		usr_info = json.dumps({'usrname':current_user.uname})
	price = request.form.get('pprice')
	p = json.dumps({'pimg':request.form.get('pimg1_path').encode('utf-8'),'pname':request.form.get('pname')})

	return render_template('order.html',p=p,price=price,usr_info=usr_info)

@app.route('/postReview',methods=['POST','GET'])
@login_required
def postReview():

	usr_info = json.dumps({'usrname':current_user.uname})
	uid = current_user.uid

	if request.method == 'POST' and request.form.get('content'):
		cont = request.form.get('content')
		p = request.values['name']
		print p
		app.logger.debug('name: %s', p)
		pid = db.session.query(Product).filter_by(pname=p).all()

		new_review = Review(cont.encode('utf-8'),pid,uid)
		app.logger.debug('cont: %s', cont)
		return redirect(url_for('show_index'))
	else:
		p = json.dumps({'pimg':request.form.get('pimg1_path').encode('utf-8'),'pname':request.form.get('pname')})
		return render_template('review.html',usr_info=usr_info,p=p)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('show_index'))

if __name__ == '__main__':
	app.run(debug=True)