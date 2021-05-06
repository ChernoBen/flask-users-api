import traceback
from flask_restful import Resource,reqparse
from models.UserModel import UserModel
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from werkzeug.security import safe_str_cmp
from utils.blocklist import BLOCKLIST

features = reqparse.RequestParser()
features.add_argument('email',type=str,required=True,help="Email cant not be blank")
features.add_argument('password',type=str,required=True,help='Password can not be blank')
features.add_argument('ativado',type=bool)

class User(Resource):

    arg = reqparse.RequestParser()
    arg.add_argument('email',type=str,required=True,help='E-mail can not be blank')
    arg.add_argument('password',type=float,required=True,help='password can not be blank')

    def get(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json(),200
        return{'message':'Hotel not found'},404

    @jwt_required()
    def delete(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': "An internal error ocurred while trying to delete user"}, 500
            return {'message':'User deleted'},200
        return {'message':'User does not exist'},404

class UserRegister(Resource):
    def post(self):
        dados = features.parse_args()
        if UserModel.find_by_email(dados['email']):
            return {'message':f"email {dados['email']} already exists."},400
        user = UserModel(**dados)
        #user.ativado = False
        id = user.user_id
        try:
            user.save_user()
            #user.send_email_confirmation()
        except Exception as e:
            user.delete_user()
            print(e)
            return {'message':'An internal error has ocurred '},500
        return {'message':'User creates successfully','id':id},200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = features.parse_args()
        user = UserModel.find_by_email(dados['email'])
        if user and safe_str_cmp(user.password,dados['password']):
            if user.ativado:
                access_token = create_access_token(identity=user.user_id)
                return {'access_token':access_token},200
            else:
                return {'message':'User not confirmed'},400
        return {'message':'user name is incorrect'},401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT token indetifier
        BLOCKLIST.add(jwt_id)
        return {'message':'Logged out successfully'},200

class UserConfirm(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {'message':'User not found'},404
        user.ativado = True
        return {'messae':'User id confirmed successfully'}