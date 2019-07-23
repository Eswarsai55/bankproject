from flask import Flask,jsonify,request
import jwt
import datetime
from flask_sqlalchemy import SQLAlchemy
from functools import wraps




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/BankDetails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='secretkey'
db=SQLAlchemy(app)

from models import *


def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token=request.args.get('token')
		if not token:
			return jsonify({'message':'Token is required'}),403
		try:
			data=jwt.decode(token,app.config['SECRET_KEY'])
		except:
			return jsonify({'message':"Invalid Token"}),403
			
		return f(*args,**kwargs)
	return decorated


@app.route('/<ifsc>',methods=['GET'])
@token_required
def getbranchdetails(ifsc):
	try:
		branchdetails=Branches.query.filter_by(ifsc=ifsc).first()
		return jsonify(branchdetails.serialize())
	except Exception as e:
		return(str(e))

@app.route('/api/<bankid>',methods=['GET'])
@token_required
def getbankdetails(bankid):
	try:
		bankdetails=Banks.query.filter_by(id=bankid).first()
		return jsonify(bankdetails.serialize())
	except Exception as e:
		return(str(e))


@app.route('/login')
def login():
	auth_token = jwt.encode({'exp':datetime.datetime.utcnow()+datetime.timedelta(days=5)},app.config['SECRET_KEY'])
	return jsonify({'token':auth_token.decode('UTF-8')})




if __name__=='__main__':
	app.run(debug=True)