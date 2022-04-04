from app.modelos.modelos import BlackList, User
import bcrypt
from flask_restful import Resource
from ..modelos import db, User, BlackList
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
import bcrypt

class VistaSignIn(Resource):

    def post(self):
        password1 = request.json["password1"]
        password2 = request.json["password2"]
        email = request.json["email"]
        if password1 != password2:
            return {"message": "Passwords must match in order to Sign-In"}, 403

        password1 = bcrypt.hashpw((password1).encode('utf-8'), bcrypt.gensalt())
        exist_email = User.query.filter_by(email=email).first() is not None
        if exist_email:
            return {"message": "This Email match an existent account.Try again!"}, 403
        new_user = User(username=request.json["username"], password1=password1, email=email)
        access_token = create_access_token(identity=request.json["username"])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "user created successfully", "access_token": access_token}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):
    def get(self):
        return "pong"

    def post(self):
        u_username = request.json["username"]
        u_password1 = request.json["password1"]
        user = User.query.filter_by(username=u_username).first()
        db.session.commit()

        if user is None:
            return "The username do not exist", 404

        if not bcrypt.checkpw(u_password1.encode('utf8'), user.password1):
            return "Incorrect password"

        else:
            access_token = create_access_token(identity=user.username)
            return {"message": "Access granted", "username": {"username": user.username, "id": user.id},
                    "access_token": access_token}


class VistaBlackList(Resource):
    
    @jwt_required()
    def get(self,email):
        email_existance = True if BlackList.query.filter_by(email=email).first() else False
        if email_existance:
            return {"message": "Email exist in the blacklist."}, 201
        return {"message": "Email does'nt exist in the blacklist."}, 200

    @jwt_required()
    def post(self):
        user_email = request.json["user_email"]
        uuid = "1"
        reason = request.json["reason"]
        ip =  request.remote_addr
        created_by = User.query.filter_by(username=get_jwt_identity()).first().id
        created_on = datetime.now() 

        email_existance = True if BlackList.query.filter_by(email=user_email).first() else False

        if not email_existance:
            new_email_to_list = BlackList(email=user_email, uuid=uuid, reason=reason,created_by=created_by,created_on=created_on,ip_addr=ip)
            db.session.add(new_email_to_list)
            db.session.commit()
            return {"message":"Email added to database of blacklist emails."},200
        return {"message": "Email already added to blacklist."}, 201
        