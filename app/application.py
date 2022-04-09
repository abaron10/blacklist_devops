from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from modelos.modelos import BlackList, User, db
from flask_cors import CORS
from flask import request
import bcrypt
from datetime import datetime

def create_app(config_name):
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_system.db'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['JWT_SECRET_KEY'] = 'ROCK&ROLL_TRAIN_ACDC'
    application.config['PROPAGATE_EXCEPTION'] = True
    return application

application = create_app('default')
app_context = application.app_context()
app_context.push()
application.debug = True
db.init_app(application)
db.create_all()
cors = CORS(application)
jwt = JWTManager(application)


@application.route("/", methods=["GET"])
def index():
    return "pong"

@application.route("/auth/signup",methods=['POST'])
def sign_in_user():
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

@application.route("/auth/login",methods=['POST'])
def log_in_user():
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

@application.route("/blacklist/<string:email>",methods=['POST','GET'])
@jwt_required()
def blacklist(email=None):
    if request.method == 'POST':
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
    else:
        email_existance = True if BlackList.query.filter_by(email=email).first() else False
        if email_existance:
            return {"message": "Email exist in the blacklist."}, 201
        return {"message": "Email does'nt exist in the blacklist."}, 200

if __name__ == "__main__":
    application.run(port = 3000, debug = True)