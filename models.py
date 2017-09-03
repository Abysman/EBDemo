from flask_sqlalchemy import SQLAlchemy
from flask_login import *
db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), unique=True)
    upwd = db.Column(db.String(100))

    def __init__(self,user_name,upwd):
    	# self.uid = uid
        self.uname=user_name
        self.upwd=upwd

    def get_id(self):
        return unicode(self.uid)

    def serialize(self):
    	return{
    		'uid':self.uid,
    		'uname':self.uname.encode('utf-8'),
    		'upwd':self.upwd.encode('utf-8')
    	}

class Product(db.Model):
	__tablename__ = 'product'
	pid = db.Column(db.Integer, primary_key=True)
	pname = db.Column(db.String(20))
	pprice = db.Column(db.Float)
	pstock = db.Column(db.Integer)
	pimg1_path = db.Column(db.String(100))
	pimg2_path = db.Column(db.String(100))

	def __repr__(self):
		return '<Product %r>' % self.pname

	def serialize(self):
		return{
				'pid':int(self.pid),
				'pname':self.pname.encode('utf-8'),
				'pprice':int(self.pprice),
				'pstock':int(self.pstock),
				'pimg1_path':self.pimg1_path.encode('utf-8'),
				'pimg2_path':self.pimg2_path.encode('utf-8')
		}

class Review(db.Model):
	__tablename__ = 'review'
	rid = db.Column(db.Integer, primary_key=True)
	rcontent = db.Column(db.String(200))
	pid = db.Column(db.Integer)
	uid = db.Column(db.Integer)

	def __init__(self,rcontent,pid,uid):
		self.rcontent = rcontent
		self.pid = pid
		self.uid = uid


	def __repr__(self):
		return '<Review %r>' % self.content


	def serialize(self):
		return{
				'rid':int(self.rid),
				'rcontent':self.rcontent.encode('utf-8'),
				'pid':int(self.pid),
				'uid':int(self.uid)
		}

class Orders(db.Model):
	__tablename__ = 'orders'
	oid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer)
	pid = db.Column(db.Integer)
	onum = db.Column(db.Integer,unique=True)

	def __init__(self,uid,pid,onum):
		self.uid = uid
		self.pid = pid
		self.onum = onum

	def __repr__(self):
		return '<Order %r>' % self.onum

	def serialize(self):
		return{
				'oid':self.oid,
				'uid':self.uid,
				'pid':self.pid,
				'onum':self.onum
		}

