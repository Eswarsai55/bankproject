from app import db
import jwt



class Banks(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String())
	branch=db.relationship('Branches',backref='branches',lazy=True)
	
	def __init__(self,id,name):
		self.id=id
		self.name=name
	
	def serialize(self):
		return{
		'id':self.id,
		'name':self.name
		}
	

class Branches(db.Model):
	ifsc=db.Column(db.String(),primary_key=True)
	branch=db.Column(db.String())
	address=db.Column(db.String())
	city=db.Column(db.String())
	district=db.Column(db.String())
	state=db.Column(db.String())
	bank_id=db.Column(db.Integer,db.ForeignKey('banks.id'))
	
	
	def __init__(self,ifsc,branch,address,city,district,state,bank_id):
		self.ifsc=ifsc
		self.branch=branch
		self.address=address
		self.city=city
		self.district=district
		self.state=state
		self.bank_id=bank_id
	def encode_auth_token(self,id):
    
		try:
			payload = {					
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
			'iat': datetime.datetime.utcnow(),
			'sub': ifsc
			}
			return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
			)
		except Exception as e:
			return e	
	
		
	def serialize(self):
		return{
		'ifsc':self.ifsc,
		'branch':self.branch,
		'address':self.address,
		'city':self.city,
		'district':self.district,
		'state':self.state
		}
		
