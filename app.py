from flask import Flask,jsonify
from flask_restful import  Api
from flask_jwt import JWT,timedelta

from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from security import authenticate, identity as identity_function

app = Flask(__name__)
app.secret_key = 'David'
api = Api(app)



#change default /auth to custom /login URL 
app.config['JWT_AUTH_URL_RULE'] ='/login' 

#Change token expiration time from default 5 minutes to half an hour
app.config['JWT_EXPIRATION_DELTA'] =  timedelta(seconds=1800)

#config JWT aauth key name to be 'email' instead of default 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

jwt = JWT(app,authenticate,identity_function) #/auth

#customize error handler
#@jwt.error_handlers
def customized_error_handler(error):
	return jsonify({'message':error.description, 'code':error.status_code}),error.status_code

#customize JWT auth response, include user_id in response body
@jwt.auth_response_handler
def customized_response_handler(access_token,identity):
	return jsonify({'access_token':access_token.decode('utf-8'), 'user_id':identity.id})


		
api.add_resource(Item,'/item/<string:name>') #hhtp://127.0.0.1:5001/student/David
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5001,debug=True)
