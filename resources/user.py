import sqlite3
from flask_restful import Resource,reqparse

from models.user_model import UserModel

	

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="Username field cannot be blank")
	parser.add_argument('password',
		type=str,
		required=True,
		help="Password cannot be blank")

	def post(self):
		data = UserRegister.parser.parse_args()
		#Check if the user exists in the database
		if UserModel.find_by_username(data['username']): #implies if arg not None
			return {"message": "User already exists"}
        #If doesnt exist create e a new user
		user = UserModel(**data)#data['username'], data['password']
		user.save_to_db()

		return {"message":"User created successfully"},201
			
								
